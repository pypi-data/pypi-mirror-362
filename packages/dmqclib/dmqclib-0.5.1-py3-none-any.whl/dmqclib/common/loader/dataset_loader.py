"""
This module provides factory functions for loading and instantiating various dataset
preparation steps within the dmqclib library. It uses a configuration object to
determine the specific class to load for each step (e.g., input, summary, select)
and retrieves it from a central registry.

Functions within this module facilitate the dynamic creation of dataset
preparation objects based on predefined configurations, enabling a flexible
and extensible data processing pipeline.
"""

from typing import Dict, Optional, Type

import polars as pl

from dmqclib.common.base.dataset_base import DataSetBase
from dmqclib.common.config.dataset_config import DataSetConfig
from dmqclib.common.loader.dataset_registry import (
    EXTRACT_DATASET_REGISTRY,
    INPUT_DATASET_REGISTRY,
    LOCATE_DATASET_REGISTRY,
    SELECT_DATASET_REGISTRY,
    SPLIT_DATASET_REGISTRY,
    SUMMARY_DATASET_REGISTRY,
)
from dmqclib.prepare.step1_read_input.input_base import InputDataSetBase
from dmqclib.prepare.step2_calc_stats.summary_base import SummaryStatsBase
from dmqclib.prepare.step3_select_profiles.select_base import ProfileSelectionBase
from dmqclib.prepare.step4_select_rows.locate_base import LocatePositionBase
from dmqclib.prepare.step5_extract_features.extract_base import ExtractFeatureBase
from dmqclib.prepare.step6_split_dataset.split_base import SplitDataSetBase


def _get_prepare_class(
    config: DataSetConfig, step: str, registry: Dict[str, Type[DataSetBase]]
) -> Type[DataSetBase]:
    """
    Retrieve the class constructor from the specified registry for a given step.

    1. Obtain the class name by calling :meth:`DataSetConfig.get_base_class(step)`.
    2. Look up the class in the provided registry using the extracted name.
    3. Return the class (not an instantiated object).

    :param config: A dataset configuration object that determines the base class name
                   under a specific ``step``.
    :type config: :class:`~dmqclib.common.config.dataset_config.DataSetConfig`
    :param step: The step name (e.g., "input", "summary", "select") in the YAML config.
    :type step: str
    :param registry: A dictionary mapping class names (str) to class types inheriting
                     from :class:`~dmqclib.common.base.dataset_base.DataSetBase`.
    :type registry: Dict[str, Type[DataSetBase]]
    :raises ValueError: If the class name from the config is not found in ``registry``.
    :return: The class constructor corresponding to the requested step.
    :rtype: Type[:class:`~dmqclib.common.base.dataset_base.DataSetBase`]
    """
    class_name = config.get_base_class(step)
    dataset_class = registry.get(class_name)
    if not dataset_class:
        raise ValueError(f"Unknown dataset class specified: {class_name}")

    return dataset_class


def load_step1_input_dataset(config: DataSetConfig) -> InputDataSetBase:
    """
    Load an :class:`~dmqclib.prepare.step1_read_input.input_base.InputDataSetBase`-derived class
    based on the configuration.

    Uses the subclass name retrieved from YAML via ``config.get_base_class("input")``
    to fetch the correct class from :data:`INPUT_DATASET_REGISTRY`, then instantiates it.

    :param config: The dataset configuration object, which includes a ``base_class``
                   field under the "input" step in the YAML.
    :type config: :class:`~dmqclib.common.config.dataset_config.DataSetConfig`
    :return: An instantiated object that inherits from
             :class:`~dmqclib.prepare.step1_read_input.input_base.InputDataSetBase`.
    :rtype: :class:`~dmqclib.prepare.step1_read_input.input_base.InputDataSetBase`
    """
    dataset_class = _get_prepare_class(config, "input", INPUT_DATASET_REGISTRY)
    return dataset_class(config)


def load_step2_summary_dataset(
    config: DataSetConfig, input_data: Optional[pl.DataFrame] = None
) -> SummaryStatsBase:
    """
    Load a :class:`~dmqclib.prepare.step2_calc_stats.summary_base.SummaryStatsBase`-derived class
    based on the configuration.

    Uses the subclass name retrieved from YAML via ``config.get_base_class("summary")``
    to fetch the correct class from :data:`SUMMARY_DATASET_REGISTRY`, then instantiates it.

    :param config: The dataset configuration object, referencing the "summary" step.
    :type config: :class:`~dmqclib.common.config.dataset_config.DataSetConfig`
    :param input_data: A Polars DataFrame from which summary stats can be computed,
                       defaults to None.
    :type input_data: Optional[:class:`polars.DataFrame`]
    :return: An instantiated object that inherits from
             :class:`~dmqclib.prepare.step2_calc_stats.summary_base.SummaryStatsBase`.
    :rtype: :class:`~dmqclib.prepare.step2_calc_stats.summary_base.SummaryStatsBase`
    """
    dataset_class = _get_prepare_class(config, "summary", SUMMARY_DATASET_REGISTRY)
    return dataset_class(config, input_data=input_data)


def load_step3_select_dataset(
    config: DataSetConfig, input_data: Optional[pl.DataFrame] = None
) -> ProfileSelectionBase:
    """
    Load a :class:`~dmqclib.prepare.step3_select_profiles.select_base.ProfileSelectionBase`-derived
    class based on the configuration.

    Uses the subclass name retrieved from YAML via ``config.get_base_class("select")``
    to fetch the correct class from :data:`SELECT_DATASET_REGISTRY`, then instantiates it.

    :param config: The dataset configuration object, referencing the "select" step.
    :type config: :class:`~dmqclib.common.config.dataset_config.DataSetConfig`
    :param input_data: A Polars DataFrame from which profiles can be selected, defaults to None.
    :type input_data: Optional[:class:`polars.DataFrame`]
    :return: An instantiated object that inherits from
             :class:`~dmqclib.prepare.step3_select_profiles.select_base.ProfileSelectionBase`.
    :rtype: :class:`~dmqclib.prepare.step3_select_profiles.select_base.ProfileSelectionBase`
    """
    dataset_class = _get_prepare_class(config, "select", SELECT_DATASET_REGISTRY)
    return dataset_class(config, input_data=input_data)


def load_step4_locate_dataset(
    config: DataSetConfig,
    input_data: Optional[pl.DataFrame] = None,
    selected_profiles: Optional[pl.DataFrame] = None,
) -> LocatePositionBase:
    """
    Load a :class:`~dmqclib.prepare.step4_select_rows.locate_base.LocatePositionBase`-derived class
    based on the configuration.

    Uses the subclass name retrieved from YAML via ``config.get_base_class("locate")``
    to fetch the correct class from :data:`LOCATE_DATASET_REGISTRY`, then instantiates it.

    :param config: The dataset configuration object, referencing the "locate" step.
    :type config: :class:`~dmqclib.common.config.dataset_config.DataSetConfig`
    :param input_data: A Polars DataFrame containing data from which locations can be derived,
                       defaults to None.
    :type input_data: Optional[:class:`polars.DataFrame`]
    :param selected_profiles: A Polars DataFrame representing pre-selected profiles,
                              defaults to None.
    :type selected_profiles: Optional[:class:`polars.DataFrame`]
    :return: An instantiated object that inherits from
             :class:`~dmqclib.prepare.step4_select_rows.locate_base.LocatePositionBase`.
    :rtype: :class:`~dmqclib.prepare.step4_select_rows.locate_base.LocatePositionBase`
    """
    dataset_class = _get_prepare_class(config, "locate", LOCATE_DATASET_REGISTRY)
    return dataset_class(
        config,
        input_data=input_data,
        selected_profiles=selected_profiles,
    )


def load_step5_extract_dataset(
    config: DataSetConfig,
    input_data: Optional[pl.DataFrame] = None,
    selected_profiles: Optional[pl.DataFrame] = None,
    selected_rows: Optional[Dict[str, pl.DataFrame]] = None,
    summary_stats: Optional[pl.DataFrame] = None,
) -> ExtractFeatureBase:
    """
    Load a :class:`~dmqclib.prepare.step5_extract_features.extract_base.ExtractFeatureBase`-derived
    class based on the configuration.

    Uses the subclass name retrieved from YAML via ``config.get_base_class("extract")``
    to fetch the correct class from :data:`EXTRACT_DATASET_REGISTRY`, then instantiates it.

    :param config: The dataset configuration object, referencing the "extract" step.
    :type config: :class:`~dmqclib.common.config.dataset_config.DataSetConfig`
    :param input_data: An optional Polars DataFrame containing data for extraction steps.
    :type input_data: Optional[:class:`polars.DataFrame`]
    :param selected_profiles: A Polars DataFrame of selected profiles, if applicable.
    :type selected_profiles: Optional[:class:`polars.DataFrame`]
    :param selected_rows: A dictionary mapping target names (str) to Polars DataFrames
                          of rows to be processed. Defaults to None.
    :type selected_rows: Optional[Dict[str, :class:`polars.DataFrame`]]
    :param summary_stats: A Polars DataFrame containing summary stats for scaling or references.
    :type summary_stats: Optional[:class:`polars.DataFrame`]
    :return: An instantiated object that inherits from
             :class:`~dmqclib.prepare.step5_extract_features.extract_base.ExtractFeatureBase`.
    :rtype: :class:`~dmqclib.prepare.step5_extract_features.extract_base.ExtractFeatureBase`
    """
    dataset_class = _get_prepare_class(config, "extract", EXTRACT_DATASET_REGISTRY)
    return dataset_class(
        config,
        input_data=input_data,
        selected_profiles=selected_profiles,
        selected_rows=selected_rows,
        summary_stats=summary_stats,
    )


def load_step6_split_dataset(
    config: DataSetConfig, target_features: Optional[Dict[str, pl.DataFrame]] = None
) -> SplitDataSetBase:
    """
    Load a :class:`~dmqclib.prepare.step6_split_dataset.split_base.SplitDataSetBase`-derived class
    based on the configuration.

    Uses the subclass name retrieved from YAML via ``config.get_base_class("split")``
    to fetch the correct class from :data:`SPLIT_DATASET_REGISTRY`, then instantiates it.

    :param config: The dataset configuration object, referencing the "split" step.
    :type config: :class:`~dmqclib.common.config.dataset_config.DataSetConfig`
    :param target_features: A dictionary mapping target names (str) to Polars DataFrames
                            containing features to be split into train/test sets or folds.
                            Defaults to None.
    :type target_features: Optional[Dict[str, :class:`polars.DataFrame`]]
    :return: An instantiated object that inherits from
             :class:`~dmqclib.prepare.step6_split_dataset.split_base.SplitDataSetBase`.
    :rtype: :class:`~dmqclib.prepare.step6_split_dataset.split_base.SplitDataSetBase`
    """
    dataset_class = _get_prepare_class(config, "split", SPLIT_DATASET_REGISTRY)
    return dataset_class(
        config,
        target_features=target_features,
    )
