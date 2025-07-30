"""
This module defines the ProfileSummaryStats5 class, a specialized feature
extraction component for combining row references with summary statistics
from Polars DataFrames. It is designed to extract, transform, and optionally
scale statistical features based on pre-computed summary data.
"""

from typing import Optional, Dict

import polars as pl

from dmqclib.common.base.feature_base import FeatureBase


class ProfileSummaryStats5(FeatureBase):
    """
    A feature-extraction class that combines row references from
    :attr:`selected_rows` with summary statistics from :attr:`summary_stats`.
    It constructs columns of summarized metrics (e.g., min, max) for specified
    variables and optionally applies scaling.

    This class inherits from :class:`FeatureBase`, which provides a
    generic framework for feature extraction, including placeholders
    for multi-stage scaling.
    """

    def __init__(
        self,
        target_name: Optional[str] = None,
        feature_info: Optional[Dict] = None,
        selected_profiles: Optional[pl.DataFrame] = None,
        filtered_input: Optional[pl.DataFrame] = None,
        selected_rows: Optional[Dict[str, pl.DataFrame]] = None,
        summary_stats: Optional[pl.DataFrame] = None,
    ) -> None:
        """
        Initialize the profile summary stats feature extractor.

        :param target_name: The name of the target used to lookup
                            corresponding rows in :attr:`selected_rows`.
        :type target_name: Optional[str]
        :param feature_info: A dictionary specifying
                             feature parameters and stats.

                             Example structure:
                             .. code-block:: python

                                {
                                  "stats": {
                                    "temp": {
                                      "min": {
                                        "min": 0.0,
                                        "max": 30.0
                                      },
                                      "mean": {
                                        "min": 0.0,
                                        "max": 30.0
                                      }
                                      # ...
                                    },
                                    "psal": {
                                      # ...
                                    }
                                  }
                                }
        :type feature_info: Optional[Dict]
        :param selected_profiles: A Polars DataFrame of selected profiles,
                                  typically unused by this class but provided
                                  for consistency.
        :type selected_profiles: Optional[pl.DataFrame]
        :param filtered_input: A Polars DataFrame of potentially filtered input data,
                               not directly used here.
        :type filtered_input: Optional[pl.DataFrame]
        :param selected_rows: A dictionary of DataFrames keyed by target names,
                              containing rows for which features are extracted.
        :type selected_rows: Optional[Dict[str, pl.DataFrame]]
        :param summary_stats: A Polars DataFrame of summary statistics
                              keyed by (platform_code, profile_no, variable).
        :type summary_stats: Optional[pl.DataFrame]
        """
        super().__init__(
            target_name=target_name,
            feature_info=feature_info,
            selected_profiles=selected_profiles,
            filtered_input=filtered_input,
            selected_rows=selected_rows,
            summary_stats=summary_stats,
        )

    def extract_features(self) -> None:
        """
        Traverse the :attr:`feature_info["stats"]` structure to assemble
        columns from :attr:`summary_stats`, merging them into :attr:`features`.

        Steps:

          1. :meth:`_filter_selected_rows_cols` - initialize :attr:`features` by selecting
             base columns (row_id, platform_code, profile_no).
          2. For each top-level key and subkey in :attr:`feature_info["stats"]`,
             call :meth:`_extract_single_summary` to join in the corresponding
             metric from :attr:`summary_stats`.
          3. Drop columns (platform_code, profile_no) that are no longer needed in
             the final feature set.
        """
        self._filter_selected_rows_cols()

        variables_and_metrics = [
            (variable_name, metric_name)
            for variable_name, variable_stats in self.feature_info["stats"].items()
            for metric_name in variable_stats.keys()
        ]
        for variable_name, metric_name in variables_and_metrics:
            self._extract_single_summary(variable_name, metric_name)

        self.features = self.features.drop(["platform_code", "profile_no"])

    def _filter_selected_rows_cols(self) -> None:
        """
        Initialize :attr:`features` by selecting the essential columns
        from :attr:`selected_rows[target_name]`.
        """
        self.features = self.selected_rows[self.target_name].select(
            ["row_id", "platform_code", "profile_no"]
        )

    def _extract_single_summary(self, variable_name: str, metric_name: str) -> None:
        """
        Join a single summary statistic (e.g., min, mean, max) from :attr:`summary_stats`
        onto :attr:`features`.

        :param variable_name: The variable category key (e.g., "temp", "psal") in
                              :attr:`summary_stats`. This was previously named `target_name`.
        :type variable_name: str
        :param metric_name: The specific metric key (e.g., "min", "mean", "max")
                            under the variable category. This was previously named `var_name`.
        :type metric_name: str
        """
        self.features = self.features.join(
            self.summary_stats.filter(pl.col("variable") == variable_name).select(
                pl.col("platform_code"),
                pl.col("profile_no"),
                pl.col(metric_name).alias(f"{variable_name}_{metric_name}"),
            ),
            on=["platform_code", "profile_no"],
            maintain_order="left",
        )

    def scale_first(self) -> None:
        """
        An initial scaling hook (unimplemented).

        Subclasses or calling code can override or extend this method
        to perform additional transformations before stats-based feature joins.
        """
        pass  # pragma: no cover

    def scale_second(self) -> None:
        """
        Min-max scale the newly joined summary statistics.

        For each top-level key (e.g., "temp") and subkey (e.g., "mean") in
        :attr:`feature_info["stats"]`, transform the combined column
        named "temp_mean" or "temp_min" etc. according to specified
        min and max.
        """
        columns_to_add = [
            (
                (pl.col(f"{col_name}_{stat_name}") - scale_info["min"])
                / (scale_info["max"] - scale_info["min"])
            ).alias(f"{col_name}_{stat_name}")
            for col_name, variable_stats in self.feature_info["stats"].items()
            for stat_name, scale_info in variable_stats.items()
        ]

        self.features = self.features.with_columns(columns_to_add)
