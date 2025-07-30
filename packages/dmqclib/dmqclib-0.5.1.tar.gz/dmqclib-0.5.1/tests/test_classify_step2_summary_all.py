"""Unit tests for the SummaryDataSetAll class.

This module contains tests for verifying the correct functionality of
SummaryDataSetAll, including output file name generation, data loading,
and the calculation of global and profile-specific statistics.
"""

import os
import unittest
from pathlib import Path

import polars as pl

from dmqclib.classify.step2_calc_stats.dataset_all import SummaryDataSetAll
from dmqclib.common.config.classify_config import ClassificationConfig
from dmqclib.common.loader.classify_loader import load_classify_step1_input_dataset


class TestSummaryDataSetAll(unittest.TestCase):
    """
    A suite of tests for verifying summary dataset operations in SummaryDataSetAll.
    Ensures output filenames, data loading, and profile/statistical calculations
    function as expected.
    """

    def setUp(self):
        """Set up test environment and load input dataset.

        Initializes configuration and loads a sample input dataset
        for use across multiple tests.
        """
        self.config_file_path = str(
            Path(__file__).resolve().parent
            / "data"
            / "config"
            / "test_classify_001.yaml"
        )
        self.config = ClassificationConfig(self.config_file_path)
        self.config.select("NRT_BO_001")
        self.test_data_file = (
            Path(__file__).resolve().parent
            / "data"
            / "input"
            / "nrt_cora_bo_test.parquet"
        )
        self.ds = load_classify_step1_input_dataset(self.config)
        self.ds.input_file_name = str(self.test_data_file)
        self.ds.read_input_data()

    def test_output_file_name(self):
        """Verify that the output file name is set correctly based on the configuration."""
        ds = SummaryDataSetAll(self.config)
        self.assertEqual(
            "/path/to/data_1/nrt_bo_001/summary/summary_stats_classify.tsv",
            str(ds.output_file_name),
        )

    def test_step_name(self):
        """Check that the step name attribute is accurately set to 'summary'."""
        ds = SummaryDataSetAll(self.config)
        self.assertEqual(ds.step_name, "summary")

    def test_input_data(self):
        """Confirm that input_data is correctly stored as a Polars DataFrame.

        Also verifies the dimensions (rows and columns) of the loaded data.
        """
        ds = SummaryDataSetAll(self.config, input_data=self.ds.input_data)
        self.assertIsInstance(ds.input_data, pl.DataFrame)
        self.assertEqual(ds.input_data.shape[0], 19480)
        self.assertEqual(ds.input_data.shape[1], 30)

    def test_global_stats(self):
        """Check that calculate_global_stats returns correct columns and row count.

        Ensures the generated global statistics DataFrame has the expected structure.
        """
        ds = SummaryDataSetAll(self.config, input_data=self.ds.input_data)
        df = ds.calculate_global_stats("temp")
        self.assertIsInstance(df, pl.DataFrame)
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df.shape[1], 12)

    def test_profile_stats(self):
        """Check that calculate_profile_stats processes grouped profiles correctly.

        Verifies the dimensions of the DataFrame containing profile-specific statistics.
        """
        ds = SummaryDataSetAll(self.config, input_data=self.ds.input_data)
        grouped_df = ds.input_data.group_by(ds.profile_col_names)
        df = ds.calculate_profile_stats(grouped_df, "temp")
        self.assertEqual(df.shape[0], 84)
        self.assertEqual(df.shape[1], 12)

    def test_summary_stats(self):
        """Check that calculate_stats populates summary_stats with correct dimensions.

        Ensures the final summary statistics DataFrame has the expected number
        of rows and columns after calculation.
        """
        ds = SummaryDataSetAll(self.config, input_data=self.ds.input_data)
        ds.calculate_stats()
        self.assertEqual(ds.summary_stats.shape[0], 425)
        self.assertEqual(ds.summary_stats.shape[1], 12)

    def test_write_summary_stats(self):
        """Confirm that summary statistics are written to file and file creation is verified.

        Creates a temporary file, writes the summary statistics, and then
        checks for its existence before cleaning up.
        """
        ds = SummaryDataSetAll(self.config, input_data=self.ds.input_data)
        ds.output_file_name = str(
            Path(__file__).resolve().parent
            / "data"
            / "summary"
            / "temp_summary_stats_classify.tsv"
        )

        ds.calculate_stats()
        ds.write_summary_stats()
        self.assertTrue(os.path.exists(ds.output_file_name))
        os.remove(ds.output_file_name)

    def test_write_no_summary_stats(self):
        """Ensure ValueError is raised if write_summary_stats is called with empty stats.

        Verifies that attempting to write statistics before they are calculated
        or if they are empty results in a ValueError.
        """
        ds = SummaryDataSetAll(self.config, input_data=self.ds.input_data)

        with self.assertRaises(ValueError):
            ds.write_summary_stats()
