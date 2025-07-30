"""
Provides an abstract base class, :class:`BuildModelBase`, for building and testing
machine learning models using structured training and test datasets.

This module establishes a framework for model development within a larger
data quality control (DMQC) system, integrating with configuration management
and model loading utilities. Subclasses are expected to implement specific
model building and testing logic tailored to different modeling paradigms or
frameworks.
"""

import os
from abc import abstractmethod
from typing import Optional, Dict

import polars as pl

from dmqclib.common.base.config_base import ConfigBase
from dmqclib.common.base.dataset_base import DataSetBase
from dmqclib.common.base.model_base import ModelBase
from dmqclib.common.loader.model_loader import load_model_class


class BuildModelBase(DataSetBase):
    """
    An abstract base class to build and test models, using training/test sets
    and a YAML-based configuration.

    Inherits from :class:`DataSetBase` (with step name ``"build"``)
    to ensure that the provided configuration matches the expected
    fields for model-building. Subclasses must define their own
    logic in the :meth:`build` and :meth:`test` abstract methods,
    potentially for different modeling frameworks.

    .. note::

       If you intend to instantiate this class directly (rather than a subclass),
       you may need to define an ``expected_class_name`` that matches
       the config's ``base_class`` property. Otherwise, a
       :class:`NotImplementedError` may be raised.
    """

    def __init__(
        self,
        config: ConfigBase,
        training_sets: Optional[Dict[str, pl.DataFrame]] = None,
        test_sets: Optional[Dict[str, pl.DataFrame]] = None,
        step_name: str = "build",
    ) -> None:
        """
        Initialize the model-building base class with optional training
        and test sets.

        :param config: A training configuration object containing
                       paths and parameters for building and testing models.
        :type config: ConfigBase
        :param training_sets: A dictionary of Polars DataFrames, where keys are target
                              names and values are DataFrames with training examples
                              for that target. Defaults to None.
        :type training_sets: Optional[Dict[str, pl.DataFrame]]
        :param test_sets: A dictionary of Polars DataFrames, where keys are target
                          names and values are DataFrames with testing examples
                          for that target. Defaults to None.
        :type test_sets: Optional[Dict[str, pl.DataFrame]]
        :param step_name: The name of the current processing step,
                          defaults to "build".
        :type step_name: str
        """
        super().__init__(step_name=step_name, config=config)

        #: Default names for model files and test reports,
        #: with placeholders for the target name.
        self.default_file_names: Dict[str, str] = {
            "report": "test_report_{target_name}.tsv",
            "prediction": "test_prediction_{target_name}.parquet",
        }
        self.default_model_file_name: str = "model_{target_name}.joblib"

        #: A dictionary mapping "model" or "result" to
        #: target-specific file paths.
        self.output_file_names: Dict[str, Dict[str, str]] = {
            k: self.config.get_target_file_names(step_name="build", default_file_name=v)
            for k, v in self.default_file_names.items()
        }

        #: A dictionary mapping "model" to target-specific file paths.
        self.model_file_names: Dict[str, str] = self.config.get_target_file_names(
            "model", self.default_model_file_name
        )

        #: A Polars DataFrame (or dictionary) containing training data.
        self.training_sets: Optional[Dict[str, pl.DataFrame]] = training_sets
        #: A Polars DataFrame (or dictionary) containing test data.
        self.test_sets: Optional[Dict[str, pl.DataFrame]] = test_sets

        #: Loaded from :meth:`load_base_model`; can be overridden for each target.
        self.base_model: Optional[ModelBase] = None
        self.load_base_model()

        #: A dictionary to store model objects keyed by target name.
        self.models: Dict[str, Optional[ModelBase]] = {}
        #: A dictionary to store test results keyed by target name.
        self.reports: Dict[str, pl.DataFrame] = {}
        #: A dictionary to store predictions results keyed by target name.
        self.predictions: Dict[str, pl.DataFrame] = {}

    def load_base_model(self) -> None:
        """
        Load the base model class from the configuration.

        The loaded model is stored in :attr:`base_model` and may be cloned,
        specialized, or reloaded for each target in the building process.
        """
        self.base_model = load_model_class(self.config)

    def build_targets(self) -> None:
        """
        Iterate over all targets from the configuration, calling :meth:`build`
        for each, and then optionally calling :meth:`test` if test sets exist.
        """
        for target_name in self.config.get_target_names():
            self.build(target_name)
            if self.test_sets is not None and target_name in self.test_sets:
                self.test(target_name)

    def test_targets(self) -> None:
        """
        Iterate over all targets, ensuring that a model has been built before
        calling :meth:`test`.

        :raises ValueError: If a target has no corresponding entry in
                            :attr:`models`.
        """
        for target_name in self.config.get_target_names():
            if target_name not in self.models:
                raise ValueError(
                    f"No valid model found for the variable '{target_name}'."
                )
            self.test(target_name)

    @abstractmethod
    def build(self, target_name: str) -> None:
        """
        Build a model for the specified target name.

        This abstract method must be implemented by subclasses to
        perform the steps necessary for initializing, training,
        and storing the model in :attr:`models`.

        :param target_name: The identifier for this target's model
                            in :attr:`training_sets`.
        :type target_name: str
        """
        pass  # pragma: no cover

    @abstractmethod
    def test(self, target_name: str) -> None:
        """
        Test a model for the specified target name.

        Typically, this includes running predictions, evaluating
        performance metrics, and storing results in :attr:`reports`.

        :param target_name: The identifier for this target's model
                            and test set in :attr:`test_sets` (plus
                            entries in :attr:`models`).
        :type target_name: str
        """
        pass  # pragma: no cover

    def write_reports(self) -> None:
        """
        Write each target's test reports to a TSV file.

        :raises ValueError: If :attr:`reports` is empty, indicating no tests
                            have been carried out or no reports stored.
        """
        if not self.reports:
            raise ValueError("Member variable 'reports' must not be empty.")

        for target_name, df in self.reports.items():
            output_path = self.output_file_names["report"][target_name]
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.write_csv(output_path, separator="\t")

    def write_models(self) -> None:
        """
        Serialize and write each target's model to disk.

        :raises ValueError: If :attr:`models` is empty, indicating no models
                            have been built for writing.
        """
        if not self.models:
            raise ValueError("Member variable 'models' must not be empty.")

        for target_name, model_ref in self.models.items():
            output_path = self.model_file_names[target_name]
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            if model_ref:
                model_ref.save_model(output_path)

    def read_models(self) -> None:
        """
        Read and restore each target's model from disk, storing
        the loaded model in :attr:`models`.

        :raises FileNotFoundError: If a model file does not exist
                                   for a particular target.
        """
        for target_name, path in self.model_file_names.items():
            if not os.path.exists(path):
                raise FileNotFoundError(f"File '{path}' does not exist.")

            new_model_instance = load_model_class(self.config)
            new_model_instance.load_model(path)
            self.models[target_name] = new_model_instance

    def write_predictions(self) -> None:
        """
        Serialize and write each target's predictions to disk.

        :raises ValueError: If :attr:`predictions` is empty, indicating no predictions
                            have been built for writing.
        """
        if not self.predictions:
            raise ValueError("Member variable 'predictions' must not be empty.")

        for target_name, df in self.predictions.items():
            output_path = self.output_file_names["prediction"][target_name]
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.write_parquet(output_path)
