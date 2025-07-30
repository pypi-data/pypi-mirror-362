"""
This module defines the ExtractDataSetA class, a specialized feature extraction class
for Copernicus CTD data. It extends ExtractFeatureBase to implement
specific data processing and feature generation steps for this dataset,
integrating with the dmqclib framework's configuration and data flow.
"""

from typing import Optional, Dict

import polars as pl

from dmqclib.common.base.config_base import ConfigBase
from dmqclib.prepare.step5_extract_features.extract_base import ExtractFeatureBase


class ExtractDataSetA(ExtractFeatureBase):
    """
    A subclass of :class:`ExtractFeatureBase` designed to extract features
    specifically from Copernicus CTD data.

    This class sets its :attr:`expected_class_name` to ``"ExtractDataSetA"``,
    ensuring it is recognized in the YAML configuration as a valid
    extract class within the dmqclib framework. It inherits the full
    feature extraction pipeline and lifecycle management from its base class,
    :class:`ExtractFeatureBase`.
    """

    expected_class_name: str = "ExtractDataSetA"

    def __init__(
        self,
        config: ConfigBase,
        input_data: Optional[pl.DataFrame] = None,
        selected_profiles: Optional[pl.DataFrame] = None,
        selected_rows: Optional[Dict[str, pl.DataFrame]] = None,
        summary_stats: Optional[pl.DataFrame] = None,
    ) -> None:
        """
        Initializes the feature extraction workflow for Copernicus CTD data.

        This constructor sets up the necessary data and configuration for the
        feature extraction process, leveraging the capabilities of the base class.

        :param config: A dataset configuration object that manages paths,
                       target definitions, and parameters for feature extraction.
        :type config: :class:`~dmqclib.common.base.config_base.ConfigBase`
        :param input_data: An optional Polars DataFrame containing all available data
                           for feature extraction. This typically represents the full dataset
                           pre-processed in earlier steps. Defaults to None.
        :type input_data: :class:`polars.DataFrame` or None
        :param selected_profiles: An optional Polars DataFrame containing specifically-selected
                                  profiles from earlier data preparation steps. This subset
                                  is used to focus feature generation on relevant profiles.
                                  Defaults to None.
        :type selected_profiles: :class:`polars.DataFrame` or None
        :param selected_rows: An optional dictionary mapping each target (str) to its respective
                            subset of rows (:class:`polars.DataFrame`) for feature generation.
                            This allows for target-specific feature extraction.
                            Defaults to None.
        :type selected_rows: Dict[str, :class:`polars.DataFrame`] or None
        :param summary_stats: An optional Polars DataFrame with summary statistics
                              (e.g., mean, standard deviation) that may guide scaling
                              or normalization of features. Defaults to None.
        :type summary_stats: :class:`polars.DataFrame` or None
        """
        super().__init__(
            config=config,
            input_data=input_data,
            selected_profiles=selected_profiles,
            selected_rows=selected_rows,
            summary_stats=summary_stats,
        )
