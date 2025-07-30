"""Unit tests for the SummaryDataSetA class, covering output file handling,
data loading, and statistical calculations."""

import os
import unittest
from pathlib import Path

import polars as pl

from dmqclib.common.config.dataset_config import DataSetConfig
from dmqclib.common.loader.dataset_loader import load_step1_input_dataset
from dmqclib.prepare.step2_calc_stats.dataset_a import SummaryDataSetA


class TestSelectDataSetA(unittest.TestCase):
    """
    A suite of tests for verifying summary dataset operations in SummaryDataSetA.
    Ensures output filenames, data loading, and profile/statistical calculations
    function as expected.
    """

    def setUp(self):
        """Set up test environment by loading configuration and input dataset."""
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
        self.ds = load_step1_input_dataset(self.config)
        self.ds.input_file_name = str(self.test_data_file)
        self.ds.read_input_data()

    def test_output_file_name(self):
        """Verify that the output file name is set correctly based on the configuration."""
        ds = SummaryDataSetA(self.config)
        self.assertEqual(
            "/path/to/data_1/nrt_bo_001/summary/summary_stats.tsv",
            str(ds.output_file_name),
        )

    def test_default_output_file_name(self):
        """Verify that a default output file name is correctly set when `output_file_name` is not specified in the configuration."""
        config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_dataset_002.yaml"
        )
        config = DataSetConfig(config_file_path)
        config.select("NRT_BO_001")

        ds = SummaryDataSetA(config)
        self.assertEqual(
            "/path/to/data_1/summary_dataset_folder/summary/summary_in_params.txt",
            str(ds.output_file_name),
        )

    def test_step_name(self):
        """Check that the step name attribute is accurately set to 'summary'."""
        ds = SummaryDataSetA(self.config)
        self.assertEqual(ds.step_name, "summary")

    def test_input_data(self):
        """Confirm that `input_data` is correctly stored as a Polars DataFrame with expected dimensions."""
        ds = SummaryDataSetA(self.config, input_data=self.ds.input_data)
        self.assertIsInstance(ds.input_data, pl.DataFrame)
        self.assertEqual(ds.input_data.shape[0], 132342)
        self.assertEqual(ds.input_data.shape[1], 30)

    def test_global_stats(self):
        """Check that `calculate_global_stats` returns a Polars DataFrame with the correct columns and row count."""
        ds = SummaryDataSetA(self.config, input_data=self.ds.input_data)
        df = ds.calculate_global_stats("temp")
        self.assertIsInstance(df, pl.DataFrame)
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df.shape[1], 12)

    def test_profile_stats(self):
        """Check that `calculate_profile_stats` correctly processes grouped profiles and returns a DataFrame of expected dimensions."""
        ds = SummaryDataSetA(self.config, input_data=self.ds.input_data)
        grouped_df = ds.input_data.group_by(ds.profile_col_names)
        df = ds.calculate_profile_stats(grouped_df, "temp")
        self.assertEqual(df.shape[0], 503)
        self.assertEqual(df.shape[1], 12)

    def test_summary_stats(self):
        """Check that `calculate_stats` correctly populates `summary_stats` with the expected dimensions."""
        ds = SummaryDataSetA(self.config, input_data=self.ds.input_data)
        ds.calculate_stats()
        self.assertEqual(ds.summary_stats.shape[0], 2520)
        self.assertEqual(ds.summary_stats.shape[1], 12)

    def test_write_summary_stats(self):
        """Confirm that `summary_stats` are successfully written to a file and the file's existence is verified."""
        ds = SummaryDataSetA(self.config, input_data=self.ds.input_data)
        ds.output_file_name = str(
            Path(__file__).resolve().parent
            / "data"
            / "summary"
            / "temp_summary_stats.tsv"
        )

        ds.calculate_stats()
        ds.write_summary_stats()
        self.assertTrue(os.path.exists(ds.output_file_name))
        os.remove(ds.output_file_name)

    def test_write_no_summary_stats(self):
        """Ensure `ValueError` is raised if `write_summary_stats` is called when `summary_stats` is empty."""
        ds = SummaryDataSetA(self.config, input_data=self.ds.input_data)

        with self.assertRaises(ValueError):
            ds.write_summary_stats()

    def test_summary_stats_observation(self):
        """Check that `create_summary_stats_observation` calculates observation-level summary statistics correctly with expected dimensions."""
        ds = SummaryDataSetA(self.config, input_data=self.ds.input_data)
        ds.calculate_stats()
        ds.create_summary_stats_observation()
        self.assertEqual(ds.summary_stats_observation.shape[0], 5)
        self.assertEqual(ds.summary_stats_observation.shape[1], 5)

    def test_summary_stats_observation_without_stats_ds(self):
        """Ensure `ValueError` is raised if `create_summary_stats_observation` is called when `summary_stats` is empty."""
        ds = SummaryDataSetA(self.config, input_data=self.ds.input_data)
        with self.assertRaises(ValueError):
            ds.create_summary_stats_observation()

    def test_summary_stats_profile(self):
        """Check that `create_summary_stats_profile` calculates profile-level summary statistics correctly with expected dimensions."""
        ds = SummaryDataSetA(self.config, input_data=self.ds.input_data)
        ds.calculate_stats()
        ds.create_summary_stats_profile()
        self.assertEqual(ds.summary_stats_profile.shape[0], 27)
        self.assertEqual(ds.summary_stats_profile.shape[1], 6)

    def test_summary_stats_profile_without_stats_ds(self):
        """Ensure `ValueError` is raised if `create_summary_stats_profile` is called when `summary_stats` is empty."""
        ds = SummaryDataSetA(self.config, input_data=self.ds.input_data)
        with self.assertRaises(ValueError):
            ds.create_summary_stats_profile()
