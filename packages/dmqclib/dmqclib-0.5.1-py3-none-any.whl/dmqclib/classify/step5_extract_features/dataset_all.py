"""
This module defines the ExtractDataSetAll class, a specialized feature extraction
component for processing Copernicus CTD data. It extends the base feature
extraction capabilities provided by ExtractFeatureBase and integrates with a
configuration system for managing data paths and parameters.
"""

from typing import Optional, Dict

import polars as pl

from dmqclib.common.base.config_base import ConfigBase
from dmqclib.prepare.step5_extract_features.extract_base import ExtractFeatureBase


class ExtractDataSetAll(ExtractFeatureBase):
    """
    A subclass of :class:`ExtractFeatureBase` for extracting features
    from Copernicus CTD data.

    This class sets its :attr:`expected_class_name` to ``ExtractDataSetAll`` so
    that it matches the relevant YAML configuration. All feature extraction logic
    inherits from the parent class, :class:`ExtractFeatureBase`.
    """

    expected_class_name: str = "ExtractDataSetAll"

    def __init__(
        self,
        config: ConfigBase,
        input_data: Optional[pl.DataFrame] = None,
        selected_profiles: Optional[pl.DataFrame] = None,
        selected_rows: Optional[Dict[str, pl.DataFrame]] = None,
        summary_stats: Optional[pl.DataFrame] = None,
    ) -> None:
        """
        Initialize the feature extraction process for Copernicus CTD data.

        :param config: A configuration object that manages paths, target definitions,
                       and parameters for feature extraction.
        :type config: ConfigBase
        :param input_data: An optional Polars DataFrame containing the complete dataset
                           for feature extraction. If not provided at initialization,
                           it should be assigned later.
        :type input_data: Optional[pl.DataFrame]
        :param selected_profiles: An optional Polars DataFrame of selected profiles
                                  from earlier steps. If not provided, it should be
                                  assigned later.
        :type selected_profiles: Optional[pl.DataFrame]
        :param selected_rows: An optional dictionary mapping target names to respective
                            DataFrames containing the rows needed for feature generation.
                            If not provided, it should be assigned later.
        :type selected_rows: Optional[Dict[str, pl.DataFrame]]
        :param summary_stats: An optional Polars DataFrame with summary statistics,
                              potentially used for scaling or normalization.
                              If not provided, it should be assigned later.
        :type summary_stats: Optional[pl.DataFrame]
        """
        super().__init__(
            config=config,
            input_data=input_data,
            selected_profiles=selected_profiles,
            selected_rows=selected_rows,
            summary_stats=summary_stats,
        )

        #: Default file naming pattern when writing feature files for each target.
        self.default_file_name: str = (
            "extracted_features_classify_{target_name}.parquet"
        )

        #: Dictionary mapping target names to the corresponding Parquet file paths.
        self.output_file_names: Dict[str, str] = self.config.get_target_file_names(
            step_name="extract", default_file_name=self.default_file_name
        )

        #: Column names used for intermediate or reference purposes
        #: (e.g., linking positive and negative rows).
        self.drop_col_names = [
            "profile_id",
            "pair_id",
        ]
