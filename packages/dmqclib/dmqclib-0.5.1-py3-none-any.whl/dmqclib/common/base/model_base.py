"""
This module defines `ModelBase`, an abstract base class for developing
machine learning models within the dmqclib framework.

It provides a common interface and essential functionalities such as
configuration loading, model saving, and model loading, which all
concrete model implementations should inherit and extend.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional, Any

from joblib import dump, load

from dmqclib.common.base.config_base import ConfigBase


class ModelBase(ABC):
    """
    Abstract base class for modeling tasks.

    Subclasses must define:

    - ``expected_class_name`` to match the configuration
    - The :meth:`build` method for model building
    - The :meth:`test` method for model testing

    .. note::

       Since this class inherits from :class:`abc.ABC`, it cannot be directly
       instantiated and must be subclassed.
    """

    expected_class_name: Optional[str] = None  # Must be overridden by child classes

    def __init__(self, config: ConfigBase) -> None:
        """
        Initialize the model with configuration data and validate
        that the expected class name matches what's in the YAML configuration.

        :param config: A configuration object providing parameters
                       needed for model assembly and execution.
        :type config: ConfigBase
        :raises NotImplementedError: If ``expected_class_name`` is not defined in a subclass.
        :raises ValueError: If the class name derived from the configuration
                            does not match the ``expected_class_name`` of this class.
        """
        if not self.expected_class_name:
            raise NotImplementedError(
                "Child class must define 'expected_class_name' attribute"
            )

        # Validate that the YAML's "class" matches the child's declared class name
        base_class = config.get_base_class("model")
        if base_class != self.expected_class_name:
            raise ValueError(
                f"Configuration mismatch: expected class '{self.expected_class_name}' "
                f"but got '{base_class}'"
            )

        model_params = config.data["step_param_set"]["steps"]["model"].get(
            "model_params", {}
        )

        self.config: ConfigBase = config
        self.model_params: dict = model_params

        self.training_set: Optional[Any] = None
        self.test_set: Optional[Any] = None
        self.model: Optional[Any] = None
        self.predictions: Optional[Any] = None
        self.report: Optional[Any] = None
        self.k: int = 0

    @abstractmethod
    def build(self) -> None:
        """
        Build the model architecture or pipeline.

        Subclasses must implement logic to create, configure,
        and compile the model.
        """
        pass  # pragma: no cover

    @abstractmethod
    def test(self) -> None:
        """
        Evaluate the model performance on a provided test set or validation data.

        Subclasses must implement how the model is used to make predictions
        and how accuracy or performance measures are computed.
        """
        pass  # pragma: no cover

    def load_model(self, file_name: str) -> None:
        """
        Load or deserialize a model from the given file path.

        :param file_name: The path to the file from which the model will be loaded.
        :type file_name: str
        :raises FileNotFoundError: If the specified file does not exist.
        """
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"File '{file_name}' does not exist.")

        self.model = load(file_name)

    def save_model(self, file_name: str) -> None:
        """
        Save or serialize the current model to the provided file path.

        :param file_name: The path indicating where the model will be saved.
        :type file_name: str
        """
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        dump(self.model, file_name)

    def __repr__(self) -> str:
        """
        Return a string representation of the ModelBase instance.

        :return: A string describing the instance with its class name declared by ``expected_class_name``.
        :rtype: str
        """
        return f"ModelBase(class={self.expected_class_name})"
