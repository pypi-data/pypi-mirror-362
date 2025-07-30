"""
Unit tests for the DataSetBase class in dmqclib.common.base.model_base
This module verifies the correct functionality of DataSetBase's methods.
"""

import unittest
from pathlib import Path

from dmqclib.common.base.config_base import ConfigBase
from dmqclib.common.base.model_base import ModelBase
from dmqclib.common.config.training_config import TrainingConfig


class ModelBaseWithEmptyName(ModelBase):
    """
    ModelBaseWithEmptyName is used to test methods and variables in ModelBase
    """

    def __init__(self, config: ConfigBase) -> None:
        super().__init__(config)

    def build(self) -> None:
        pass

    def test(self) -> None:
        pass


class ModelBaseWithExpectedName(ModelBase):
    """
    ModelBaseWithExpectedName is used to test methods and variables in ModelBase
    """

    expected_class_name: str = "XGBoost"

    def __init__(self, config: ConfigBase) -> None:
        super().__init__(config)

    def build(self) -> None:
        pass

    def test(self) -> None:
        pass


class ModelBaseWithWrongName(ModelBase):
    """
    ModelBaseWithWrongName is used to test methods and variables in ModelBase
    """

    expected_class_name: str = "XGBoostZ"

    def __init__(self, config: ConfigBase) -> None:
        super().__init__(config)

    def build(self) -> None:
        pass

    def test(self) -> None:
        pass


class TestModelBaseMethods(unittest.TestCase):
    """
    A suite of tests that verify the correctness of methods
    within the ModelBase.
    """

    def setUp(self):
        """
        Set up a reference to the test configuration file (test_training_001.yaml)
        to be used by all subsequent tests in this class.
        """
        self.config_file_path = (
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_training_001.yaml"
        )
        self.config = TrainingConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")

    def test_expected_class_name(self):
        """
        Ensure that an undefined expected class_name raises a NotImplementedError.
        """
        with self.assertRaises(NotImplementedError):
            _ = ModelBaseWithEmptyName(self.config)

    def test_model_name(self):
        """
        Ensure that an unmatched model name raises a ValueError.
        """
        with self.assertRaises(ValueError):
            _ = ModelBaseWithWrongName(self.config)

    def test_representing_str(self):
        """
        Ensure that the instance returns a correct string representation.
        """
        ds = ModelBaseWithExpectedName(self.config)
        self.assertEqual(str(ds), "ModelBase(class=XGBoost)")

    def test_load_input_with_invalid_path(self):
        """
        Ensure that an invalid file path raises a FileNotFoundError.
        """
        ds = ModelBaseWithExpectedName(self.config)
        with self.assertRaises(FileNotFoundError):
            ds.load_model("invalid_file_path")
