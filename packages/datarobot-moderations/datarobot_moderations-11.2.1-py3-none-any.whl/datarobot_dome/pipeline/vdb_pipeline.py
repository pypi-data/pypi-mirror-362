#  ---------------------------------------------------------------------------------
#  Copyright (c) 2025 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2025.
#
#  DataRobot, Inc. Confidential.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#  ---------------------------------------------------------------------------------
import logging
import time
from typing import Any
from typing import Optional

import pandas as pd
from datarobot.enums import CustomMetricAggregationType
from datarobot.enums import CustomMetricDirectionality

from datarobot_dome.constants import CUSTOM_METRIC_DESCRIPTION_SUFFIX
from datarobot_dome.constants import LOGGER_NAME_PREFIX
from datarobot_dome.constants import ModerationEventTypes
from datarobot_dome.metrics.factory import MetricScorerFactory
from datarobot_dome.metrics.metric_scorer import MetricScorer
from datarobot_dome.metrics.metric_scorer import ScorerType
from datarobot_dome.pipeline.pipeline import Pipeline

LATENCY_NAME = "VDB Score Latency"
DEFAULT_PER_PREDICTION = True

score_latency = {
    "name": LATENCY_NAME,
    "directionality": CustomMetricDirectionality.LOWER_IS_BETTER,
    "units": "seconds",
    "type": CustomMetricAggregationType.AVERAGE,
    "baselineValue": 0,
    "isModelSpecific": True,
    "timeStep": "hour",
    "description": f"Latency of actual VDB Score. {CUSTOM_METRIC_DESCRIPTION_SUFFIX}",
}


class VDBPipeline(Pipeline):
    def __init__(self, config: Optional[dict[str, Any]] = None):
        super().__init__()
        metric_config = config.get("metrics", {}) if config else {}
        self._score_configs: dict[ScorerType, dict[str, Any]] = {
            stype.value: metric_config.get(stype.lower().replace("_", "-"), {})
            for stype in ScorerType
        }
        self._scorers: list[MetricScorer] = list()
        self._logger = logging.getLogger(LOGGER_NAME_PREFIX + "." + self.__class__.__name__)
        self._add_default_custom_metrics()
        self.create_custom_metrics_if_any()
        self.create_scorers()
        self.update_custom_metric_association_ids()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({len(self.custom_metrics)} metrics)"

    def _add_default_custom_metrics(self):
        """Adds the default custom metrics based on the `_score_configs` map."""
        # create a list of tuples, so we can track the scorer type
        metric_list = [(score_latency, False, None)]
        for score_type, score_config in self._score_configs.items():
            metric_def = MetricScorerFactory.custom_metric_config(score_type, score_config)
            per_row = score_config.get("per-prediction", DEFAULT_PER_PREDICTION)
            metric_list.append((metric_def, per_row, score_type))

        # Metric list so far does not need association id for reporting
        for metric_def, per_row, score_type in metric_list:
            self.add_custom_metric(metric_def, per_row, scorer_type=score_type)

    def create_scorers(self):
        """
        Creates a scorer for each metric in the custom_metric_map list.

        NOTE: all metrics that failed to be created in DR app have been removed
        """
        if not self._deployment:
            self._logger.debug("Skipping creation of scorers due to no deployment")
            return

        input_column = self._deployment.model["target_name"]
        for metric_name, metric_data in self.custom_metric_map.items():
            score_type = metric_data.get("scorer_type")
            if not score_type:
                continue

            score_config = self._score_configs.get(score_type)
            if score_config.get("input_column") is None:
                score_config["input_column"] = input_column
            scorer = MetricScorerFactory.create(score_type, score_config)
            self._scorers.append(scorer)

    def update_custom_metric_association_ids(self):
        """Update whether tracking per-prediction metrics based on deployment settings."""
        has_assoc = bool(self._association_id_column_name)
        for metric_name, metric_data in self.custom_metric_map.items():
            score_type = metric_data.get("scorer_type")
            if not score_type:
                continue

            scorer_config = self._score_configs.get(score_type, {})
            per_assoc = scorer_config.get("per-prediction", DEFAULT_PER_PREDICTION)
            metric_data["requires_association_id"] = has_assoc and per_assoc

    def scorers(self) -> list[MetricScorer]:
        """Get all scorers for this pipeline."""
        return self._scorers

    def record_aggregate_value(self, metric_name: str, value: Any) -> None:
        """
        Locally records the metric_name/value in the pipeline's area for aggregate metrics where the
        bulk upload with pick it up.
        """
        if self.aggregate_custom_metric is None:
            return

        entry = self.aggregate_custom_metric[metric_name]
        self.set_custom_metrics_aggregate_entry(entry, value)

    def record_score_latency(self, latency_in_sec: float):
        """Records aggregate latency metric value locally"""
        self.record_aggregate_value(LATENCY_NAME, latency_in_sec)

    def report_custom_metrics(self, individual_metrics: list[dict[str, Any]]) -> None:
        """
        Reports all the custom-metrics to DR app.

        The bulk upload includes grabbing all the aggregated metrics, plus the list of
        individual metric payloads.
        """
        if self.delayed_custom_metric_creation:
            # Flag is not set yet, so no point reporting custom metrics
            return

        if not self._deployment:
            # in "test" mode, there is not a deployment and therefore no custom_metrics
            return

        payload = self.add_aggregate_metrics_to_payload({"buckets": individual_metrics})
        self.upload_custom_metrics(payload)

    def run_model_score(
        self, input_df: pd.DataFrame, model, drum_score_fn, **kwargs
    ) -> pd.DataFrame:
        """
        A wrapper to execute vdb's `score` method.  Wrapper is useful to calculate the
        latency of the `score` method and handle any exceptional conditions
        Returns:
            predictions_df: DataFrame obtained as a return value from user's `score`
                method
        """
        start_time = time.time()

        try:
            predictions_df = drum_score_fn(input_df, model, **kwargs)
        except Exception as e:
            title = "Failed to execute vdb score function"
            message = f"Exception: {e}"
            self._logger.error(title + " " + message)
            pd.set_option("display.max_columns", None)
            self._logger.error(input_df)
            self.send_event_sync(
                title, message, ModerationEventTypes.MODERATION_MODEL_SCORING_ERROR
            )
            raise

        score_latency = time.time() - start_time
        self.record_score_latency(score_latency)
        return predictions_df

    def score(self, data: pd.DataFrame, model, drum_score_fn, **kwargs):
        """
        Run on each prediction, and takes care of running the "score" function as well
        as collecting the metrics.
        """
        self._logger.debug(data)

        # clear/allocate memory for reporting metrics
        self.get_new_metrics_payload()

        # add the association-id if not present
        association_id_column_name = self.get_association_id_column_name()
        if (
            association_id_column_name
            and association_id_column_name not in data.columns
            and self.auto_generate_association_ids
        ):
            data[association_id_column_name] = self.generate_association_ids(len(data))

        # NOTE: no "pre-score" calculation on the DataFrame for the predictions

        # perform the main "score" function for this model
        predictions_df = self.run_model_score(data, model, drum_score_fn, **kwargs)

        # make sure association ids get copied over
        if (
            association_id_column_name
            and association_id_column_name not in predictions_df.columns
            and association_id_column_name in data.columns
        ):
            predictions_df[association_id_column_name] = data[association_id_column_name]

        # loop through all the metrics scoring with predictions_df that has citations
        association_ids = (
            []
            if association_id_column_name not in predictions_df.columns
            else predictions_df[association_id_column_name]
        )
        metric_reports = []
        for scorer in self.scorers():
            metric_info = self.custom_metric_map[scorer.name]
            if metric_info.get("requires_association_id", False) and len(association_ids):
                values = scorer.score_rows(predictions_df)
                if not values:
                    self.logger.debug(f"No {scorer} values found")
                    continue

                # assign back to the dataframe, so consumer has it
                predictions_df[scorer.name] = values
                metric_id = metric_info.get("id")
                for association_id, value in zip(association_ids, values):
                    metric_reports.append(
                        self.custom_metric_individual_payload(metric_id, value, association_id)
                    )
                continue

            value = scorer.score(predictions_df)
            self.record_aggregate_value(scorer.name, value)

        self.report_custom_metrics(metric_reports)
        return predictions_df
