"""
Unit tests for the `create_training_dataset` function, verifying its ability to
generate the correct directory structure and output files for various data
processing steps within a training dataset.
"""

import os
import shutil
import unittest
from pathlib import Path

from dmqclib.common.config.dataset_config import DataSetConfig
from dmqclib.interface.prepare import create_training_dataset


class TestCreateTrainingDataSet(unittest.TestCase):
    """
    Tests for verifying that create_training_dataset produces the
    expected directory structure and output files for training data.
    """

    def setUp(self):
        """
        Prepare the test environment by creating a DataSetConfig object,
        defining file paths, and updating the configuration with test input
        and output paths.
        """
        self.config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_dataset_001.yaml"
        )
        self.config = DataSetConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")
        self.config.data["input_file_name"] = "nrt_cora_bo_test.parquet"
        self.test_data_location = Path(__file__).resolve().parent / "data" / "test"
        self.input_data_path = Path(__file__).resolve().parent / "data" / "input"
        self.config.data["path_info"] = {
            "name": "data_set_1",
            "common": {"base_path": str(self.test_data_location)},
            "input": {"base_path": str(self.input_data_path), "step_folder_name": ""},
        }

    def test_create_training_data_set(self):
        """
        Verify that `create_training_dataset` generates the expected folder
        hierarchy and all required output files for summary, select, locate,
        extract, and split steps.
        """
        create_training_dataset(self.config)

        output_folder = (
            self.test_data_location / self.config.data["dataset_folder_name"]
        )

        self.assertTrue(
            os.path.exists(str(output_folder / "summary" / "summary_stats.tsv"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "select" / "selected_profiles.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "locate" / "selected_rows_temp.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "locate" / "selected_rows_psal.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "locate" / "selected_rows_pres.parquet"))
        )
        self.assertTrue(
            os.path.exists(
                str(output_folder / "extract" / "extracted_features_temp.parquet")
            )
        )
        self.assertTrue(
            os.path.exists(
                str(output_folder / "extract" / "extracted_features_psal.parquet")
            )
        )
        self.assertTrue(
            os.path.exists(
                str(output_folder / "extract" / "extracted_features_pres.parquet")
            )
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "split" / "train_set_temp.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "split" / "train_set_psal.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "split" / "train_set_pres.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "split" / "test_set_temp.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "split" / "test_set_psal.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "split" / "test_set_pres.parquet"))
        )

    def tearDown(self):
        """
        Clean up the test environment by removing the generated output directory
        and its contents after each test.
        """
        output_folder = (
            self.test_data_location / self.config.data["dataset_folder_name"]
        )
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)


class TestCreateTrainingDataSetNegX5(unittest.TestCase):
    """
    Tests for verifying that create_training_dataset produces the
    expected directory structure and output files for training data when
    custom step folder names are configured.
    """

    def setUp(self):
        """
        Prepare the test environment by creating a DataSetConfig object,
        defining file paths, and updating the configuration with test input
        and output paths, including a custom folder name for the 'split' step.
        """
        self.config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_dataset_003.yaml"
        )
        self.config = DataSetConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")
        self.config.data["input_file_name"] = "nrt_cora_bo_test.parquet"
        self.test_data_location = Path(__file__).resolve().parent / "data" / "test"
        self.input_data_path = Path(__file__).resolve().parent / "data" / "input"
        self.config.data["path_info"] = {
            "name": "data_set_1",
            "common": {"base_path": str(self.test_data_location)},
            "input": {"base_path": str(self.input_data_path), "step_folder_name": ""},
            "split": {"step_folder_name": "training"},
        }

    def test_create_training_data_set(self):
        """
        Verify that `create_training_dataset` generates the expected folder
        hierarchy and all required output files, specifically checking the
        custom 'training' folder for split data.
        """
        create_training_dataset(self.config)

        output_folder = (
            self.test_data_location / self.config.data["dataset_folder_name"]
        )

        self.assertTrue(
            os.path.exists(str(output_folder / "summary" / "summary_stats.tsv"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "select" / "selected_profiles.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "locate" / "selected_rows_temp.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "locate" / "selected_rows_psal.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "locate" / "selected_rows_pres.parquet"))
        )
        self.assertTrue(
            os.path.exists(
                str(output_folder / "extract" / "extracted_features_temp.parquet")
            )
        )
        self.assertTrue(
            os.path.exists(
                str(output_folder / "extract" / "extracted_features_psal.parquet")
            )
        )
        self.assertTrue(
            os.path.exists(
                str(output_folder / "extract" / "extracted_features_pres.parquet")
            )
        )
        # Verify files are in the custom 'training' folder instead of 'split'
        self.assertTrue(
            os.path.exists(str(output_folder / "training" / "train_set_temp.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "training" / "train_set_psal.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "training" / "train_set_pres.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "training" / "test_set_temp.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "training" / "test_set_psal.parquet"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "training" / "test_set_pres.parquet"))
        )

    def tearDown(self):
        """
        Clean up the test environment by removing the generated output directory
        and its contents after each test.
        """
        output_folder = (
            self.test_data_location / self.config.data["dataset_folder_name"]
        )
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
