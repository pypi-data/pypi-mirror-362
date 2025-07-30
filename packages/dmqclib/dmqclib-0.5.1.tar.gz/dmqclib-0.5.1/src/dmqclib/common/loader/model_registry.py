"""
This module provides a registry of model classes that can be used
during training or inference steps. Each key in the dictionary
corresponds to a model name (string), and each value is the class
constructor for that model.
"""

from typing import Dict, Type

from dmqclib.common.base.model_base import ModelBase
from dmqclib.train.models.xgboost import XGBoost

#: A dictionary mapping model names to their corresponding Python classes.
#:
#: The keys are strings (e.g., "XGBoost"), and the values are class objects
#: that inherit from :class:`dmqclib.common.base.model_base.ModelBase`.
#:
#: :type: Dict[str, Type[ModelBase]]
MODEL_REGISTRY: Dict[str, Type[ModelBase]] = {
    "XGBoost": XGBoost,
}
