Welcome to the dmqclib documentation!
=======================================

**dmqclib** is a Python library that provides a configuration-driven workflow for machine learning, simplifying dataset preparation, model training, and data classification. It is a core component of the AIQC project.

The library is designed around a three-stage workflow:

1.  **Dataset Preparation:** Ingest raw data and transform it into a feature-rich dataset ready for training.
2.  **Training & Evaluation:** Train machine learning models and evaluate their performance using cross-validation.
3.  **Classification:** Apply a trained model to classify new, unseen data.

Each stage is controlled by a YAML configuration file, allowing you to define and reproduce your entire workflow with ease.

----------

These tutorials provide a step-by-step guide to the core workflows of the library. If you are new to dmqclib, start here.

.. toctree::
   :maxdepth: 2
   :caption: 📘 Getting Started

   tutorial/overview
   tutorial/installation
   tutorial/preparation
   tutorial/training
   tutorial/classification

----------

This section provides practical examples and solutions for common tasks related to using dmqclib.

.. toctree::
   :maxdepth: 2
   :caption: 💡 How-To Guides

   how-to/data_preprocessing_utilities

----------

This section provides detailed reference information for all parameters in the YAML configuration files.

.. toctree::
   :maxdepth: 2
   :caption: ⚙️ Configuration

   configuration/preparation
   configuration/training
   configuration/classification

----------

For in-depth information on specific functions, classes, and methods, consult the API documentation.

.. toctree::
   :maxdepth: 2
   :caption: 🧩 API Reference

   api/modules
