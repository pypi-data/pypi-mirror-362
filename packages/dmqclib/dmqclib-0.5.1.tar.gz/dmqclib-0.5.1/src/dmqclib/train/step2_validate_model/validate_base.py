"""
This module defines the :class:`ValidationBase` abstract base class, providing
a foundational framework for validating trained machine learning models.

It integrates with the ``dmqclib`` library's configuration and data handling
mechanisms, enabling robust and standardized validation routines across
different model types and datasets. Subclasses are expected to implement
the specific validation logic tailored to their model and data.
"""

import os
from abc import abstractmethod
from typing import Optional, Dict, List

import polars as pl

from dmqclib.common.base.config_base import ConfigBase
from dmqclib.common.base.dataset_base import DataSetBase
from dmqclib.common.loader.model_loader import load_model_class


class ValidationBase(DataSetBase):
    """
    An abstract base class that provides a framework for validating
    trained model(s) using a specified training set. Inherits from
    :class:`DataSetBase` to leverage YAML-based configuration checks
    and the step name ``"validate"``.

    .. note::

       If this class is to be instantiated directly (rather than a subclass),
       you may need to define an ``expected_class_name`` attribute. Otherwise,
       :class:`DataSetBase` may raise a :class:`NotImplementedError` if the
       YAML's ``base_class`` does not match.
    """

    def __init__(
        self,
        config: ConfigBase,
        training_sets: Optional[Dict[str, pl.DataFrame]] = None,
    ) -> None:
        """
        Initialize the validation base class with a training configuration
        and optional training sets.

        :param config: A training configuration object containing
                       paths, target definitions, and model parameters.
        :type config: :class:`dmqclib.common.base.config_base.ConfigBase`
        :param training_sets: A dictionary of Polars DataFrames where keys
                              are target names and values are the corresponding
                              training data, or None if no training sets are provided.
        :type training_sets: Optional[Dict[str, polars.DataFrame]]
        :raises NotImplementedError: If a subclass does not define
                                     ``expected_class_name`` and is instantiated
                                     with a YAML config specifying
                                     ``base_class``, and they do not match.
        :raises ValueError: If the YAML's ``base_class`` does not match the
                            ``expected_class_name`` for a subclass.
        """
        super().__init__(step_name="validate", config=config)

        #: Default file naming pattern for validation reports.
        self.default_file_names: Dict[str, str] = {
            "report": "validation_report_{target_name}.tsv",
        }

        #: A dictionary mapping "result" to a dictionary of target-specific file paths.
        self.output_file_names: Dict[str, Dict[str, str]] = {
            k: self.config.get_target_file_names(
                step_name="validate", default_file_name=v
            )
            for k, v in self.default_file_names.items()
        }

        #: Optional Polars DataFrame with training sets
        #: (or dictionary if the structure is aggregated).
        self.training_sets: Optional[Dict[str, pl.DataFrame]] = training_sets

        #: Base model class instantiated through the model loader.
        self.base_model = None
        self.load_base_model()

        #: Subclasses or the validation routine can store specialized model instances here.
        self.models: Dict[str, List] = {}

        #: A dictionary mapping each target name to a Polars DataFrame
        #: of validation reports (e.g., predictions, metrics).
        self.reports: Dict[str, pl.DataFrame] = {}

        #: A dictionary for storing any summarised metrics derived from :attr:`reports`.
        self.summarised_reports: Dict[str, pl.DataFrame] = {}

    def load_base_model(self) -> None:
        """
        Load the primary model class specified in the training configuration.

        The loaded model class is stored in :attr:`base_model`
        and can be used or extended in the subclass's validation routines.
        """
        self.base_model = load_model_class(self.config)

    def process_targets(self) -> None:
        """
        Iterate over the target names defined in :attr:`config` and validate
        each using :meth:`validate`.
        """
        for target_name in self.config.get_target_names():
            self.validate(target_name)

    @abstractmethod
    def validate(self, target_name: str) -> None:
        """
        An abstract method for validating one or more models on a specific target.

        Subclasses must implement the logic to use :attr:`training_sets`
        (and possibly :attr:`base_model` or :attr:`models`)
        to evaluate performance, store metrics in :attr:`reports`, etc.

        :param target_name: The key identifying which target to validate.
        :type target_name: str
        """
        pass  # pragma: no cover

    def write_reports(self) -> None:
        """
        Write the validation results stored in :attr:`reports` to TSV files.

        Each target's report DataFrame is written to a file specified by
        :attr:`output_file_names`. Directories are created if they do not exist.

        :raises ValueError: If :attr:`reports` is empty, indicating no validation
                            results are available to write.
        """
        if not self.reports:
            raise ValueError("Member variable 'reports' must not be empty.")

        for target_name, df in self.reports.items():
            output_path = self.output_file_names["report"][target_name]
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.write_csv(output_path, separator="\t")
