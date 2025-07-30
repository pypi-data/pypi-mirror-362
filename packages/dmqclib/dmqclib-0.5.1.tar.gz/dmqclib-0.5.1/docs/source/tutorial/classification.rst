Step 4: Classification
======================

You have successfully prepared a dataset and trained a machine learning model. The final step in the ``dmqclib`` workflow is to put that model to work by classifying a new, unseen dataset. This workflow applies your pre-trained model to every observation in an input file, adding model predictions and probability scores as new columns.

This is the culmination of the ``dmqclib`` pipeline, transforming your machine learning model into a practical tool for real-time data analysis and quality control.

.. admonition:: Prerequisites

   This tutorial assumes you have successfully completed :doc:`./training`. To proceed with classification, you will need:

   *   The trained model file(s) saved in the directory you specified in the training configuration (e.g., `~/aiqc_project/models/`).
   *   The original raw data file (``nrt_cora_bo_4.parquet``) that you wish to classify. This file should be in your `~/aiqc_project/input/` directory.

The Classification Workflow
---------------------------

The classification process follows the familiar ``dmqclib`` pattern: you will generate a configuration template, customize it to point to your input data, the trained model, and the desired output location, and then execute the classification script.

Step 4.1: Generate the Configuration Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, use ``dmqclib`` to generate the boilerplate configuration template specifically for the `classify` workflow.

.. code-block:: python

   import dmqclib as dm
   import os

   # Define the path for the config file
   config_path = os.path.expanduser("~/aiqc_project/config/classification_config.yaml")

   # This creates 'classification_config.yaml' in '~/aiqc_project/config'
   dm.write_config_template(
       file_name=config_path,
       stage="classify"
   )
   print(f"Configuration template generated at: {config_path}")


Step 4.2: Customize the Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open the newly created ``~/aiqc_project/config/classification_config.yaml`` file in your text editor. You need to configure the paths for the raw input data, the location of your trained model, and where the final classified output should be saved.

**Crucially, the `target_sets`, `summary_stats_sets`, `feature_sets`, and `feature_param_sets` in this classification configuration MUST EXACTLY MATCH those used in your `prepare_config.yaml` for the model's training.** This ensures that the new input data is preprocessed and features are engineered in precisely the same way the model expects. You can often copy these sections directly from your `prepare_config.yaml`.

Update your `classification_config.yaml` file to match the following. Remember to replace placeholder paths and details with your actual project setup.

.. code-block:: yaml

    path_info_sets:
      - name: data_set_1
        common:
          base_path: ~/aiqc_project/data # Root directory for all processed outputs for this job
        input:
          base_path: ~/aiqc_project/input # Directory containing the raw input files to classify
          step_folder_name: "" # Set to "" if input files are directly in base_path
        model:
          base_path: ~/aiqc_project/models # Directory containing your trained model file(s) from the training step
        concat:
          step_folder_name: classify # Subdirectory within common.base_path for the final classified output

.. code-block:: yaml

    # These sections should be copied from your prepare_config.yaml used for model training
    # For example:
    # target_sets:
    #   - name: target_set_1_3
    #     variables: ...
    # summary_stats_sets:
    #   - name: summary_stats_set_1
    #     stats: ...
    # feature_sets:
    #   - name: feature_set_1
    #     features: ...
    # feature_param_sets:
    #   - name: feature_set_1_param_set_3
    #     params: ...

    # If you have custom step classes, ensure these match your training setup.
    # step_class_sets:
    #   - name: data_set_step_set_1
    #     steps: ...

    # Configure any specific parameters for classification steps (e.g., input filters)
    # step_param_sets:
    #   - name: data_set_param_set_1
    #     steps: ...

.. code-block:: yaml

    classification_sets:
      - name: classification_0001  # A unique name for this classification task
        dataset_folder_name: dataset_0001  # This MUST match the dataset_folder_name used during preparation and training
        input_file_name: nrt_cora_bo_4.parquet   # The specific raw input filename to classify
        path_info: data_set_1
        target_set: target_set_1_3
        summary_stats_set: summary_stats_set_1
        feature_set: feature_set_1
        feature_param_set: feature_set_1_param_set_3
        step_class_set: data_set_step_set_1
        step_param_set: data_set_param_set_1

.. note::
   The classification configuration file is comprehensive and has many options similar to both preparation and training configurations. For a complete reference of all available parameters, please consult the dedicated :doc:`../../configuration/classification` page.

Step 4.3: Run the Classification Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have customized your `classification_config.yaml` with the correct paths, input file, and inherited configuration references, you can execute the classification workflow.

Load the configuration file and then call the `classify_dataset` function:

.. code-block:: python

   import dmqclib as dm
   import os

   config_path = os.path.expanduser("~/aiqc_project/config/classification_config.yaml")
   config = dm.read_config(config_path)
   dm.classify_dataset(config)
   print(f"Classification complete! Outputs saved to: {os.path.join(config.path_info_sets[0].common.base_path, config.classification_sets[0].dataset_folder_name, config.path_info_sets[0].concat.step_folder_name)}")

Understanding the Output
------------------------

After the command finishes, your output root directory (e.g., `~/aiqc_project/data`) will contain a new folder named `dataset_0001` (from `classification_sets.dataset_folder_name`). Inside `dataset_0001`, you will find several subdirectories, reflecting the processing steps:

*   **`summary`**: Contains intermediate files with summary statistics if re-calculated or referenced.
*   **`select`**: Stores the input profiles after any initial filtering. In classification, this typically includes all profiles you want to classify.
*   **`locate`**: Contains all observation records that proceeded through the pipeline, often after proximity-based selection for feature generation.
*   **`extract`**: Holds the features extracted from the observation records, transformed consistently with how the model was trained.
*   **`classify`**: (Defined by `path_info_sets.concat.step_folder_name`) This is the final output directory. It contains:
    *   A `.parquet` file with the original input data, augmented with new columns for the model's predictions (e.g., `temp_prediction`) and prediction probabilities (e.g., `temp_probability`).
    *   Potentially, a summary report detailing the classification results.

Conclusion
----------

Congratulations! You have successfully completed the entire ``dmqclib`` workflow, from raw data preparation to training a machine learning model and then using it to generate predictions on new data.

You now have a powerful, repeatable, and configurable pipeline for your machine learning tasks. You can easily adapt the configuration files to process new datasets, experiment with different models and features, or integrate this into larger automated workflows.
