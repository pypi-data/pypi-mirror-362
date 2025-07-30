Dataset Preparation (Configuration)
====================================
The `prepare` workflow (`stage="prepare"`) is central to setting up your data for machine learning tasks within this library. It provides comprehensive control over the entire data processing pipeline, from ingesting raw files and applying advanced feature engineering to meticulously creating the final training, validation, and test datasets.

Core Concepts: Modular Configuration
------------------------------------
The configuration for dataset preparation is designed around a powerful "building blocks" concept. Instead of defining a monolithic configuration, you define various sets of specialized configurations once, give each set a unique name, and then combine them as needed to construct a complete and flexible data processing pipeline. This modularity promotes reusability, simplifies experimentation, and enhances maintainability.

The primary configuration sections (building blocks) are:

*   **`path_info_sets`**: Defines reusable directory structures for input data and processed outputs.
*   **`target_sets`**: Specifies the prediction target variables, including their quality control (QC) flags.
*   **`summary_stats_sets`**: Configures summary statistics essential for normalizing feature values.
*   **`feature_sets`**: Lists the specific feature engineering methods to be applied.
*   **`feature_param_sets`**: Provides detailed parameters and settings for each chosen feature engineering method.
*   **`step_class_sets`**: (**Advanced**) Allows users to define custom Python classes for individual processing steps, enabling deep customization of the pipeline's behavior.
*   **`step_param_sets`**: Supplies general parameters that control the behavior of the default or custom processing steps.
*   **`data_sets`**: The central assembly section, where you combine named blocks from the sections above to define a complete and executable data processing pipeline.

Detailed Configuration Sections
-------------------------------

`path_info_sets`
^^^^^^^^^^^^^^^^
This section defines the critical file system locations for both your raw input data and the various processed output artifacts. You can define multiple named path configurations to easily switch between different storage environments or project setups.

*   **`common.base_path`**: The root directory where all processed data and intermediate artifacts will be saved by this workflow.
*   **`input.base_path`**: The directory containing your raw input data files.
*   **`split.step_folder_name`**: The name of the subdirectory where the final training, validation, and test datasets will be stored (e.g., `training`).

.. code-block:: yaml

   path_info_sets:
     - name: data_set_1
       common:
         base_path: /path/to/data
       input:
         base_path: /path/to/input
         step_folder_name: ""
       split:
         step_folder_name: training

`target_sets`
^^^^^^^^^^^^^
This section specifies the target variables that your machine learning model will predict. For each target variable, you must also define its corresponding quality control (QC) flag column. These flags are crucial for identifying good versus bad data points, allowing the pipeline to filter or weight data appropriately. You define both positive (good) and negative (bad) flag values.

.. code-block:: yaml

   target_sets:
     - name: target_set_1_3
       variables:
         - name: temp
           flag: temp_qc
           pos_flag_values: [3, 4, 5, 6, 7, 8, 9]
           neg_flag_values: [1, 2]

`summary_stats_sets`
^^^^^^^^^^^^^^^^^^^^
This section defines summary statistics that will be used for normalization or scaling of feature values. These statistics are typically derived from your dataset itself to ensure proper scaling. The `dmqclib` (Data Management Quality Control Library) provides convenient functions (`get_summary_stats` and `format_summary_stats`) to calculate and format these statistics directly from your input data, making it easy to populate this section.

.. code-block:: yaml

   summary_stats_sets:
     - name: summary_stats_set_1
       stats:
         - name: location
           min_max: { longitude: { min: 14.5, max: 23.5 },
                      latitude: { min: 55, max: 66 } }

The following Python commands, utilizing `dmqclib`, can provide all necessary information to update the values in `summary_stats_sets` based on your actual data:

.. code-block:: python

   import dmqclib as dm

   input_file = "~/aiqc_project/input/nrt_cora_bo_4.parquet"

   stats_all = dm.get_summary_stats(input_file, "all")
   print(dm.format_summary_stats(stats_all))

   stats_profiles = dm.get_summary_stats(input_file, "profiles")
   print(dm.format_summary_stats(stats_profiles))

`feature_sets` & `feature_param_sets`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These two interconnected sections are dedicated to configuring your feature engineering process.

*   **`feature_sets`**: This block lists the *names* of the specific feature engineering methods you want to apply to your data.
*   **`feature_param_sets`**: This block provides the detailed parameters and configurations for each of the feature methods listed in your chosen `feature_sets` block. This allows for fine-grained control over how each feature is generated.

.. code-block:: yaml

   # A list of features to apply
   feature_sets:
     - name: feature_set_1
       features:
         - location
         - day_of_year
         - profile_summary_stats5
         - basic_values
         - flank_up
         - flank_down

   # Parameters for the features listed above
   feature_param_sets:
     - name: feature_set_1_param_set_3
       params:
         - feature: location
           stats_set: {name: location, type: min_max}
         - feature: day_of_year
           convert: sine
         - feature: profile_summary_stats5
           stats_set: { name: profile_summary_stats5, type: min_max }
         - feature: basic_values
           stats_set: {name: basic_values3, type: min_max}
         - feature: flank_up
           flank_up: 5
           stats_set: {name: basic_values3, type: min_max}
         - feature: flank_down
           flank_down: 5
           stats_set: {name: basic_values3, type: min_max}

`step_class_sets`
^^^^^^^^^^^^^^^^^
(**Advanced Use**)
This section allows you to define and reference custom Python classes that implement the logic for specific processing steps within the data preparation pipeline. While the library provides default implementations for all steps, this block gives advanced users the flexibility to replace or extend pipeline behaviors with their own code. Each entry maps a step name (e.g., `input`, `summary`) to the name of a Python class.

.. code-block:: yaml

   step_class_sets:
     - name: data_set_step_set_1
       steps:
         input: InputDataSetA
         summary: SummaryDataSetA
         select: SelectDataSetA
         locate: LocateDataSetA
         extract: ExtractDataSetA
         split: SplitDataSetA

`step_param_sets`
^^^^^^^^^^^^^^^^^
This section provides general parameters that control the behavior of the various data processing steps within the pipeline (whether default or custom `step_class_sets`). Examples of parameters include data filtering rules, sampling ratios, and split configurations.

*   **`steps.input.sub_steps.filter_rows`**: A boolean flag to enable/disable row filtering.
*   **`steps.input.filter_method_dict.remove_years`**: Specifies a list of years to be excluded from the dataset.
*   **`steps.select.neg_pos_ratio`**: Controls the ratio of negative to positive samples (e.g., for imbalanced datasets).
*   **`steps.split.test_set_fraction`**: Defines the proportion of data to allocate to the test set.

.. code-block:: yaml

   step_param_sets:
     - name: data_set_param_set_1
       steps:
         input: { sub_steps: { rename_columns: false,
                               filter_rows: true },
                  rename_dict: { },
                  filter_method_dict: { remove_years: [2023],
                                        keep_years: [] } }
         summary: { }
         select: { neg_pos_ratio: 5 }
         locate: { neighbor_n: 5 }
         extract: { }
         split: { test_set_fraction: 0.1,
                  k_fold: 10 }

`data_sets`
^^^^^^^^^^^
This is the main "pipeline assembly" section. Each entry in this list defines a complete data preparation job by linking together the named building blocks defined in the other sections. This section essentially orchestrates which specific configuration sets are used for a given dataset processing run.

*   **`name`**: A unique identifier for this particular dataset preparation job (e.g., `dataset_0001`).
*   **`dataset_folder_name`**: The name of the specific folder that will be created within the `common.base_path` to store outputs for this job (e.g., `dataset_0001`).
*   **`input_file_name`**: The specific raw data file (located in `input.base_path`) to be processed for this job.
*   **`path_info`**: The `name` of the path configuration to use from `path_info_sets`.
*   **`target_set`**: The `name` of the target configuration to use from `target_sets`.
*   ...and similarly for all other configuration sets.

.. code-block:: yaml

   data_sets:
     - name: dataset_0001
       dataset_folder_name: dataset_0001
       input_file_name: nrt_cora_bo_4.parquet
       path_info: data_set_1
       target_set: target_set_1_3
       # ... other set references would follow here

Full Example
------------

Below is a complete example of a `prepare_config.yaml` file, demonstrating how all the building blocks are combined. The lines you will most commonly need to edit or customize are highlighted for quick reference.

.. code-block:: yaml
   :caption: Full prepare_config.yaml example
   :emphasize-lines: 5, 7, 30, 97, 99, 109, 110, 111

   ---
   path_info_sets:
     - name: data_set_1
       common:
         base_path: /path/to/data # Root output directory for processed data
       input:
         base_path: /path/to/input # Directory containing raw input files
         step_folder_name: ""
       split:
         step_folder_name: training

   target_sets:
     - name: target_set_1_3
       variables:
         - name: temp
           flag: temp_qc
           pos_flag_values: [3, 4, 5, 6, 7, 8, 9]
           neg_flag_values: [1, 2]
         - name: psal
           flag: psal_qc
           pos_flag_values: [3, 4, 5, 6, 7, 8, 9]
           neg_flag_values: [1, 2]
         - name: pres
           flag: pres_qc
           pos_flag_values: [3, 4, 5, 6, 7, 8, 9]
           neg_flag_values: [1, 2]

   summary_stats_sets:
     - name: summary_stats_set_1
       stats:
         - name: location
           min_max: { longitude: { min: 14.5, max: 23.5 },
                      latitude: { min: 55, max: 66 } }
         - name: profile_summary_stats5
           min_max: { temp: { mean: { min: 0, max: 12.5 },
                              median: { min: 0, max: 15 },
                              sd: { min: 0, max: 6.5 },
                              pct25: { min: 0, max: 12 },
                              pct75: { min: 1, max: 19 } },
                      psal: { mean: { min: 2.9, max: 12 },
                              median: { min: 2.9, max: 12 },
                              sd: { min: 0, max: 4 },
                              pct25: { min: 2.5, max: 8.5 },
                              pct75: { min: 3, max: 16 } },
                      pres: { mean: { min: 24, max: 105 },
                              median: { min: 24, max: 105 },
                              sd: { min: 13, max: 60 },
                              pct25: { min: 12, max: 53 },
                              pct75: { min: 35, max: 156 } } }
         - name: basic_values3
           min_max: { temp: { min: 0, max: 20 },
                      psal: { min: 0, max: 20 },
                      pres: { min: 0, max: 200 } }

   feature_sets:
     - name: feature_set_1
       features:
         - location
         - day_of_year
         - profile_summary_stats5
         - basic_values
         - flank_up
         - flank_down

   feature_param_sets:
     - name: feature_set_1_param_set_3
       params:
         - feature: location
           stats_set: {name: location, type: min_max}
         - feature: day_of_year
           convert: sine
         - feature: profile_summary_stats5
           stats_set: { name: profile_summary_stats5, type: min_max }
         - feature: basic_values
           stats_set: {name: basic_values3, type: min_max}
         - feature: flank_up
           flank_up: 5
           stats_set: {name: basic_values3, type: min_max}
         - feature: flank_down
           flank_down: 5
           stats_set: {name: basic_values3, type: min_max}

   step_class_sets:
     - name: data_set_step_set_1
       steps:
         input: InputDataSetA
         summary: SummaryDataSetA
         select: SelectDataSetA
         locate: LocateDataSetA
         extract: ExtractDataSetA
         split: SplitDataSetA

   step_param_sets:
     - name: data_set_param_set_1
       steps:
         input: { sub_steps: { rename_columns: false,
                               filter_rows: true },
                  rename_dict: { },
                  filter_method_dict: { remove_years: [2023],
                                        keep_years: [] } }
         summary: { }
         select: { neg_pos_ratio: 5 }
         locate: { neighbor_n: 5 }
         extract: { }
         split: { test_set_fraction: 0.1,
                  k_fold: 10 }

   data_sets:
     - name: dataset_0001  # Your unique name for this dataset job
       dataset_folder_name: dataset_0001  # The folder name for output files
       input_file_name: nrt_cora_bo_4.parquet # The specific raw input file to process
       path_info: data_set_1
       target_set: target_set_1_3
       summary_stats_set: summary_stats_set_1
       feature_set: feature_set_1
       feature_param_set: feature_set_1_param_set_3
       step_class_set: data_set_step_set_1
       step_param_set: data_set_param_set_1
