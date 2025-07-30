"""
This module provides an XGBoost model wrapper, inheriting from `dmqclib.common.base.model_base.ModelBase`.

It facilitates training, prediction, and evaluation of an XGBoost classifier using Polars DataFrames,
converting them to Pandas for compatibility with the `xgboost` library. The module includes
methods for building the model, making predictions, and generating a comprehensive classification
report using `sklearn.metrics`.
"""

from typing import Dict, Any

import polars as pl
import xgboost as xgb
from sklearn.metrics import (
    classification_report,
)

from dmqclib.common.base.config_base import ConfigBase
from dmqclib.common.base.model_base import ModelBase


class XGBoost(ModelBase):
    """
    An XGBoost model wrapper class for training and testing using Polars data.

    Inherits from :class:`ModelBase` and implements the ``build`` and ``test`` methods
    specifically for an XGBoost classifier.

    Features include:

    - Conversion of Polars DataFrames to Pandas for compatibility with XGBoost.
    - Automatic application of ``model_params`` from the YAML config, if defined;
      otherwise, uses default hyperparameters.
    - Computation and storage of metrics (accuracy, balanced accuracy,
      classification report) in :attr:`report`.

    .. note::

       This class sets :attr:`expected_class_name` to ``"XGBoost"``, ensuring
       it can be matched in the YAML configuration if used within a
       loader or factory pattern.
    """

    expected_class_name: str = "XGBoost"

    def __init__(self, config: ConfigBase) -> None:
        """
        Initialize the XGBoost model with default or user-specified parameters.

        This constructor calls the parent :class:`ModelBase` constructor and then sets
        up default XGBoost parameters if no ``model_params`` are provided via the
        ``config`` object (i.e., if :attr:`self.model_params` is empty after :meth:`super().__init__`).

        :param config: A configuration object providing model parameters
                       (e.g., learning rate, max depth) and other metadata.
        :type config: ConfigBase
        :raises ValueError: If inherited requirements of :class:`ModelBase`
                            (like missing attributes) are not satisfied.
        """
        super().__init__(config=config)

        self.model_params: Dict[str, Any] = {
            "n_estimators": 100,
            "max_depth": 6,
            "learning_rate": 0.1,
            "eval_metric": "logloss",
        }
        # Update model parameters with config step parameters
        model_params = self.config.get_step_params("model").get("model_params", {})
        self.model_params.update(model_params)

    def build(self) -> None:
        """
        Train the XGBoost classifier using the assigned training set.

        Steps:

          1. Convert the Polars DataFrame (:attr:`training_set`) to Pandas.
          2. Separate features (X) and labels (y).
          3. Initialize and fit an XGBoost classifier with
             :attr:`model_params`.

        :raises ValueError: If :attr:`training_set` is ``None`` or empty during the training process.
        """
        if self.training_set is None:
            raise ValueError("Member variable 'training_set' must not be empty.")

        x_train = self.training_set.select(pl.exclude("label")).to_pandas()
        y_train = self.training_set["label"].to_pandas()

        self.model = xgb.XGBClassifier(**self.model_params)
        self.model.fit(x_train, y_train)

    def test(self) -> None:
        """
        Evaluate the trained XGBoost classifier on the assigned test set.

        Steps:

          1. Call :meth:`predict` to generate predictions on the test set.
          2. Call :meth:`create_report` to compute and store various evaluation metrics
             in :attr:`report`.

        The :attr:`k` attribute (provided by parent class or
        cross-validation context) is used to identify the fold number:

          - If :attr:`k` is 0, the 'k' column is dropped from the final :attr:`report`.

        :raises ValueError: If :attr:`test_set` is ``None`` or empty during prediction.
        :raises ValueError: If :attr:`predictions` is ``None`` during report creation.
        """
        self.predict()
        self.create_report()

    def predict(self) -> None:
        """
        Generates predictions for the test set using the trained model.

        Converts the Polars test set to a Pandas DataFrame, makes predictions
        using the stored XGBoost model, and stores the results in the
        :attr:`predictions` attribute as a Polars DataFrame.

        :raises ValueError: If :attr:`test_set` is ``None`` or empty.
        """
        if self.test_set is None:
            raise ValueError("Member variable 'test_set' must not be empty.")

        x_test = self.test_set.select(pl.exclude("label")).to_pandas()
        self.predictions = pl.DataFrame({"predicted": self.model.predict(x_test)})

    def create_report(self) -> None:
        """
        Computes and compiles a comprehensive classification report based on test results.

        This method calculates detailed classification metrics (precision, recall,
        f1-score, support) for each class, their macro/weighted averages, and
        overall accuracy using a single call to
        :func:`sklearn.metrics.classification_report`.

        The overall balanced accuracy is derived from the macro average recall.

        All computed metrics are stored in the :attr:`report` attribute as a Polars DataFrame.
        The :attr:`k` attribute (fold number) is included in the report rows and dropped if :attr:`k` is 0.

        :raises ValueError: If :attr:`test_set` or :attr:`predictions` are ``None``.
        """
        if self.test_set is None:
            raise ValueError("Member variable 'test_set' must not be empty.")

        if self.predictions is None:
            raise ValueError("Member variable 'predictions' must not be empty.")

        y_test = self.test_set["label"].to_pandas()
        y_pred = self.predictions["predicted"].to_pandas()

        # A single call to classification_report gets us almost everything we need.
        classification_dict = classification_report(
            y_test, y_pred, output_dict=True, zero_division=0
        )

        report_rows = []

        # Process all items from the classification report dictionary
        for label_key, metrics in classification_dict.items():
            if label_key == "accuracy":
                # This is the overall accuracy. Add it as a distinct metric type.
                report_rows.append(
                    {"k": self.k, "metric_type": "overall_accuracy", "value": metrics}
                )
            elif label_key == "macro avg":
                # Balanced accuracy is the same as the recall of the macro average.
                balanced_accuracy = metrics.get("recall")
                report_rows.append(
                    {
                        "k": self.k,
                        "metric_type": "balanced_accuracy",
                        "value": balanced_accuracy,
                    }
                )
                # Fall through to also add the full macro avg report row
                report_rows.append(
                    {
                        "k": self.k,
                        "metric_type": "classification_report",
                        "label": label_key,
                        "precision": metrics.get("precision"),
                        "recall": metrics.get("recall"),
                        "f1-score": metrics.get("f1-score"),
                        "support": metrics.get("support"),
                    }
                )
            else:  # Handles class labels and 'weighted avg'
                report_rows.append(
                    {
                        "k": self.k,
                        "metric_type": "classification_report",
                        "label": label_key,
                        "precision": metrics.get("precision"),
                        "recall": metrics.get("recall"),
                        "f1-score": metrics.get("f1-score"),
                        "support": metrics.get("support"),
                    }
                )

        self.report = pl.DataFrame(report_rows)

        if self.k == 0:
            self.report = self.report.drop("k")
