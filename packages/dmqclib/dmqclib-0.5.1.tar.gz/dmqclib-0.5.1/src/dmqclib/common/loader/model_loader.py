"""
This module provides utility functions for loading and managing model classes
based on configuration settings, typically used in a machine learning or data
processing pipeline.
"""

from typing import Optional, Type

from dmqclib.common.base.config_base import ConfigBase
from dmqclib.common.base.model_base import ModelBase
from dmqclib.common.loader.model_registry import MODEL_REGISTRY


def load_model_class(config: ConfigBase) -> ModelBase:
    """
    Retrieve and instantiate a model class for the "model" step from the provided configuration.

    This function performs the following steps:

    1. Fetches the class name from the configuration using ``config.get_base_class("model")``.
    2. Looks up the corresponding class in the global :data:`~dmqclib.common.loader.model_registry.MODEL_REGISTRY`.
    3. Instantiates the found class with the given configuration object as an argument.

    :param config: A configuration object that includes a "base_class" entry
                   under the "model" step, specifying which model class to load.
                   This object must implement the ``get_base_class`` method.
    :type config: dmqclib.common.base.config_base.ConfigBase
    :returns: An instantiated model object, which is an instance of a class
              inheriting from :class:`~dmqclib.common.base.model_base.ModelBase`.
    :rtype: dmqclib.common.base.model_base.ModelBase
    :raises ValueError: If the retrieved model class name is not found in
                        the :data:`~dmqclib.common.loader.model_registry.MODEL_REGISTRY`.
    """
    class_name: str = config.get_base_class("model")
    model_class: Optional[Type[ModelBase]] = MODEL_REGISTRY.get(class_name)
    if not model_class:
        raise ValueError(f"Unknown model class specified: {class_name}")

    return model_class(config)
