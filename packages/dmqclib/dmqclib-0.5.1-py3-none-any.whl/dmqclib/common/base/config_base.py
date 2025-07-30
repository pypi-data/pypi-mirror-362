"""A base class for handling YAML-based configurations.

This module defines the `ConfigBase` abstract base class, which provides a
standardized interface for loading, validating, and accessing configuration
data from YAML files. It is designed to manage configurations for various
components of a data processing pipeline, such as datasets, training tasks,
and classification tasks.

The class centralizes configuration management by using JSON schema for
validation and providing structured methods for accessing configuration values,
ensuring consistency and reusability.
"""

import os
from abc import ABC
from typing import List, Dict, Optional

import jsonschema
import yaml
from jsonschema import validate

from dmqclib.common.config.yaml_schema import (
    get_data_set_config_schema,
    get_training_config_schema,
    get_classification_config_schema,
)
from dmqclib.common.config.yaml_templates import (
    get_config_data_set_template,
    get_config_train_set_template,
    get_config_classify_set_template,
)
from dmqclib.common.utils.config import get_config_item
from dmqclib.common.utils.config import read_config


class ConfigBase(ABC):
    """Abstract base class for loading and accessing YAML configurations.

    This class provides a common interface for handling configuration files.
    It supports loading from a file path or from a built-in template,
    validating the configuration against a predefined JSON schema, and
    providing convenient methods to access specific parts of the config.

    Subclasses must override the ``expected_class_name`` attribute to match
    the ``base_class`` value specified in the YAML configuration, which ensures
    that the correct configuration is used with the correct class.

    .. note::
       This is an abstract base class and should not be instantiated directly.

    :ivar expected_class_name: Must be overridden by subclasses to match the
                               YAML's ``base_class`` entry.
    :vartype expected_class_name: str, optional
    :ivar section_name: The top-level section of the config this instance manages
                        (e.g., "data_sets").
    :vartype section_name: str
    :ivar yaml_schema: The JSON schema used for validating the configuration.
    :vartype yaml_schema: dict
    :ivar full_config: The entire configuration loaded from the YAML file.
    :vartype full_config: dict
    :ivar valid_yaml: A boolean flag indicating if the loaded configuration
                      is valid against the schema.
    :vartype valid_yaml: bool
    :ivar data: The specific configuration dictionary for the selected dataset
                or task, populated after calling :meth:`select`.
    :vartype data: dict, optional
    :ivar dataset_name: The name of the selected dataset or task.
    :vartype dataset_name: str, optional
    """

    expected_class_name = None  # Must be overridden by child classes

    def __init__(
        self, section_name: str, config_file: str, auto_select: bool = False
    ) -> None:
        """Initialize the configuration object from a YAML file or template.

        This loads a YAML configuration, either from a specified file path or
        a predefined template string (e.g., "template:data_sets"), and
        prepares it for validation and use.

        :param section_name: The name of the configuration section to load,
                             e.g., "data_sets", "training_sets".
        :type section_name: str
        :param config_file: The path to the YAML configuration file or a
                            template identifier string (e.g., "template:data_sets").
        :type config_file: str
        :param auto_select: If ``True``, automatically validates the config and
                            attempts to select the single configuration entry
                            if only one is present. Defaults to ``False``.
        :type auto_select: bool
        :raises NotImplementedError: If a subclass does not define the
                                     ``expected_class_name`` attribute.
        :raises ValueError: If ``section_name`` or a template name is not
                            supported, or if ``auto_select`` is True but
                            multiple configuration entries exist.
        """
        if not self.expected_class_name:
            raise NotImplementedError(
                "Child class must define 'expected_class_name' attribute"
            )

        yaml_schemas = {
            "data_sets": get_data_set_config_schema,
            "training_sets": get_training_config_schema,
            "classification_sets": get_classification_config_schema,
        }
        if section_name not in yaml_schemas:
            raise ValueError(f"Section name {section_name} is not supported.")

        yaml_templates = {
            "template:data_sets": get_config_data_set_template,
            "template:training_sets": get_config_train_set_template,
            "template:classification_sets": get_config_classify_set_template,
        }
        if str(config_file).startswith("template:"):
            if str(config_file) not in yaml_templates:
                raise ValueError(f"Template name {config_file} is not supported.")
            full_config = yaml.safe_load(yaml_templates.get(str(config_file))())
        else:
            full_config = read_config(config_file)

        self.section_name: str = section_name
        self.yaml_schema: Dict = yaml.safe_load(yaml_schemas.get(section_name)())
        self.full_config: Dict = full_config
        self.valid_yaml: bool = False
        self.data: Optional[Dict] = None
        self.dataset_name: Optional[str] = None

        if auto_select:
            self.auto_select()

    def auto_select(self):
        """Automatically validate and select a single configuration entry.

        This method validates the configuration and, if it contains exactly
        one top-level entry within the specified ``section_name``, it
        automatically selects that entry. This is useful for simple
        configurations with only one dataset or task.

        :raises ValueError: If the YAML configuration is invalid, or if
                            ``auto_select`` is called when there are multiple
                            configuration entries.
        :rtype: None
        """
        message = self.validate()
        if not self.valid_yaml:
            raise ValueError(message)

        if len(self.full_config[self.section_name]) == 1:
            self.select(self.full_config[self.section_name][0]["name"])
        else:
            raise ValueError(
                "'auto_select' option is invalid when there are multiple data set names"
            )

    def validate(self) -> str:
        """Validate the loaded configuration against the corresponding schema.

        Sets the :attr:`valid_yaml` flag to ``True`` on success.

        :return: A message indicating whether validation succeeded or failed.
                 If it fails, the message includes the error details.
        :rtype: str
        """
        try:
            validate(instance=self.full_config, schema=self.yaml_schema)
            self.valid_yaml = True
            return "YAML file is valid"
        except jsonschema.exceptions.ValidationError as e:
            self.valid_yaml = False
            return f"YAML file is invalid: {e.message}"

    def select(self, dataset_name: str) -> None:
        """Select and load a specific configuration entry from the YAML.

        This method first validates the entire YAML file. If valid, it
        extracts the configuration for the specified ``dataset_name`` and
        populates the :attr:`data` attribute.

        :param dataset_name: The name of the dataset or task configuration
                             to select from the YAML file.
        :type dataset_name: str
        :raises ValueError: If the YAML configuration is invalid or the
                            specified ``dataset_name`` (or its associated
                            ``path_info`` reference) is not found in the
                            configuration.
        :rtype: None
        """
        message = self.validate()
        if not self.valid_yaml:
            raise ValueError(message)

        self.data = get_config_item(
            self.full_config, self.section_name, dataset_name
        ).copy()
        self.data["path_info"] = get_config_item(
            self.full_config, "path_info_sets", self.data["path_info"]
        )
        self.dataset_name = dataset_name

    def get_base_path(self, step_name: str) -> str:
        """Retrieve the base path for a given processing step.

        If a specific base path is not defined for the given ``step_name``,
        it falls back to the "common" base path.

        :param step_name: The name of the step (e.g., "summary", "preprocess").
        :type step_name: str
        :return: The configured base path as a string.
        :rtype: str
        :raises ValueError: If no ``base_path`` is found for the step or in
                            the "common" section of the selected configuration.
        """
        if step_name not in self.data["path_info"] or (
            step_name in self.data["path_info"]
            and "base_path" not in self.data["path_info"][step_name]
        ):
            step_name = "common"
        base_path = self.data["path_info"][step_name].get("base_path")

        if base_path is None:
            raise ValueError(
                f"'base_path' for '{step_name}' not found or set to None in the config file"
            )

        return base_path

    def get_summary_stats(self, stats_name: str, stats_type: str = "min_max") -> Dict:
        """Retrieve specific summary statistics parameters from the configuration.

        This method iterates through the `summary_stats_set` in the loaded
        configuration to find the entry matching `stats_name` and returns
        the dictionary associated with `stats_type` for that entry.

        :param stats_name: The name of the summary statistics set to retrieve
                           (e.g., "global_temperature_stats").
        :type stats_name: str
        :param stats_type: The specific type of statistics to retrieve from
                           the named set (e.g., "min_max", "mean_sd").
                           Defaults to "min_max".
        :type stats_type: str
        :raises ValueError: If the specified ``stats_name`` is not found in
                            the configuration's ``summary_stats_set``.
        :raises KeyError: If 'summary_stats_set' or 'stats' keys are missing from
                          the configuration data within the current context of `self.data`.
        :return: A dictionary containing the requested summary statistics parameters.
        :rtype: dict
        """
        for stats in self.data["summary_stats_set"]["stats"]:
            if stats["name"] == stats_name:
                return stats.get(stats_type)

        raise ValueError(
            f"Summary statistics set '{stats_name}' not found in the config file."
        )

    def get_step_params(self, step_name: str) -> Dict:
        """Retrieve the parameters dictionary for a specific step.

        :param step_name: The name of the step to get parameters for.
        :type step_name: str
        :return: A dictionary of parameters for the specified step.
        :rtype: dict
        :raises KeyError: If the specified ``step_name`` is not found in the
                          ``step_param_set.steps`` section of the configuration,
                          or if 'step_param_set' or 'steps' are missing from
                          the configuration data within the current context of `self.data`.
        """
        return self.data["step_param_set"]["steps"][step_name]

    def get_dataset_folder_name(self, step_name: str) -> str:
        """Get the dataset-specific folder name for a given step.

        This method attempts to retrieve a ``dataset_folder_name`` defined
        at the dataset level or overridden within the specific step's parameters.

        :param step_name: The name of the step.
        :type step_name: str
        :return: The folder name for the dataset specific to the step, or an
                 empty string if not defined.
        :rtype: str
        """
        dataset_folder_name = self.data.get("dataset_folder_name", "")

        if (
            step_name in self.data["step_param_set"]["steps"]
            and "dataset_folder_name" in self.data["step_param_set"]["steps"][step_name]
        ):
            dataset_folder_name = self.get_step_params(step_name).get(
                "dataset_folder_name", ""
            )

        return dataset_folder_name

    def get_step_folder_name(
        self, step_name: str, folder_name_auto: bool = True
    ) -> str:
        """Get the folder name for a specific processing step.

        If no folder name is explicitly defined in the configuration, this
        method can fall back to using the step name itself.

        :param step_name: The name of the step.
        :type step_name: str
        :param folder_name_auto: If ``True``, use ``step_name`` as the folder
                                 name if it's not defined in the config.
                                 Defaults to ``True``.
        :type folder_name_auto: bool
        :return: The step's folder name.
        :rtype: str
        """
        orig_step_name = step_name
        if step_name not in self.data["path_info"] or (
            step_name in self.data["path_info"]
            and "step_folder_name" not in self.data["path_info"][step_name]
        ):
            step_name = "common"
        step_folder_name = self.data["path_info"][step_name].get("step_folder_name")

        if step_folder_name is None:
            step_folder_name = orig_step_name if folder_name_auto else ""

        return step_folder_name

    def get_file_name(self, step_name: str, default_name: Optional[str] = None) -> str:
        """Retrieve the file name for a given step.

        This method looks for a 'file_name' entry within the step's parameters.
        If not found, it falls back to a provided default name.

        :param step_name: The name of the step.
        :type step_name: str
        :param default_name: A fallback file name to use if not defined in
                             the configuration. Defaults to ``None``.
        :type default_name: str, optional
        :return: The file name for the step.
        :rtype: str
        :raises ValueError: If no file name is found in the config for the step and no
                            ``default_name`` is provided.
        """
        file_name = default_name
        if (
            step_name in self.data["step_param_set"]["steps"]
            and "file_name" in self.data["step_param_set"]["steps"][step_name]
        ):
            file_name = self.data["step_param_set"]["steps"][step_name].get(
                "file_name", ""
            )

        if file_name is None:
            raise ValueError(
                f"'file_name' for '{step_name}' not found or set to None in the config file"
            )

        return file_name

    def get_full_file_name(
        self,
        step_name: str,
        default_file_name: Optional[str] = None,
        use_dataset_folder: bool = True,
        folder_name_auto: bool = True,
    ) -> str:
        """Construct a full, normalized file path for a step.

        The path is built by combining the base path, dataset folder (optional),
        step folder, and file name.

        :param step_name: The name of the step to construct the path for.
        :type step_name: str
        :param default_file_name: A default file name if one is not in the config.
                                  Defaults to ``None``.
        :type default_file_name: str, optional
        :param use_dataset_folder: If ``True``, include the dataset-specific
                                   folder in the path. Defaults to ``True``.
        :type use_dataset_folder: bool
        :param folder_name_auto: If ``True``, auto-generate the step folder
                                 name if not specified. Defaults to ``True``.
        :type folder_name_auto: bool
        :return: The complete, normalized file path.
        :rtype: str
        :raises ValueError: If a base path or file name cannot be determined
                            (propagated from :meth:`get_base_path` or
                            :meth:`get_file_name`).
        :raises KeyError: If 'step_param_set' or 'steps' are missing when trying
                          to get the file name or folder (propagated from
                          :meth:`get_dataset_folder_name` or :meth:`get_file_name`).
        """
        base_path = self.get_base_path(step_name)
        dataset_folder_name = (
            self.get_dataset_folder_name(step_name) if use_dataset_folder else ""
        )
        folder_name = self.get_step_folder_name(step_name, folder_name_auto)
        file_name = self.get_file_name(step_name, default_file_name)

        return os.path.normpath(
            os.path.join(base_path, dataset_folder_name, folder_name, file_name)
        )

    def get_base_class(self, step_name: str) -> str:
        """Retrieve the associated class name for a specified step.

        :param step_name: The name of the step.
        :type step_name: str
        :return: The class name defined for the step in the configuration.
        :rtype: str
        :raises KeyError: If the specified ``step_name`` is not found in the
                          ``step_class_set.steps`` section of the configuration,
                          or if 'step_class_set' or 'steps' are missing from
                          the configuration data within the current context of `self.data`.
        """
        return self.data["step_class_set"]["steps"][step_name]

    def get_target_variables(self) -> List[Dict]:
        """Get the list of target variable definitions from the configuration.

        :return: A list where each item is a dictionary defining a target variable.
        :rtype: list[dict]
        :raises KeyError: If 'target_set' or 'variables' keys are missing from
                          the configuration data within the current context of `self.data`.
        """
        return self.data["target_set"]["variables"]

    def get_target_names(self) -> List[str]:
        """Get the names of all target variables.

        :return: A list of target variable names as strings.
        :rtype: list[str]
        :raises KeyError: If 'target_set' or 'variables' keys are missing from
                          the configuration data (propagated from
                          :meth:`get_target_variables`).
        """
        return [x["name"] for x in self.get_target_variables()]

    def get_target_dict(self) -> Dict[str, Dict]:
        """Get target variable definitions as a name-keyed dictionary.

        :return: A dictionary mapping each target variable name to its
                 full definition dictionary.
        :rtype: dict[str, dict]
        :raises KeyError: If 'target_set' or 'variables' keys are missing from
                          the configuration data (propagated from
                          :meth:`get_target_variables`).
        """
        return {x["name"]: x for x in self.get_target_variables()}

    def get_target_file_names(
        self,
        step_name: str,
        default_file_name: Optional[str] = None,
        use_dataset_folder: bool = True,
        folder_name_auto: bool = True,
    ) -> Dict[str, str]:
        """Construct a dictionary of full file paths for each target variable.

        This is useful when file names are templatized with the target name,
        e.g., ``"model_{target_name}.pkl"``.

        :param step_name: The name of the step.
        :type step_name: str
        :param default_file_name: A default file name template. Defaults to ``None``.
        :type default_file_name: str, optional
        :param use_dataset_folder: If ``True``, include the dataset folder.
                                   Defaults to ``True``.
        :type use_dataset_folder: bool
        :param folder_name_auto: If ``True``, auto-generate the step folder name.
                                 Defaults to ``True``.
        :type folder_name_auto: bool
        :return: A dictionary mapping each target name to its formatted file path.
        :rtype: dict[str, str]
        :raises ValueError: If a base path or file name cannot be determined
                            (propagated from :meth:`get_full_file_name`).
        :raises KeyError: If 'target_set' or 'variables' keys are missing from
                          the configuration data, or if keys for path/step
                          parameters are missing (propagated from
                          :meth:`get_target_names` or :meth:`get_full_file_name`).
        """
        full_file_name = self.get_full_file_name(
            step_name, default_file_name, use_dataset_folder, folder_name_auto
        )
        return {
            x: full_file_name.format(target_name=x) for x in self.get_target_names()
        }

    def update_feature_param_with_stats(self):
        """Update feature parameters with corresponding summary statistics.

        This method iterates through the `feature_param_set` and, for any
        parameter dictionary that contains a "stats_set" key, it retrieves
        the relevant summary statistics using :meth:`get_summary_stats` and
        assigns them to a new "stats" key within that parameter dictionary.
        This modifies the `self.data` attribute in-place.

        :raises ValueError: If a referenced ``stats_set`` name is not found
                            in the configuration (propagated from
                            :meth:`get_summary_stats`).
        :raises KeyError: If 'feature_param_set' or 'params' keys are missing
                          from the configuration data within the current context of `self.data`.
        :rtype: None
        """
        for x in self.data["feature_param_set"]["params"]:
            if "stats_set" in x:
                x["stats"] = self.get_summary_stats(
                    x["stats_set"]["name"], x["stats_set"]["type"]
                )

    def __repr__(self) -> str:
        """Return a string representation of the configuration object.

        :return: A string identifying the instance and its managed section.
        :rtype: str
        """
        return f"ConfigBase(section_name={self.section_name})"
