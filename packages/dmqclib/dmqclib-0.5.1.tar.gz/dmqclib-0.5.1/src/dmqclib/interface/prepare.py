"""
This module orchestrates the creation of a training dataset by sequentially
loading and processing data through multiple preparation steps.

It defines the `create_training_dataset` function, which acts as the main
entry point for initiating the multi-stage data pipeline, from raw input
to final training and validation datasets.
"""

from dmqclib.common.base.config_base import ConfigBase
from dmqclib.common.loader.dataset_loader import load_step1_input_dataset
from dmqclib.common.loader.dataset_loader import load_step2_summary_dataset
from dmqclib.common.loader.dataset_loader import load_step3_select_dataset
from dmqclib.common.loader.dataset_loader import load_step4_locate_dataset
from dmqclib.common.loader.dataset_loader import load_step5_extract_dataset
from dmqclib.common.loader.dataset_loader import load_step6_split_dataset


def create_training_dataset(config: ConfigBase) -> None:
    """
    Execute a series of steps to produce a training dataset.

    This function orchestrates the sequential loading and processing of data
    through multiple preparation steps, as defined by the provided configuration
    object. It relies on a series of helper functions (e.g., ``load_stepX_dataset``)
    and class methods to perform distinct operations, ultimately generating
    and writing the final training and validation datasets.

    The processing typically involves the following stages:

    1.  **Input Data Loading:** Reads and prepares the initial raw data.
    2.  **Summary Statistics Calculation:** Computes and stores aggregate
        statistics from the input data.
    3.  **Profile Selection:** Identifies and labels specific profiles or
        data subsets based on criteria.
    4.  **Target Row Location:** Pinpoints and extracts specific rows of interest
        within the selected profiles.
    5.  **Feature Extraction:** Derives and extracts relevant features for
        modeling from the located target rows, often incorporating summary
        statistics.
    6.  **Dataset Splitting:** Divides the extracted features into training
        and validation sets.

    :param config: A configuration object specifying the classes and parameters
                   for each step in the dataset preparation process. This object
                   guides how each data loading and processing step is performed.
    :type config: dmqclib.common.base.config_base.ConfigBase
    :return: None. This function performs I/O operations (reading input, writing
             intermediate and final datasets) and does not return any value.
    :rtype: None

    :Example:

    .. code-block:: python

        from dmqclib.common.base.config_base import ConfigBase
        # Assume cfg is an initialized ConfigBase instance
        cfg = ConfigBase(...)
        create_training_dataset(cfg)
    """
    ds_input = load_step1_input_dataset(config)
    ds_input.read_input_data()

    ds_summary = load_step2_summary_dataset(config, ds_input.input_data)
    ds_summary.calculate_stats()
    ds_summary.write_summary_stats()

    ds_select = load_step3_select_dataset(config, ds_input.input_data)
    ds_select.label_profiles()
    ds_select.write_selected_profiles()

    ds_locate = load_step4_locate_dataset(
        config, ds_input.input_data, ds_select.selected_profiles
    )
    ds_locate.process_targets()
    ds_locate.write_selected_rows()

    ds_extract = load_step5_extract_dataset(
        config,
        ds_input.input_data,
        ds_select.selected_profiles,
        ds_locate.selected_rows,
        ds_summary.summary_stats,
    )
    ds_extract.process_targets()
    ds_extract.write_target_features()

    ds_split = load_step6_split_dataset(config, ds_extract.target_features)
    ds_split.process_targets()
    ds_split.write_data_sets()
