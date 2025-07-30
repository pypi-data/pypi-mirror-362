from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from kumoapi.pquery import QueryType
from kumoapi.rfm import PQueryDefinition

import kumolib
from kumoai.experimental.rfm.local_graph_store import LocalGraphStore
from kumoai.experimental.rfm.pquery import PQueryPandasBackend


class LocalPQueryDriver:
    def __init__(
        self,
        graph_store: LocalGraphStore,
        query: PQueryDefinition,
        random_seed: Optional[int],
    ) -> None:
        self._graph_store = graph_store
        self._query = query
        self._rng = np.random.default_rng(random_seed)

    def _get_candidates(
        self,
        exclude_node: Optional[np.ndarray] = None,
    ) -> np.ndarray:

        if self._query.query_type == QueryType.TEMPORAL:
            assert exclude_node is None

        table_name = self._query.entity.pkey.table_name
        num_nodes = len(self._graph_store.df_dict[table_name])
        mask_dict = self._graph_store.mask_dict

        # Case 1: All nodes are valid and nothing to exclude:
        if exclude_node is None and table_name not in mask_dict:
            return np.arange(num_nodes)

        # Case 2: Not all nodes are valid - lookup valid nodes:
        if exclude_node is None:
            pkey_map = self._graph_store.pkey_map_dict[table_name]
            return pkey_map['arange'].to_numpy().copy()

        # Case 3: Exclude nodes - use a mask to exclude them:
        mask = np.full((num_nodes, ), fill_value=True, dtype=bool)
        mask[exclude_node] = False
        if table_name in mask_dict:
            mask &= mask_dict[table_name]
        return mask.nonzero()[0]

    def collect_test(
        self,
        size: int,
        anchor_time: pd.Timestamp,
        batch_size: int = 1024,
        max_iterations: int = 20,
    ) -> Tuple[np.ndarray, pd.Series]:

        candidate = self._get_candidates()
        self._rng.shuffle(candidate)

        nodes: List[np.ndarray] = []
        ys: List[pd.Series] = []

        num_labels = candidate_offset = 0
        time = pd.Series(anchor_time).repeat(batch_size).reset_index(drop=True)
        for _ in range(max_iterations):
            node = candidate[candidate_offset:candidate_offset + batch_size]

            y, mask = self(node, time[:len(node)])

            nodes.append(node[mask])
            ys.append(y)

            num_labels += len(y)

            if num_labels > size:
                break  # Sufficient number of labels collected. Abort.

            candidate_offset += batch_size
            if candidate_offset >= len(candidate):
                break

        if len(nodes) > 1:
            node = np.concatenate(nodes, axis=0)[:size]
            y = pd.concat(ys, axis=0).reset_index(drop=True)[:size]
        else:
            node = nodes[0][:size]
            y = ys[0][:size]

        if len(node) == 0:
            raise RuntimeError("Failed to generate any test examples for "
                               "evaluation. Is your predictive query too "
                               "restrictive?")

        return node, y

    def collect_train(
        self,
        size: int,
        anchor_time: pd.Timestamp,
        exclude_node: Optional[np.ndarray] = None,
        batch_size: int = 1024,
        max_iterations: int = 20,
    ) -> Tuple[np.ndarray, pd.Series, pd.Series]:

        candidate = self._get_candidates(exclude_node)
        self._rng.shuffle(candidate)

        if len(candidate) == 0:
            raise RuntimeError("Failed to generate any context examples "
                               "since there exists not enough entities")

        nodes: List[np.ndarray] = []
        times: List[pd.Series] = []
        ys: List[pd.Series] = []

        num_labels = candidate_offset = 0
        anchor_time = anchor_time - self._query.target.end_offset
        for _ in range(max_iterations):
            node = candidate[candidate_offset:candidate_offset + batch_size]
            time = pd.Series(anchor_time).repeat(len(node))
            time = time.reset_index(drop=True)

            y, mask = self(node, time)

            nodes.append(node[mask])
            times.append(time[mask].reset_index(drop=True))
            ys.append(y)

            num_labels += len(y)

            if num_labels > size:
                break  # Sufficient number of labels collected. Abort.

            candidate_offset += batch_size
            if candidate_offset >= len(candidate):
                # Restart with an earlier anchor time (if applicable).
                if self._query.query_type == QueryType.STATIC:
                    break  # Cannot jump back in time for static PQs. Abort.
                candidate_offset = 0
                anchor_time = anchor_time - self._query.target.end_offset
                if anchor_time < self._graph_store.min_time:
                    break  # No earlier anchor time left. Abort.

        if len(nodes) > 1:
            node = np.concatenate(nodes, axis=0)[:size]
            time = pd.concat(times, axis=0).reset_index(drop=True)[:size]
            y = pd.concat(ys, axis=0).reset_index(drop=True)[:size]
        else:
            node = nodes[0][:size]
            time = times[0][:size]
            y = ys[0][:size]

        if len(node) == 0:
            raise ValueError("Failed to generate any context examples. Is "
                             "your predictive query too restrictive?")

        return node, time, y

    def __call__(
        self,
        node: np.ndarray,
        anchor_time: pd.Series,
    ) -> Tuple[pd.Series, np.ndarray]:

        specs = self._query.get_sampling_specs(self._graph_store.edge_types)
        num_hops = max([spec.hop for spec in specs] + [0])
        num_neighbors: Dict[Tuple[str, str, str], list[int]] = {}
        for spec in specs:
            if spec.edge_type not in num_neighbors:
                num_neighbors[spec.edge_type] = [0] * num_hops
            num_neighbors[spec.edge_type][spec.hop - 1] = -1

        edge_types = list(num_neighbors.keys())
        node_types = list(
            set([self._query.entity.pkey.table_name])
            | set(src for src, _, _ in edge_types)
            | set(dst for _, _, dst in edge_types))

        sampler = kumolib.NeighborSampler(  # type: ignore[attr-defined]
            node_types,
            edge_types,
            {
                '__'.join(edge_type): self._graph_store.colptr_dict[edge_type]
                for edge_type in edge_types
            },
            {
                '__'.join(edge_type): self._graph_store.row_dict[edge_type]
                for edge_type in edge_types
            },
            {
                node_type: time
                for node_type, time in self._graph_store.time_dict.items()
                if node_type in node_types
            },
        )

        forward_time = anchor_time + self._query.target.end_offset
        _, _, node_dict, batch_dict, _, _ = sampler.sample(
            {
                '__'.join(edge_type): np.array(values)
                for edge_type, values in num_neighbors.items()
            },
            {},  # TODO use date offset based sampling
            self._query.entity.pkey.table_name,
            node,
            forward_time.astype(int).to_numpy(),
        )

        feat_dict: Dict[str, pd.DataFrame] = {}
        for table_name, columns in self._query.column_dict.items():
            df = self._graph_store.df_dict[table_name]
            row_id = node_dict[table_name]
            df = df[list(columns)].iloc[row_id].reset_index(drop=True)
            feat_dict[table_name] = df

        time_dict: Dict[str, pd.Series] = {}
        for table_name in self._query.time_tables:
            df = self._graph_store.df_dict[table_name]
            row_id = node_dict[table_name]
            ser = df[self._graph_store.time_column_dict[table_name]]
            ser = ser.iloc[row_id].reset_index(drop=True)
            time_dict[table_name] = ser

        y, mask = PQueryPandasBackend().eval_pquery(
            query=self._query,
            feat_dict=feat_dict,
            time_dict=time_dict,
            batch_dict=batch_dict,
            anchor_time=anchor_time,
        )

        return y, mask
