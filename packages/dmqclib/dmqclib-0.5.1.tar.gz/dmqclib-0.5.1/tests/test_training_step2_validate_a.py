"""
This module contains unit tests for the KFoldValidation class, ensuring its
correct integration with training configurations, data loading, model execution
(XGBoost), and report generation. It verifies that the validation process
behaves as expected across various scenarios.
"""

import os
import unittest
from pathlib import Path

import polars as pl

from dmqclib.common.config.training_config import TrainingConfig
from dmqclib.common.loader.training_loader import load_step1_input_training_set
from dmqclib.train.models.xgboost import XGBoost
from dmqclib.train.step2_validate_model.kfold_validation import KFoldValidation


class TestKFoldValidation(unittest.TestCase):
    """
    A suite of tests ensuring that KFoldValidation correctly captures
    configurations, splits training data, applies the XGBoost model,
    and writes validation results.
    """

    def setUp(self):
        """
        Prepare the test environment by loading a training configuration
        and input training data. The input file names for train/test sets
        are defined here for subsequent model validation tests.
        """
        self.config_file_path = (
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_training_001.yaml"
        )
        self.config = TrainingConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")
        data_path = Path(__file__).resolve().parent / "data" / "training"
        self.input_file_names = {
            "train": {
                "temp": str(data_path / "train_set_temp.parquet"),
                "psal": str(data_path / "train_set_psal.parquet"),
                "pres": str(data_path / "train_set_pres.parquet"),
            },
            "test": {
                "temp": str(data_path / "test_set_temp.parquet"),
                "psal": str(data_path / "test_set_psal.parquet"),
                "pres": str(data_path / "test_set_pres.parquet"),
            },
        }

        self.ds_input = load_step1_input_training_set(self.config)
        self.ds_input.input_file_names = self.input_file_names
        self.ds_input.process_targets()

    def test_step_name(self):
        """
        Check that the step name is correctly identified as 'validate'.
        """
        ds = KFoldValidation(self.config)
        self.assertEqual(ds.step_name, "validate")

    def test_output_file_names(self):
        """
        Verify that the default output file names are correctly resolved
        based on the configuration.
        """
        ds = KFoldValidation(self.config)
        self.assertEqual(
            "/path/to/validate_1/nrt_bo_001/validate_folder_1/validation_report_temp.tsv",
            str(ds.output_file_names["report"]["temp"]),
        )
        self.assertEqual(
            "/path/to/validate_1/nrt_bo_001/validate_folder_1/validation_report_psal.tsv",
            str(ds.output_file_names["report"]["psal"]),
        )
        self.assertEqual(
            "/path/to/validate_1/nrt_bo_001/validate_folder_1/validation_report_pres.tsv",
            str(ds.output_file_names["report"]["pres"]),
        )

    def test_base_model(self):
        """
        Ensure the base model attribute of KFoldValidation is an XGBoost
        instance, as defined by the configuration.
        """
        ds = KFoldValidation(self.config)
        self.assertIsInstance(ds.base_model, XGBoost)

    def test_training_sets(self):
        """
        Check that training data is properly loaded and accessible
        within the KFoldValidation instance.
        """
        ds = KFoldValidation(self.config, training_sets=self.ds_input.training_sets)

        self.assertIsInstance(ds.training_sets["temp"], pl.DataFrame)
        self.assertEqual(ds.training_sets["temp"].shape[0], 116)
        self.assertEqual(ds.training_sets["temp"].shape[1], 57)

        self.assertIsInstance(ds.training_sets["psal"], pl.DataFrame)
        self.assertEqual(ds.training_sets["psal"].shape[0], 126)
        self.assertEqual(ds.training_sets["psal"].shape[1], 57)

        self.assertIsInstance(ds.training_sets["pres"], pl.DataFrame)
        self.assertEqual(ds.training_sets["pres"].shape[0], 110)
        self.assertEqual(ds.training_sets["pres"].shape[1], 57)

    def test_default_k_fold(self):
        """
        Confirm that the k_fold value defaults to 10 if no specific
        configuration entry is present for it.
        """
        ds = KFoldValidation(self.config, training_sets=self.ds_input.training_sets)
        # Temporarily modify config data to simulate missing k_fold setting
        ds.config.data["step_param_set"]["steps"]["validate"]["k_fold"] = None

        k_fold = ds.get_k_fold()
        self.assertEqual(k_fold, 10)

    def test_fold_validation(self):
        """
        Check that the KFoldValidation process, utilizing the XGBoost model,
        successfully processes the training sets and populates the reports.
        """
        ds = KFoldValidation(self.config, training_sets=self.ds_input.training_sets)
        ds.process_targets()

        self.assertIsInstance(ds.reports["temp"], pl.DataFrame)
        self.assertEqual(ds.reports["temp"].shape[0], 18)
        self.assertEqual(ds.reports["temp"].shape[1], 8)

        self.assertIsInstance(ds.reports["psal"], pl.DataFrame)
        self.assertEqual(ds.reports["psal"].shape[0], 18)
        self.assertEqual(ds.reports["psal"].shape[1], 8)

        self.assertIsInstance(ds.reports["pres"], pl.DataFrame)
        self.assertEqual(ds.reports["pres"].shape[0], 18)
        self.assertEqual(ds.reports["pres"].shape[1], 8)

    def test_write_results(self):
        """
        Ensure validation reports are written to the specified output files
        and that these files are created on the file system.
        Temporary files are cleaned up after the test.
        """
        ds = KFoldValidation(self.config, training_sets=self.ds_input.training_sets)

        data_path = Path(__file__).resolve().parent / "data" / "training"
        ds.output_file_names["report"]["temp"] = str(
            data_path / "temp_validation_report_temp.tsv"
        )
        ds.output_file_names["report"]["psal"] = str(
            data_path / "temp_validation_report_psal.tsv"
        )
        ds.output_file_names["report"]["pres"] = str(
            data_path / "temp_validation_report_pres.tsv"
        )

        ds.process_targets()
        ds.write_reports()

        self.assertTrue(os.path.exists(ds.output_file_names["report"]["temp"]))
        self.assertTrue(os.path.exists(ds.output_file_names["report"]["psal"]))
        self.assertTrue(os.path.exists(ds.output_file_names["report"]["pres"]))

        os.remove(ds.output_file_names["report"]["temp"])
        os.remove(ds.output_file_names["report"]["psal"])
        os.remove(ds.output_file_names["report"]["pres"])

    def test_write_reports_empty_reports(self):
        """
        Ensure that calling write_reports with empty reports (i.e., before
        process_targets has been called) raises a ValueError.
        """
        ds = KFoldValidation(self.config, training_sets=self.ds_input.training_sets)
        with self.assertRaises(ValueError):
            ds.write_reports()
