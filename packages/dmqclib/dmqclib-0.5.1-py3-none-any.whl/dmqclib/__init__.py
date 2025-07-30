"""
This module provides a high-level interface to the dmqclib library,
exposing core functionalities for configuration management, dataset
preparation, model training and evaluation, and dataset classification.
"""

from importlib.metadata import version

from dmqclib.interface.classify import classify_dataset as classify_dataset
from dmqclib.interface.config import read_config as read_config
from dmqclib.interface.config import write_config_template as write_config_template
from dmqclib.interface.prepare import create_training_dataset as create_training_dataset
from dmqclib.interface.stats import format_summary_stats as format_summary_stats
from dmqclib.interface.stats import get_summary_stats as get_summary_stats
from dmqclib.interface.train import train_and_evaluate as train_and_evaluate

__version__ = version("dmqclib")
