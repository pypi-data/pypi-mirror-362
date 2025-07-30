"""
This module contains unit tests for the BuildModel class, which is responsible
for building, testing, and saving machine learning models, specifically XGBoost models,
within the dmqclib training pipeline.
"""

import os
import unittest
from pathlib import Path

import polars as pl

from dmqclib.common.config.training_config import TrainingConfig
from dmqclib.common.loader.training_loader import load_step1_input_training_set
from dmqclib.train.models.xgboost import XGBoost
from dmqclib.train.step4_build_model.build_model import BuildModel


class TestBuildModel(unittest.TestCase):
    """
    A suite of tests ensuring that building, testing, and saving XGBoost models
    via BuildModel follows the expected configuration and data flows.
    """

    def setUp(self):
        """
        Prepare a test training configuration and load input data for subsequent tests.
        Define mock train/test file paths for data loading.
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
        """Check that the BuildModel step name is correctly assigned."""
        ds = BuildModel(self.config)
        self.assertEqual(ds.step_name, "build")

    def test_output_file_names(self):
        """
        Verify that default output file names (model and results) are as expected
        based on the configuration.
        """
        ds = BuildModel(self.config)

        self.assertEqual(
            "/path/to/model_1/nrt_bo_001/model_folder_1/model_temp.joblib",
            str(ds.model_file_names["temp"]),
        )
        self.assertEqual(
            "/path/to/model_1/nrt_bo_001/model_folder_1/model_psal.joblib",
            str(ds.model_file_names["psal"]),
        )
        self.assertEqual(
            "/path/to/model_1/nrt_bo_001/model_folder_1/model_pres.joblib",
            str(ds.model_file_names["pres"]),
        )

        self.assertEqual(
            "/path/to/build_1/nrt_bo_001/build_folder_1/test_report_temp.tsv",
            str(ds.output_file_names["report"]["temp"]),
        )
        self.assertEqual(
            "/path/to/build_1/nrt_bo_001/build_folder_1/test_report_psal.tsv",
            str(ds.output_file_names["report"]["psal"]),
        )
        self.assertEqual(
            "/path/to/build_1/nrt_bo_001/build_folder_1/test_report_pres.tsv",
            str(ds.output_file_names["report"]["pres"]),
        )

    def test_base_model(self):
        """Ensure that the configured base model is an XGBoost instance."""
        ds = BuildModel(self.config)
        self.assertIsInstance(ds.base_model, XGBoost)

    def test_training_sets(self):
        """
        Check that training and test sets are loaded into BuildModel correctly,
        verifying their types and dimensions.
        """
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=self.ds_input.test_sets,
        )

        self.assertIsInstance(ds.training_sets["temp"], pl.DataFrame)
        self.assertEqual(ds.training_sets["temp"].shape[0], 116)
        self.assertEqual(ds.training_sets["temp"].shape[1], 57)

        self.assertIsInstance(ds.training_sets["psal"], pl.DataFrame)
        self.assertEqual(ds.training_sets["psal"].shape[0], 126)
        self.assertEqual(ds.training_sets["psal"].shape[1], 57)

        self.assertIsInstance(ds.training_sets["pres"], pl.DataFrame)
        self.assertEqual(ds.training_sets["pres"].shape[0], 110)
        self.assertEqual(ds.training_sets["pres"].shape[1], 57)

        self.assertIsInstance(ds.test_sets["temp"], pl.DataFrame)
        self.assertEqual(ds.test_sets["temp"].shape[0], 12)
        self.assertEqual(ds.test_sets["temp"].shape[1], 56)

        self.assertIsInstance(ds.test_sets["psal"], pl.DataFrame)
        self.assertEqual(ds.test_sets["psal"].shape[0], 14)
        self.assertEqual(ds.test_sets["psal"].shape[1], 56)

        self.assertIsInstance(ds.test_sets["pres"], pl.DataFrame)
        self.assertEqual(ds.test_sets["pres"].shape[0], 12)
        self.assertEqual(ds.test_sets["pres"].shape[1], 56)

    def test_train_with_xgboost(self):
        """Confirm that building models populates the 'models' dictionary with XGBoost instances."""
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=self.ds_input.test_sets,
        )
        ds.build_targets()

        self.assertIsInstance(ds.models["temp"], XGBoost)
        self.assertIsInstance(ds.models["psal"], XGBoost)
        self.assertIsInstance(ds.models["pres"], XGBoost)

    def test_model_objects(self):
        """
        Confirm that building models populates a unique model object for each target.
        Ensures distinct model instances are created, not just references to the same object.
        """
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=self.ds_input.test_sets,
        )
        ds.build_targets()

        self.assertIsNot(ds.models["temp"], ds.models["psal"])
        self.assertIsNot(ds.models["temp"], ds.models["pres"])
        self.assertIsNot(ds.models["psal"], ds.models["pres"])

        # Note: assertNotEqual may depend on XGBoost's __eq__ implementation,
        # but assertIsNot is a stronger check for distinct instances.
        self.assertNotEqual(ds.models["temp"], ds.models["psal"])
        self.assertNotEqual(ds.models["temp"], ds.models["pres"])
        self.assertNotEqual(ds.models["psal"], ds.models["pres"])

    def test_build_without_test_sets(self):
        """Ensure that calling build_targets() with no test sets available raises a ValueError."""
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=None,
        )
        with self.assertRaises(ValueError):
            ds.build_targets()

    def test_build_without_training_sets(self):
        """Ensure that calling build_targets() with no training sets available raises a ValueError."""
        ds = BuildModel(
            self.config,
            training_sets=None,
            test_sets=None,
        )
        with self.assertRaises(ValueError):
            ds.build_targets()

    def test_test_with_xgboost(self):
        """
        Check that testing sets after model building populates the result columns,
        verifying data types and dimensions remain consistent.
        """
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=self.ds_input.test_sets,
        )
        ds.build_targets()
        ds.test_targets()

        self.assertIsInstance(ds.test_sets["temp"], pl.DataFrame)
        self.assertEqual(ds.test_sets["temp"].shape[0], 12)
        self.assertEqual(ds.test_sets["temp"].shape[1], 56)

        self.assertIsInstance(ds.test_sets["psal"], pl.DataFrame)
        self.assertEqual(ds.test_sets["psal"].shape[0], 14)
        self.assertEqual(ds.test_sets["psal"].shape[1], 56)

        self.assertIsInstance(ds.test_sets["pres"], pl.DataFrame)
        self.assertEqual(ds.test_sets["pres"].shape[0], 12)
        self.assertEqual(ds.test_sets["pres"].shape[1], 56)

    def test_test_without_model(self):
        """Ensure that calling test_targets() without first building models raises a ValueError."""
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=self.ds_input.test_sets,
        )
        with self.assertRaises(ValueError):
            ds.test_targets()

    def test_write_reports(self):
        """
        Check that test reports are correctly written to file,
        and then remove the temporary files created.
        """
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=self.ds_input.test_sets,
        )
        data_path = Path(__file__).resolve().parent / "data" / "training"
        ds.output_file_names["report"]["temp"] = str(
            data_path / "temp_test_report_temp.tsv"
        )
        ds.output_file_names["report"]["psal"] = str(
            data_path / "temp_test_report_psal.tsv"
        )
        ds.output_file_names["report"]["pres"] = str(
            data_path / "temp_test_report_pres.tsv"
        )

        ds.build_targets()
        ds.test_targets()
        ds.write_reports()

        self.assertTrue(os.path.exists(ds.output_file_names["report"]["temp"]))
        self.assertTrue(os.path.exists(ds.output_file_names["report"]["psal"]))
        self.assertTrue(os.path.exists(ds.output_file_names["report"]["pres"]))

        os.remove(ds.output_file_names["report"]["temp"])
        os.remove(ds.output_file_names["report"]["psal"])
        os.remove(ds.output_file_names["report"]["pres"])

    def test_write_no_results(self):
        """
        Ensure that ValueError is raised if write_reports is called
        with no test results available.
        """
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=self.ds_input.test_sets,
        )
        with self.assertRaises(ValueError):
            ds.write_reports()

    def test_write_no_models(self):
        """
        Ensure ValueError is raised if write_models is called without any built models.
        """
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=self.ds_input.test_sets,
        )
        with self.assertRaises(ValueError):
            ds.write_models()

    def test_write_models(self):
        """
        Check that the trained models are serialized to files correctly,
        and then remove the temporary files created.
        """
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=self.ds_input.test_sets,
        )
        data_path = Path(__file__).resolve().parent / "data" / "training"
        ds.model_file_names["temp"] = str(data_path / "temp_model_temp.joblib")
        ds.model_file_names["psal"] = str(data_path / "temp_model_psal.joblib")
        ds.model_file_names["pres"] = str(data_path / "temp_model_pres.joblib")

        ds.build_targets()
        ds.write_models()

        self.assertTrue(os.path.exists(ds.model_file_names["temp"]))
        self.assertTrue(os.path.exists(ds.model_file_names["psal"]))
        self.assertTrue(os.path.exists(ds.model_file_names["pres"]))

        os.remove(ds.model_file_names["temp"])
        os.remove(ds.model_file_names["psal"])
        os.remove(ds.model_file_names["pres"])

    def test_read_models(self):
        """
        Verify that existing models can be reloaded from disk and successfully
        used for testing.
        """
        ds = BuildModel(
            self.config, training_sets=None, test_sets=self.ds_input.test_sets
        )
        data_path = Path(__file__).resolve().parent / "data" / "training"
        ds.model_file_names["temp"] = str(data_path / "model_temp.joblib")
        ds.model_file_names["psal"] = str(data_path / "model_psal.joblib")
        ds.model_file_names["pres"] = str(data_path / "model_pres.joblib")

        ds.read_models()

        self.assertIsInstance(ds.models["temp"], XGBoost)
        self.assertIsInstance(ds.models["psal"], XGBoost)
        self.assertIsInstance(ds.models["pres"], XGBoost)

        ds.test_targets()

        self.assertIsInstance(ds.test_sets["temp"], pl.DataFrame)
        self.assertEqual(ds.test_sets["temp"].shape[0], 12)
        self.assertEqual(ds.test_sets["temp"].shape[1], 56)

        self.assertIsInstance(ds.test_sets["psal"], pl.DataFrame)
        self.assertEqual(ds.test_sets["psal"].shape[0], 14)
        self.assertEqual(ds.test_sets["psal"].shape[1], 56)

    def test_read_models_no_file(self):
        """Check that FileNotFoundError is raised if model files are missing during reading."""
        ds = BuildModel(
            self.config, training_sets=None, test_sets=self.ds_input.test_sets
        )
        data_path = Path(__file__).resolve().parent / "data" / "training"
        ds.model_file_names["temp"] = str(data_path / "non_existent_model.joblib")
        ds.model_file_names["psal"] = str(data_path / "non_existent_model.joblib")
        ds.model_file_names["pres"] = str(data_path / "non_existent_model.joblib")

        with self.assertRaises(FileNotFoundError):
            ds.read_models()

    def test_write_predictions(self):
        """
        Check that test predictions are correctly written to file,
        and then remove the temporary files created.
        """
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=self.ds_input.test_sets,
        )
        data_path = Path(__file__).resolve().parent / "data" / "training"
        ds.output_file_names["prediction"]["temp"] = str(
            data_path / "temp_test_prediction_temp.parquet"
        )
        ds.output_file_names["prediction"]["psal"] = str(
            data_path / "temp_test_prediction_psal.parquet"
        )
        ds.output_file_names["prediction"]["pres"] = str(
            data_path / "temp_test_prediction_pres.parquet"
        )

        ds.build_targets()
        ds.test_targets()
        ds.write_predictions()

        self.assertTrue(os.path.exists(ds.output_file_names["prediction"]["temp"]))
        self.assertTrue(os.path.exists(ds.output_file_names["prediction"]["psal"]))
        self.assertTrue(os.path.exists(ds.output_file_names["prediction"]["pres"]))

        os.remove(ds.output_file_names["prediction"]["temp"])
        os.remove(ds.output_file_names["prediction"]["psal"])
        os.remove(ds.output_file_names["prediction"]["pres"])

    def test_write_empty_predictions(self):
        """
        Ensure that calling write_predictions() before predictions are generated
        (i.e., before test_targets() is called) raises a ValueError.
        """
        ds = BuildModel(
            self.config,
            training_sets=self.ds_input.training_sets,
            test_sets=self.ds_input.test_sets,
        )
        with self.assertRaises(ValueError):
            ds.write_predictions()
