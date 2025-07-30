"""
Unit tests for verifying the correct loading and initialization of dataset classes
at various processing steps, using common loader functions.

These tests ensure that the dataset objects are correctly instantiated with the
expected step names and that any provided input data (e.g., from previous steps)
is properly assigned and retains its expected structure.
"""

import unittest
from pathlib import Path

import polars as pl

from dmqclib.common.config.dataset_config import DataSetConfig
from dmqclib.common.loader.dataset_loader import (
    load_step1_input_dataset,
    load_step2_summary_dataset,
    load_step3_select_dataset,
    load_step4_locate_dataset,
    load_step5_extract_dataset,
    load_step6_split_dataset,
)
from dmqclib.prepare.step1_read_input.dataset_a import InputDataSetA
from dmqclib.prepare.step2_calc_stats.dataset_a import SummaryDataSetA
from dmqclib.prepare.step3_select_profiles.dataset_a import SelectDataSetA
from dmqclib.prepare.step4_select_rows.dataset_a import LocateDataSetA
from dmqclib.prepare.step5_extract_features.dataset_a import ExtractDataSetA
from dmqclib.prepare.step6_split_dataset.dataset_a import SplitDataSetA


class TestInputClassLoader(unittest.TestCase):
    """
    Tests related to loading the InputDataSetA class.
    """

    def setUp(self):
        """
        Define the path to the test config file and select a dataset
        prior to each test.
        """
        self.config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_dataset_001.yaml"
        )
        self.config = DataSetConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")

    def test_load_dataset_valid_config(self):
        """
        Check that load_step1_input_dataset returns an InputDataSetA instance with
        the expected step name.
        """
        ds = load_step1_input_dataset(self.config)
        self.assertIsInstance(ds, InputDataSetA)
        self.assertEqual(ds.step_name, "input")

    def test_load_input_class_with_invalid_config(self):
        """
        Ensure that an invalid input class name raises a ValueError.
        """
        self.config.data["step_class_set"]["steps"]["input"] = "InvalidClass"
        with self.assertRaises(ValueError):
            _ = load_step1_input_dataset(self.config)


class TestSummaryClassLoader(unittest.TestCase):
    """
    Tests related to loading the SummaryDataSetA class.
    """

    def setUp(self):
        """
        Define the path to the test config file, select a dataset,
        and set up the test data file path prior to each test.
        """
        self.config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_dataset_001.yaml"
        )
        self.config = DataSetConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")
        self.test_data_file = (
            Path(__file__).resolve().parent
            / "data"
            / "input"
            / "nrt_cora_bo_test.parquet"
        )

    def test_load_dataset_valid_config(self):
        """
        Check that load_step2_summary_dataset returns a SummaryDataSetA instance
        with the correct step name.
        """
        ds = load_step2_summary_dataset(self.config)
        self.assertIsInstance(ds, SummaryDataSetA)
        self.assertEqual(ds.step_name, "summary")

    def test_load_dataset_input_data(self):
        """
        Check that load_step2_summary_dataset sets input_data properly
        when provided and retains its expected structure.
        """
        ds_input = load_step1_input_dataset(self.config)
        ds_input.input_file_name = str(self.test_data_file)
        ds_input.read_input_data()

        ds = load_step2_summary_dataset(self.config, ds_input.input_data)
        self.assertIsInstance(ds, SummaryDataSetA)
        self.assertIsInstance(ds.input_data, pl.DataFrame)
        self.assertEqual(ds.input_data.shape[0], 132342)
        self.assertEqual(ds.input_data.shape[1], 30)


class TestSelectClassLoader(unittest.TestCase):
    """
    Tests related to loading the SelectDataSetA class.
    """

    def setUp(self):
        """
        Define the path to the test config file, select a dataset,
        and set up the test data file path prior to each test.
        """
        self.config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_dataset_001.yaml"
        )
        self.config = DataSetConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")
        self.test_data_file = (
            Path(__file__).resolve().parent
            / "data"
            / "input"
            / "nrt_cora_bo_test.parquet"
        )

    def test_load_dataset_valid_config(self):
        """
        Check that load_step3_select_dataset returns a SelectDataSetA instance
        with the correct step name.
        """
        ds = load_step3_select_dataset(self.config)
        self.assertIsInstance(ds, SelectDataSetA)
        self.assertEqual(ds.step_name, "select")

    def test_load_dataset_input_data(self):
        """
        Check that load_step3_select_dataset sets input_data properly
        when provided and retains its expected structure.
        """
        ds_input = load_step1_input_dataset(self.config)
        ds_input.input_file_name = str(self.test_data_file)
        ds_input.read_input_data()

        ds = load_step3_select_dataset(self.config, ds_input.input_data)
        self.assertIsInstance(ds, SelectDataSetA)
        self.assertIsInstance(ds.input_data, pl.DataFrame)
        self.assertEqual(ds.input_data.shape[0], 132342)
        self.assertEqual(ds.input_data.shape[1], 30)


class TestLocateClassLoader(unittest.TestCase):
    """
    Tests related to loading the LocateDataSetA class.
    """

    def setUp(self):
        """
        Define the path to the test config file, select a dataset,
        and set up the test data file path prior to each test.
        """
        self.config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_dataset_001.yaml"
        )
        self.config = DataSetConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")
        self.test_data_file = (
            Path(__file__).resolve().parent
            / "data"
            / "input"
            / "nrt_cora_bo_test.parquet"
        )

    def test_load_dataset_valid_config(self):
        """
        Check that load_step4_locate_dataset returns a LocateDataSetA instance
        with the correct step name.
        """
        ds = load_step4_locate_dataset(self.config)
        self.assertIsInstance(ds, LocateDataSetA)
        self.assertEqual(ds.step_name, "locate")

    def test_load_dataset_input_data_and_profiles(self):
        """
        Check that load_step4_locate_dataset sets input_data and selected_profiles
        properly when provided and retains their expected structure.
        """
        ds_input = load_step1_input_dataset(self.config)
        ds_input.input_file_name = str(self.test_data_file)
        ds_input.read_input_data()

        ds_select = load_step3_select_dataset(self.config, ds_input.input_data)
        ds_select.label_profiles()

        ds = load_step4_locate_dataset(
            self.config, ds_input.input_data, ds_select.selected_profiles
        )

        self.assertIsInstance(ds, LocateDataSetA)

        self.assertIsInstance(ds.input_data, pl.DataFrame)
        self.assertEqual(ds.input_data.shape[0], 132342)
        self.assertEqual(ds.input_data.shape[1], 30)

        self.assertIsInstance(ds.selected_profiles, pl.DataFrame)
        self.assertEqual(ds.selected_profiles.shape[0], 50)
        self.assertEqual(ds.selected_profiles.shape[1], 8)


class TestExtractClassLoader(unittest.TestCase):
    """
    Tests related to loading the ExtractDataSetA class.
    """

    def setUp(self):
        """
        Define the path to the test config file, select a dataset,
        and set up the test data file path prior to each test.
        """
        self.config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_dataset_001.yaml"
        )
        self.config = DataSetConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")
        self.test_data_file = (
            Path(__file__).resolve().parent
            / "data"
            / "input"
            / "nrt_cora_bo_test.parquet"
        )

    def test_load_dataset_valid_config(self):
        """
        Check that load_step5_extract_dataset returns an ExtractDataSetA instance
        with the correct step name.
        """
        ds = load_step5_extract_dataset(self.config)
        self.assertIsInstance(ds, ExtractDataSetA)
        self.assertEqual(ds.step_name, "extract")

    def test_load_dataset_input_data_and_profiles(self):
        """
        Check that load_step5_extract_dataset correctly initializes the dataset
        with provided inputs and that derived attributes (e.g., `filtered_input`,
        `selected_rows`) are properly set and retain their expected structure.
        """
        ds_input = load_step1_input_dataset(self.config)
        ds_input.input_file_name = str(self.test_data_file)
        ds_input.read_input_data()

        ds_select = load_step3_select_dataset(self.config, ds_input.input_data)
        ds_select.label_profiles()

        ds_summary = load_step2_summary_dataset(self.config, ds_input.input_data)
        ds_summary.calculate_stats()

        ds_locate = load_step4_locate_dataset(
            self.config, ds_input.input_data, ds_select.selected_profiles
        )
        ds_locate.process_targets()

        ds = load_step5_extract_dataset(
            self.config,
            ds_input.input_data,
            ds_select.selected_profiles,
            ds_locate.selected_rows,
            ds_summary.summary_stats,
        )

        self.assertIsInstance(ds, ExtractDataSetA)

        self.assertIsInstance(ds.input_data, pl.DataFrame)
        self.assertEqual(ds.input_data.shape[0], 132342)
        self.assertEqual(ds.input_data.shape[1], 30)

        self.assertIsInstance(ds.summary_stats, pl.DataFrame)
        self.assertEqual(ds.summary_stats.shape[0], 2520)
        self.assertEqual(ds.summary_stats.shape[1], 12)

        self.assertIsInstance(ds.selected_profiles, pl.DataFrame)
        self.assertEqual(ds.selected_profiles.shape[0], 50)
        self.assertEqual(ds.selected_profiles.shape[1], 8)

        self.assertIsInstance(ds.filtered_input, pl.DataFrame)
        self.assertEqual(ds.filtered_input.shape[0], 10683)
        self.assertEqual(ds.filtered_input.shape[1], 30)

        self.assertIsInstance(ds.selected_rows["temp"], pl.DataFrame)
        self.assertEqual(ds.selected_rows["temp"].shape[0], 128)
        self.assertEqual(ds.selected_rows["temp"].shape[1], 9)

        self.assertIsInstance(ds.selected_rows["psal"], pl.DataFrame)
        self.assertEqual(ds.selected_rows["psal"].shape[0], 140)
        self.assertEqual(ds.selected_rows["psal"].shape[1], 9)


class TestSplitClassLoader(unittest.TestCase):
    """
    Tests related to loading the SplitDataSetA class.
    """

    def setUp(self):
        """
        Define the path to the test config file, select a dataset,
        and set up the test data file path prior to each test.
        """
        self.config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_dataset_001.yaml"
        )
        self.config = DataSetConfig(str(self.config_file_path))
        self.config.select("NRT_BO_001")
        self.test_data_file = (
            Path(__file__).resolve().parent
            / "data"
            / "input"
            / "nrt_cora_bo_test.parquet"
        )

    def test_load_dataset_valid_config(self):
        """
        Check that load_step6_split_dataset returns a SplitDataSetA instance
        with the correct step name.
        """
        ds = load_step6_split_dataset(self.config)
        self.assertIsInstance(ds, SplitDataSetA)
        self.assertEqual(ds.step_name, "split")

    def test_load_dataset_input_data(self):
        """
        Check that load_step6_split_dataset properly sets the `target_features`
        input provided from previous steps and retains its expected structure.
        """
        ds_input = load_step1_input_dataset(self.config)
        ds_input.input_file_name = str(self.test_data_file)
        ds_input.read_input_data()

        ds_select = load_step3_select_dataset(self.config, ds_input.input_data)
        ds_select.label_profiles()

        ds_summary = load_step2_summary_dataset(self.config, ds_input.input_data)
        ds_summary.calculate_stats()

        ds_locate = load_step4_locate_dataset(
            self.config, ds_input.input_data, ds_select.selected_profiles
        )
        ds_locate.process_targets()

        ds_extract = load_step5_extract_dataset(
            self.config,
            ds_input.input_data,
            ds_select.selected_profiles,
            ds_locate.selected_rows,
            ds_summary.summary_stats,
        )
        ds_extract.process_targets()

        ds = load_step6_split_dataset(self.config, ds_extract.target_features)

        self.assertIsInstance(ds, SplitDataSetA)

        self.assertIsInstance(ds.target_features["temp"], pl.DataFrame)
        self.assertEqual(ds.target_features["temp"].shape[0], 128)
        self.assertEqual(ds.target_features["temp"].shape[1], 58)

        self.assertIsInstance(ds.target_features["psal"], pl.DataFrame)
        self.assertEqual(ds.target_features["psal"].shape[0], 140)
        self.assertEqual(ds.target_features["psal"].shape[1], 58)
