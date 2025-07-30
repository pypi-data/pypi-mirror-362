"""
Module orchestrating a training-and-evaluation workflow for the configured dataset.
Each step is dynamically loaded based on the configuration provided.
"""

from dmqclib.common.base.config_base import ConfigBase
from dmqclib.common.loader.training_loader import (
    load_step1_input_training_set,
    load_step2_model_validation_class,
    load_step4_build_model_class,
)


def train_and_evaluate(config: ConfigBase) -> None:
    """
    Perform a training and evaluation process based on the specified configuration.

    This function orchestrates the end-to-end workflow, including data loading,
    model validation, and final model building and testing.

    Steps:

      1. Load and process input training data.
      2. Validate the model using the specified validation technique (e.g., k-fold).
      3. Build and test the final model, saving results and trained model artifacts.

    :param config:
        A training configuration object derived from :class:`ConfigBase`.
        Specifies which classes and parameters to use at each step
        (input, model validation, and model building).
    :type config: ConfigBase
    :returns:
        None. The function performs I/O operations and does not return a value.
    :rtype: None

    :raises SomeSpecificError: If a configuration parameter is invalid or a step fails.
        (Example: Add specific exceptions if known to be raised).

    Example Usage:
      >>> from dmqclib.common.base.config_base import ConfigBase
      >>> # Assuming cfg is an initialized ConfigBase object
      >>> cfg = ConfigBase(...)
      >>> train_and_evaluate(cfg)
    """
    ds_input = load_step1_input_training_set(config)
    ds_input.process_targets()

    ds_valid = load_step2_model_validation_class(config, ds_input.training_sets)
    ds_valid.process_targets()
    ds_valid.write_reports()

    ds_build = load_step4_build_model_class(
        config, ds_input.training_sets, ds_input.test_sets
    )
    ds_build.build_targets()
    ds_build.test_targets()
    ds_build.write_reports()
    ds_build.write_models()
