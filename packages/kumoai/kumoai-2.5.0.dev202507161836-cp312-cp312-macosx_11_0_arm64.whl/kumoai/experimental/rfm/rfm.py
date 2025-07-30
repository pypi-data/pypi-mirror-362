import json
import warnings
from typing import List, Optional, Union

import numpy as np
import pandas as pd
from kumoapi.model_plan import RunMode
from kumoapi.pquery import QueryType
from kumoapi.rfm import (
    Context,
    PQueryDefinition,
    RFMEvaluateRequest,
    RFMPredictRequest,
    RFMValidateQueryRequest,
)
from kumoapi.task import TaskType

from kumoai import global_state
from kumoai.exceptions import HTTPException
from kumoai.experimental.rfm import LocalGraph
from kumoai.experimental.rfm.local_graph_sampler import LocalGraphSampler
from kumoai.experimental.rfm.local_graph_store import LocalGraphStore
from kumoai.experimental.rfm.local_pquery_driver import LocalPQueryDriver
from kumoai.utils import ProgressLogger

_RANDOM_SEED = 42

_MAX_CONTEXT_SIZE = {
    RunMode.DEBUG: 100,
    RunMode.FAST: 1_000,
    RunMode.NORMAL: 5_000,
    RunMode.BEST: 10_000,
}
_MAX_TEST_SIZE = {
    RunMode.DEBUG: 100,
    RunMode.FAST: 1_000,
    RunMode.NORMAL: 2_000,
    RunMode.BEST: 4_000,
}


class KumoRFM:
    r"""The Kumo Relational Foundation model (RFM) from the `KumoRFM: A
    Foundation Model for In-Context Learning on Relational Data
    <https://kumo.ai/research/kumo_relational_foundation_model.pdf>`_ paper.

    :class:`KumoRFM` is a foundation model to generate predictions for any
    relational dataset without training.
    The model is pre-trained and the class provides an interface to query the
    model from a :class:`LocalGraph` object.

    .. code-block:: python

        from kumoai.experimental.rfm import LocalGraph, KumoRFM

        df_users = pd.DataFrame(...)
        df_items = pd.DataFrame(...)
        df_orders = pd.DataFrame(...)

        graph = LocalGraph.from_data({
            'users': df_users,
            'items': df_items,
            'orders': df_orders,
        })

        rfm = KumoRFM(graph)

        query = ("PREDICT COUNT(transactions.*, 0, 30, days)>0 "
                 "FOR users.user_id=0")
        result = rfm.query(query)

        print(result)  # user_id  COUNT(transactions.*, 0, 30, days) > 0
                       # 1        0.85

    Args:
        graph: The graph.
        verbose: Whether to print verbose output.
    """
    def __init__(self, graph: LocalGraph, verbose: bool = True) -> None:
        graph = graph.validate()
        self._graph_def = graph._to_api_graph_definition()
        self._graph_store = LocalGraphStore(graph, verbose=verbose)
        self._graph_sampler = LocalGraphSampler(self._graph_store)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    # TODO add @overload
    def predict(
        self,
        query: str,
        *,
        explain: bool = False,
        anchor_time: Optional[pd.Timestamp] = None,
        run_mode: Union[RunMode, str] = RunMode.FAST,
        num_hops: int = 2,
        random_seed: Optional[int] = _RANDOM_SEED,
        verbose: bool = True,
    ) -> pd.DataFrame:  # Add explain
        """Returns predictions for a predictive query.

        Args:
            query: The predictive query.
            explain: Whether to return explanations for the query.
            anchor_time: The anchor timestamp for the query.
            run_mode: The :class:`RunMode` for the query.
            num_hops: The number of hops to sample when generating the context.
            random_seed: A manual seed for generating pseudo-random numbers.
            verbose: Whether to print verbose output.

        Returns:
            The predictions as a :class:`pandas.DataFrame`
        """
        query_def = self._parse_query(query)

        if explain and run_mode in {RunMode.NORMAL, RunMode.BEST}:
            warnings.warn(f"Explainability is currently only supported for "
                          f"run mode 'FAST' (got '{run_mode}'). Provided run "
                          f"mode has been reset. Please lower the run mode to "
                          f"suppress this warning.")

        if explain:
            assert query_def.entity.ids is not None
            if len(query_def.entity.ids.value) > 1:
                raise ValueError(
                    f"Cannot explain predictions for more than a single "
                    f"entity (got {len(query_def.entity.ids.value)})")

        if explain:
            msg = f'Explaining {str(query_def)[8:]}'
        else:
            msg = f'Predicting {str(query_def)[8:]}'

        with ProgressLogger(msg, verbose=verbose) as logger:
            context = self._get_context(
                query_def,
                anchor_time=anchor_time,
                run_mode=RunMode(run_mode),
                num_hops=num_hops,
                evaluate=False,
                random_seed=random_seed,
                logger=logger,
            )
            request = RFMPredictRequest(
                context=context,
                run_mode=RunMode(run_mode),
            )
            request_bytes = request.serialize()
            logger.log(f"Generated context of size "
                       f"{len(request_bytes) / (1024*1024):.2f}MB")

            try:
                if explain:
                    resp = global_state.client.rfm_api.explain(request_bytes)
                else:
                    resp = global_state.client.rfm_api.predict(request_bytes)
            except HTTPException as e:
                try:
                    msg = json.loads(e.detail)['detail']
                except Exception:
                    msg = e.detail
                raise RuntimeError(f"An unexpected exception occurred. "
                                   f"Please create an issue at "
                                   f"'https://github.com/kumo-ai/kumo-rfm'. "
                                   f"{msg}") from None

        return pd.DataFrame(**resp.prediction)

    def evaluate(
        self,
        query: str,
        *,
        metrics: Optional[List[str]] = None,
        anchor_time: Optional[pd.Timestamp] = None,
        run_mode: Union[RunMode, str] = RunMode.FAST,
        num_hops: int = 2,
        random_seed: Optional[int] = _RANDOM_SEED,
        verbose: bool = True,
    ) -> pd.DataFrame:
        """Evaluates a predictive query.

        Args:
            query: The predictive query.
            metrics: The metrics to use.
            anchor_time: The anchor timestamp for the query.
            run_mode: The :class:`RunMode` for the query.
            num_hops: The number of hops to sample when generating the context.
            random_seed: A manual seed for generating pseudo-random numbers.
            verbose: Whether to print verbose output.

        Returns:
            The metrics as a :class:`pandas.DataFrame`
        """
        query_def = self._parse_query(query)

        msg = f'Evaluating {str(query_def)[8:]}'
        with ProgressLogger(msg, verbose=verbose) as logger:
            context = self._get_context(
                query_def,
                anchor_time=anchor_time,
                run_mode=RunMode(run_mode),
                num_hops=num_hops,
                evaluate=True,
                random_seed=random_seed,
                logger=logger if verbose else None,
            )
            if metrics is not None and len(metrics) > 0:
                self._validate_metrics(metrics, context.task_type)
                metrics = list(dict.fromkeys(metrics))
            request = RFMEvaluateRequest(
                context=context,
                run_mode=RunMode(run_mode),
                metrics=metrics,
            )
            request_bytes = request.serialize()
            logger.log(f"Generated context of size "
                       f"{len(request_bytes) / (1024*1024):.2f}MB")

            try:
                resp = global_state.client.rfm_api.evaluate(request_bytes)
            except HTTPException as e:
                try:
                    msg = json.loads(e.detail)['detail']
                except Exception:
                    msg = e.detail
                raise RuntimeError(f"An unexpected exception occurred. "
                                   f"Please create an issue at "
                                   f"'https://github.com/kumo-ai/kumo-rfm'. "
                                   f"{msg}") from None

        return pd.DataFrame.from_dict(
            resp.metrics,
            orient='index',
            columns=['value'],
        ).reset_index(names='metric')

    # Helpers #################################################################

    def _parse_query(self, query: str) -> PQueryDefinition:
        try:
            request = RFMValidateQueryRequest(
                query=query,
                graph_definition=self._graph_def,
            )

            resp = global_state.client.rfm_api.validate_query(request)
            # TODO Expose validation warnings.

            if len(resp.validation_response.warnings) > 0:
                msg = '\n'.join([
                    f'{i+1}. {warning.title}: {warning.message}' for i, warning
                    in enumerate(resp.validation_response.warnings)
                ])
                warnings.warn(f"Encountered the following warnings during "
                              f"parsing:\n{msg}")

            return resp.query_definition
        except HTTPException as e:
            try:
                msg = json.loads(e.detail)['detail']
            except Exception:
                msg = e.detail
            raise ValueError(f"Failed to parse query '{query}'. "
                             f"{msg}") from None

    def _validate_time(
        self,
        query: PQueryDefinition,
        anchor_time: pd.Timestamp,
        evaluate: bool,
    ) -> None:

        if self._graph_store.min_time == pd.Timestamp.max:
            return  # Graph without timestamps

        if anchor_time < self._graph_store.min_time:
            raise ValueError(f"Anchor timestamp '{anchor_time}' is before "
                             f"the earliest timestamp "
                             f"'{self._graph_store.min_time}' in the data.")

        if anchor_time - query.target.end_offset < self._graph_store.min_time:
            raise ValueError(f"Anchor timestamp is too early or aggregation "
                             f"time range is too large. To make this "
                             f"prediction, we would need data back to "
                             f"'{anchor_time - query.target.end_offset}', "
                             f"however, your data only contains data back to "
                             f"'{self._graph_store.min_time}'.")

        if (anchor_time - 2 * query.target.end_offset
                < self._graph_store.min_time):
            warnings.warn(f"Anchor timestamp is too early or aggregation "
                          f"time range is too large. To form proper input "
                          f"data, we would need data back to "
                          f"'{anchor_time - 2 * query.target.end_offset}', "
                          f"however, your data only contains data back to "
                          f"'{self._graph_store.min_time}'.")

        if (not evaluate and anchor_time
                > self._graph_store.max_time + pd.DateOffset(days=1)):
            warnings.warn(f"Anchor timestamp '{anchor_time}' is after the "
                          f"latest timestamp '{self._graph_store.max_time}' "
                          f"in the data. Please make sure this is intended.")

        if (evaluate and anchor_time
                > self._graph_store.max_time - query.target.end_offset):
            raise ValueError(
                f"Anchor timestamp for evaluation is after the latest "
                f"supported timestamp "
                f"'{self._graph_store.max_time - query.target.end_offset}'.")

    def _get_context(
        self,
        query: PQueryDefinition,
        anchor_time: Optional[pd.Timestamp],
        run_mode: RunMode,
        num_hops: int,
        evaluate: bool,
        random_seed: Optional[int] = _RANDOM_SEED,
        logger: Optional[ProgressLogger] = None,
    ) -> Context:

        if num_hops < 0:
            raise ValueError(f"'num_hops' must be non-negative "
                             f"(got {num_hops})")
        if num_hops > 4:
            raise ValueError(f"Cannot predict on subgraphs with more than 4 "
                             f"hops (got {num_hops}). Please reduce the "
                             f"number of hops and try again. Please create a "
                             f"feature request at "
                             f"'https://github.com/kumo-ai/kumo-rfm' if you "
                             f"must go beyond this for your use-case.")

        if anchor_time is None:
            anchor_time = self._graph_store.max_time
            if evaluate:
                anchor_time = anchor_time - query.target.end_offset

        assert anchor_time is not None
        self._validate_time(query, anchor_time, evaluate)

        query_driver = LocalPQueryDriver(self._graph_store, query, random_seed)
        task_type = query.get_task_type(
            stypes=self._graph_store.stype_dict,
            edge_types=self._graph_store.edge_types,
        )

        if logger is not None:
            if task_type == TaskType.BINARY_CLASSIFICATION:
                task_type_repr = 'binary classification'
            elif task_type == TaskType.MULTICLASS_CLASSIFICATION:
                task_type_repr = 'multi-class classification'
            elif task_type == TaskType.REGRESSION:
                task_type_repr = 'regression'
            elif task_type == TaskType.TEMPORAL_LINK_PREDICTION:
                task_type_repr = 'link prediction'
            else:
                task_type_repr = str(task_type)
            logger.log(f"Identified {query.query_type} {task_type_repr} task")

        if task_type.is_link_pred and num_hops < 2:
            raise ValueError(f"Cannot perform link prediction on subgraphs "
                             f"with less than 2 hops (got {num_hops}) since "
                             f"historical target entities need to be part of "
                             f"the context. Please increase the number of "
                             f"hops and try again.")

        y_test: Optional[pd.Series] = None
        if evaluate:
            max_test_size = _MAX_TEST_SIZE[run_mode]
            if task_type.is_link_pred:
                max_test_size = max_test_size // 5

            test_node, y_test = query_driver.collect_test(
                size=max_test_size,
                anchor_time=anchor_time,
            )
            if logger is not None:
                logger.log(f"Collected {len(y_test):,} test examples")

        else:
            assert query.entity.ids is not None
            test_node = self._graph_store.get_node_id(
                table_name=query.entity.pkey.table_name,
                pkey=pd.Series(
                    query.entity.ids.value,
                    dtype=query.entity.ids.dtype,
                ),
            )

        test_time = pd.Series(anchor_time).repeat(
            len(test_node)).reset_index(drop=True)

        train_node, train_time, y_train = query_driver.collect_train(
            size=_MAX_CONTEXT_SIZE[run_mode],
            anchor_time=anchor_time,
            exclude_node=test_node
            if query.query_type == QueryType.STATIC else None,
        )

        if logger is not None:
            if task_type == TaskType.BINARY_CLASSIFICATION:
                pos = 100 * int((y_train > 0).sum()) / len(y_train)
                msg = (f"Collected {len(y_train):,} in-context examples with "
                       f"{pos:.2f}% positive cases")
            elif task_type == TaskType.MULTICLASS_CLASSIFICATION:
                msg = (f"Collected {len(y_train):,} in-context examples "
                       f"holding {y_train.nunique()} classes")
            elif task_type == TaskType.REGRESSION:
                _min, _max = np.quantile(y_train.to_numpy(), [0.05, 0.95])
                msg = (f"Collected {len(y_train):,} in-context examples with "
                       f"targets between {format_value(float(_min))} and "
                       f"{format_value(float(_max))}")
            elif task_type == TaskType.TEMPORAL_LINK_PREDICTION:
                num_rhs = y_train.explode().nunique()
                msg = (f"Collected {len(y_train):,} in-context examples with "
                       f"{num_rhs:,} unique items")
            else:
                raise NotImplementedError
            logger.log(msg)

        entity_table_names = query.get_entity_table_names(
            self._graph_store.edge_types)

        subgraph = self._graph_sampler(
            entity_table_names=entity_table_names,
            node=np.concatenate([train_node, test_node]),
            time=np.concatenate([
                train_time.astype(int).to_numpy(),
                test_time.astype(int).to_numpy(),
            ]),
            run_mode=run_mode,
            num_hops=num_hops,
            exclude_cols_dict=query.exclude_cols_dict,
        )

        return Context(
            task_type=task_type,
            entity_table_names=entity_table_names,
            subgraph=subgraph,
            y_train=y_train,
            y_test=y_test,
            top_k=query.top_k,
        )

    @staticmethod
    def _validate_metrics(
        metrics: List[str],
        task_type: TaskType,
    ) -> None:

        if task_type == TaskType.BINARY_CLASSIFICATION:
            supported_metrics = [
                'acc', 'precision', 'recall', 'f1', 'auroc', 'auprc', 'ap'
            ]
        elif task_type == TaskType.MULTICLASS_CLASSIFICATION:
            supported_metrics = ['acc', 'precision', 'recall', 'f1', 'mrr']
        elif task_type == TaskType.REGRESSION:
            supported_metrics = ['mae', 'mape', 'mse', 'rmse', 'smape']
        elif task_type == TaskType.TEMPORAL_LINK_PREDICTION:
            supported_metrics = [
                'map@', 'ndcg@', 'mrr@', 'precision@', 'recall@', 'f1@',
                'hit_ratio@'
            ]
        else:
            raise NotImplementedError

        for metric in metrics:
            if '@' in metric:
                metric_split = metric.split('@')
                if len(metric_split) != 2:
                    raise ValueError(f"Unsupported metric '{metric}'. "
                                     f"Available metrics "
                                     f"are {supported_metrics}.")

                name, top_k = f'{metric_split[0]}@', metric_split[1]

                if not top_k.isdigit():
                    raise ValueError(f"Metric '{metric}' does not define a "
                                     f"valid 'top_k' value (got '{top_k}').")

                if int(top_k) <= 0:
                    raise ValueError(f"Metric '{metric}' needs to define a "
                                     f"positive 'top_k' value (got '{top_k}')")

                if int(top_k) > 100:
                    raise ValueError(f"Metric '{metric}' defines a 'top_k' "
                                     f"value greater than 100 "
                                     f"(got '{top_k}'). Please create a "
                                     f"feature request at "
                                     f"'https://github.com/kumo-ai/kumo-rfm' "
                                     f"if you must go beyond this for your "
                                     f"use-case.")

                metric = name

            if metric not in supported_metrics:
                raise ValueError(f"Unsupported metric '{metric}'. Available "
                                 f"metrics are {supported_metrics}. If you "
                                 f"feel a metric is missing, please create a "
                                 f"feature request at "
                                 f"'https://github.com/kumo-ai/kumo-rfm'.")


def format_value(value: Union[int, float]) -> str:
    if value == int(value):
        return f'{int(value):,}'
    if abs(value) >= 1000:
        return f'{value:,.0f}'
    if abs(value) >= 10:
        return f'{value:.1f}'
    return f'{value:.2f}'
