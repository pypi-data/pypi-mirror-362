"""
Unit tests for configuration management functionalities,
including writing configuration templates and reading existing configuration files.
"""

import os
import unittest
from pathlib import Path

from dmqclib.common.config.classify_config import ClassificationConfig
from dmqclib.common.config.dataset_config import DataSetConfig
from dmqclib.common.config.training_config import TrainingConfig
from dmqclib.interface.config import read_config
from dmqclib.interface.config import write_config_template


class TestTemplateConfig(unittest.TestCase):
    """
    Tests for verifying that configuration templates can be correctly
    written to disk for 'prepare' (dataset) and 'train' modules.
    """

    def setUp(self):
        """
        Set up test environment by defining sample file paths
        for dataset, training, and classification configuration templates.
        """
        self.ds_config_template_file = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "temp_dataset_template.yaml"
        )

        self.config_train_set_template_file = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "temp_training_template.yaml"
        )

        self.config_classify_set_template_file = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "temp_classification_template.yaml"
        )

    def test_ds_config_template(self):
        """
        Check that a dataset (prepare) configuration template can be written
        to the specified path and removed afterward.
        """
        write_config_template(self.ds_config_template_file, "prepare")
        self.assertTrue(os.path.exists(self.ds_config_template_file))
        os.remove(self.ds_config_template_file)

    def test_config_train_set_template(self):
        """
        Check that a training configuration template can be written
        to the specified path and removed afterward.
        """
        write_config_template(self.config_train_set_template_file, "train")
        self.assertTrue(os.path.exists(self.config_train_set_template_file))
        os.remove(self.config_train_set_template_file)

    def test_config_classification_set_template(self):
        """
        Check that a classification configuration template can be written
        to the specified path and removed afterward.
        """
        write_config_template(self.config_classify_set_template_file, "classify")
        self.assertTrue(os.path.exists(self.config_classify_set_template_file))
        os.remove(self.config_classify_set_template_file)

    def test_config_template_with_invalid_module(self):
        """
        Ensure that requesting a template for an invalid module name
        raises ValueError.
        """
        with self.assertRaises(ValueError):
            write_config_template(self.ds_config_template_file, "prepare2")

    def test_config_template_with_invalid_path(self):
        """
        Ensure that attempting to write a template to an invalid path
        raises IOError.
        """
        with self.assertRaises(IOError):
            write_config_template("/abc" + str(self.ds_config_template_file), "prepare")


class TestReadConfig(unittest.TestCase):
    """
    Tests for verifying that reading an existing config file returns
    the appropriate DataSetConfig or TrainingConfig object, while
    invalid inputs raise errors.
    """

    def setUp(self):
        """
        Define sample file paths for dataset, training, and classification
        configuration files used in subsequent tests.
        """
        self.ds_config_file = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_dataset_001.yaml"
        )

        self.train_config_file = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_training_001.yaml"
        )

        self.classification_config_file = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_classify_001.yaml"
        )

        self.invalid_config_file = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_dataset_invalid.yaml"
        )

    def test_ds_config(self):
        """
        Verify that reading a dataset (prepare) config file returns
        a DataSetConfig instance.
        """
        config = read_config(self.ds_config_file)
        self.assertIsInstance(config, DataSetConfig)

    def test_train_config(self):
        """
        Verify that reading a training config file returns
        a TrainingConfig instance.
        """
        config = read_config(self.train_config_file)
        self.assertIsInstance(config, TrainingConfig)

    def test_classify_config(self):
        """
        Verify that reading a classification config file returns
        a ClassificationConfig instance.
        """
        config = read_config(self.classification_config_file)
        self.assertIsInstance(config, ClassificationConfig)

    def test_config_with_invalid_module(self):
        """
        Check that specifying an invalid module name (config_type within file)
        raises ValueError.
        """
        with self.assertRaises(ValueError):
            _ = read_config(self.invalid_config_file)

    def test_config_with_invalid_path(self):
        """
        Check that providing an invalid file path raises IOError.
        """
        with self.assertRaises(IOError):
            _ = read_config(str(self.ds_config_file) + "abc")
