"""
Module providing YAML templates for both dataset preparation
and training configurations. These templates can be customized
to fit various data pipeline requirements.
"""


def get_config_data_set_template() -> str:
    """
    Retrieve a YAML template string for dataset preparation configurations.

    This template includes:

    - ``path_info_sets``: specifying common, input, and split paths.
    - ``target_sets``: defining which variables to process and their flags.
    - ``summary_stats_sets``: defining summary statistics for normalization.
    - ``feature_sets``: listing named sets of feature extraction modules.
    - ``feature_param_sets``: detailing parameters for each feature.
    - ``step_class_sets``: referencing classes for each preparation step
      (e.g., input, summary, select, locate, extract, split).
    - ``step_param_sets``: referencing parameters for the preparation steps.
    - ``data_sets``: referencing specific dataset folders, files, and
      associated configuration sets (e.g., ``step_class_set``, ``step_param_set``).

    :returns: A string containing the YAML template.
    :rtype: str
    """
    yaml_template = """
---
path_info_sets:
  - name: data_set_1
    common:
      base_path: /path/to/data # EDIT: Root output directory
    input:
      base_path: /path/to/input # EDIT: Directory with input files
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

summary_stats_sets: # EDIT: Summary stats for normalisation
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
        stats_set: {name: profile_summary_stats5, type: min_max}
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
  - name: dataset_0001  # EDIT: Your data set name
    dataset_folder_name: dataset_0001  # EDIT: Your output folder
    input_file_name: nrt_cora_bo_4.parquet # EDIT: Your input filename
    path_info: data_set_1
    target_set: target_set_1_3
    summary_stats_set: summary_stats_set_1
    feature_set: feature_set_1
    feature_param_set: feature_set_1_param_set_3
    step_class_set: data_set_step_set_1
    step_param_set: data_set_param_set_1
"""
    return yaml_template


def get_config_train_set_template() -> str:
    """
    Retrieve a YAML template string for training configurations.

    This template includes:

    - ``path_info_sets``: specifying common paths and subfolders for input, validate, and build.
    - ``target_sets``: defining variables and associated flags for training.
    - ``step_class_sets``: mapping each step (input, validate, model, build)
      to corresponding Python class names.
    - ``step_param_sets``: detailing optional parameters for each training step.
    - ``training_sets``: referencing specific dataset folders, the ``path_info`` used,
      the target set, and which ``step_class_set`` and ``step_param_set`` apply.

    :returns: A string containing the YAML template.
    :rtype: str
    """
    yaml_template = """
---
path_info_sets:
  - name: data_set_1
    common:
      base_path: /path/to/data # EDIT: Root output directory
    input:
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

step_class_sets:
  - name: training_step_set_1
    steps:
      input: InputTrainingSetA
      validate: KFoldValidation
      model: XGBoost
      build: BuildModel

step_param_sets:
  - name: training_param_set_1
    steps:
      input: { }
      validate: { k_fold: 10 }
      model: { model_params: { scale_pos_weight: 200 } }
      build: { }

training_sets:
  - name: training_0001  # EDIT: Your training name
    dataset_folder_name: dataset_0001  # EDIT: Your output folder
    path_info: data_set_1
    target_set: target_set_1_3
    step_class_set: training_step_set_1
    step_param_set: training_param_set_1
"""
    return yaml_template


def get_config_classify_set_template() -> str:
    """
    Retrieve a YAML template string for classification configurations.

    This template includes:

    - ``path_info_sets``: specifying common, input, model, and concatenation paths.
    - ``target_sets``: defining which variables to process and their flags.
    - ``summary_stats_sets``: defining summary statistics for normalization.
    - ``feature_sets``: listing named sets of feature extraction modules.
    - ``feature_param_sets``: detailing parameters for each feature.
    - ``step_class_sets``: referencing classes for each classification step
      (e.g., input, summary, select, locate, extract, model, classify, concat).
    - ``step_param_sets``: referencing parameters for the classification steps.
    - ``classification_sets``: referencing specific dataset folders, files, and
      associated configuration sets (e.g., ``step_class_set``, ``step_param_set``).

    :returns: A string containing the YAML template.
    :rtype: str
    """
    yaml_template = """
---
path_info_sets:
  - name: data_set_1
    common:
      base_path: /path/to/data # EDIT: Root output directory
    input:
      base_path: /path/to/input # EDIT: Directory with input files
      step_folder_name: ""
    model:
      base_path: /path/to/model  # EDIT: Directory with model files
    concat:
      step_folder_name: classify # EDIT: Directory with classification results

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

summary_stats_sets: # EDIT: Summary stats for normalisation
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
        stats_set: {name: profile_summary_stats5, type: min_max}
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
      input: InputDataSetAll
      summary: SummaryDataSetAll
      select: SelectDataSetAll
      locate: LocateDataSetAll
      extract: ExtractDataSetAll
      model: XGBoost
      classify: ClassifyAll
      concat: ConcatDataSetAll

step_param_sets:
  - name: data_set_param_set_1
    steps:
      input: { sub_steps: { rename_columns: false,
                            filter_rows: true },
               rename_dict: { },
               filter_method_dict: { remove_years: [],
                                     keep_years: [2023] } }
      summary: { }
      select: { }
      locate: { }
      extract: { }
      model: { }
      classify: { }
      concat: { }

classification_sets:
  - name: classification_0001  # EDIT: Your classification name
    dataset_folder_name: dataset_0001  # EDIT: Your output folder
    input_file_name: nrt_cora_bo_4.parquet   # EDIT: Your input filename
    path_info: data_set_1
    target_set: target_set_1_3
    summary_stats_set: summary_stats_set_1
    feature_set: feature_set_1
    feature_param_set: feature_set_1_param_set_3
    step_class_set: data_set_step_set_1
    step_param_set: data_set_param_set_1
"""
    return yaml_template
