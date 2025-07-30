"""Unit tests for the XGBoost model class.

This module verifies the integration of the XGBoost model with the dmqclib
configuration system, ensuring parameters are correctly loaded and processed.
"""

import unittest
from pathlib import Path

from dmqclib.common.config.training_config import TrainingConfig
from dmqclib.train.models.xgboost import XGBoost


class TestXGBoost(unittest.TestCase):
    """A suite of tests verifying basic XGBoost model setup and functionality
    through the dmqclib configuration system.
    """

    def setUp(self):
        """Define the path to the training configuration file
        and select the appropriate dataset prior to each test.
        """
        self.config_file_path = (
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_training_001.yaml"
        )
        self.config = TrainingConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")

    def test_init_class(self):
        """Verify that initializing an XGBoost object sets default values correctly.

        This test checks if the `k` attribute of the XGBoost instance
        is initialized to its expected default value (0).
        """
        ds = XGBoost(self.config)
        self.assertEqual(ds.k, 0)

    def test_model_params_scale_pos_weight(self):
        """Verify that the `scale_pos_weight` parameter can be set via configuration.

        This test modifies the configuration to include a custom
        `scale_pos_weight` and asserts that the XGBoost model
        correctly picks up this value.
        """
        self.config.data["step_param_set"]["steps"]["model"]["model_params"] = {
            "scale_pos_weight": 10
        }
        ds = XGBoost(self.config)

        self.assertIn("scale_pos_weight", ds.model_params)
        self.assertEqual(ds.model_params["scale_pos_weight"], 10)

    def test_model_params_max_depth(self):
        """Verify that the `max_depth` parameter can be set via configuration.

        This test modifies the configuration to include a custom
        `max_depth` and asserts that the XGBoost model
        correctly picks up this value.
        """
        self.config.data["step_param_set"]["steps"]["model"]["model_params"] = {
            "max_depth": 10
        }
        ds = XGBoost(self.config)

        self.assertIn("max_depth", ds.model_params)
        self.assertEqual(ds.model_params["max_depth"], 10)
