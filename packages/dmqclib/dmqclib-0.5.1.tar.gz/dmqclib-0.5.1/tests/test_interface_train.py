"""
This module contains unit tests for the training and evaluation pipeline.
It verifies that the `train_and_evaluate` function correctly generates
expected output files and directories, including validation reports and
trained model artifacts.
"""

import os
import shutil
import unittest
from pathlib import Path

from dmqclib.common.config.training_config import TrainingConfig
from dmqclib.interface.train import train_and_evaluate


class TestCreateTrainingDataSet(unittest.TestCase):
    """
    A suite of tests ensuring that training and evaluation steps
    generate the expected output files and folders.
    """

    def setUp(self):
        """
        Prepare the test environment by loading a specified training configuration,
        and defining input/output paths for subsequent training/evaluation tests.
        """
        self.config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_training_001.yaml"
        )
        self.config = TrainingConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")
        self.test_data_location = Path(__file__).resolve().parent / "data" / "test"
        self.input_data_path = str(
            Path(__file__).resolve().parent / "data" / "training"
        )
        # Configure the dataset paths for the test
        self.config.data["path_info"] = {
            "name": "data_set_1",
            "common": {"base_path": str(self.test_data_location)},
            "input": {
                "base_path": str(self.input_data_path),
                "step_folder_name": "..",
            },
        }

    def tearDown(self):
        """
        Clean up the test environment by removing any generated output folders
        and files after each test method has completed.
        """
        output_folder = (
            self.test_data_location / self.config.data["dataset_folder_name"]
        )
        if output_folder.exists() and output_folder.is_dir():
            shutil.rmtree(output_folder)

    def test_train_and_evaluate(self):
        """
        Check that train_and_evaluate runs end-to-end and produces
        validation results and trained model artifacts.
        """
        # Execute the training and evaluation process
        train_and_evaluate(self.config)

        # Define the expected output folder based on the configuration
        output_folder = (
            self.test_data_location / self.config.data["dataset_folder_name"]
        )

        # Assert that expected validation report files are created
        self.assertTrue(
            os.path.exists(
                str(output_folder / "validate" / "validation_report_temp.tsv")
            )
        )
        self.assertTrue(
            os.path.exists(
                str(output_folder / "validate" / "validation_report_psal.tsv")
            )
        )
        self.assertTrue(
            os.path.exists(
                str(output_folder / "validate" / "validation_report_pres.tsv")
            )
        )

        # Assert that expected build report files are created
        self.assertTrue(
            os.path.exists(str(output_folder / "build" / "test_report_temp.tsv"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "build" / "test_report_psal.tsv"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "build" / "test_report_pres.tsv"))
        )

        # Assert that expected trained model files are created
        self.assertTrue(
            os.path.exists(str(output_folder / "model" / "model_temp.joblib"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "model" / "model_psal.joblib"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "model" / "model_pres.joblib"))
        )


class TestCreateTrainingDataSetNegX5(unittest.TestCase):
    """
    A suite of tests ensuring that training and evaluation steps
    generate the expected output files and folders.
    """

    def setUp(self):
        """
        Prepare the test environment by loading a specified training configuration,
        and defining input/output paths for subsequent training/evaluation tests.
        """
        self.config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_training_003.yaml"
        )
        self.config = TrainingConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")
        self.test_data_location = Path(__file__).resolve().parent / "data" / "test"
        self.input_data_path = (
            Path(__file__).resolve().parent / "data" / "negx5_training"
        )

        # Configure the dataset paths for the test
        self.config.data["path_info"] = {
            "name": "data_set_1",
            "common": {"base_path": str(self.test_data_location)},
            "input": {
                "base_path": str(self.input_data_path),
                "step_folder_name": "..",
            },
        }

    def tearDown(self):
        """
        Clean up the test environment by removing any generated output folders
        and files after each test method has completed.
        """
        output_folder = (
            self.test_data_location / self.config.data["dataset_folder_name"]
        )
        if output_folder.exists() and output_folder.is_dir():
            shutil.rmtree(output_folder)

    def test_train_and_evaluate(self):
        """
        Check that train_and_evaluate runs end-to-end and produces
        validation results and trained model artifacts.
        """
        # Execute the training and evaluation process
        train_and_evaluate(self.config)

        # Define the expected output folder based on the configuration
        output_folder = (
            self.test_data_location / self.config.data["dataset_folder_name"]
        )

        # Assert that expected validation report files are created
        self.assertTrue(
            os.path.exists(
                str(output_folder / "validate" / "validation_report_temp.tsv")
            )
        )
        self.assertTrue(
            os.path.exists(
                str(output_folder / "validate" / "validation_report_psal.tsv")
            )
        )
        self.assertTrue(
            os.path.exists(
                str(output_folder / "validate" / "validation_report_pres.tsv")
            )
        )

        # Assert that expected build report files are created
        self.assertTrue(
            os.path.exists(str(output_folder / "build" / "test_report_temp.tsv"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "build" / "test_report_psal.tsv"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "build" / "test_report_pres.tsv"))
        )

        # Assert that expected trained model files are created
        self.assertTrue(
            os.path.exists(str(output_folder / "model" / "model_temp.joblib"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "model" / "model_psal.joblib"))
        )
        self.assertTrue(
            os.path.exists(str(output_folder / "model" / "model_pres.joblib"))
        )
