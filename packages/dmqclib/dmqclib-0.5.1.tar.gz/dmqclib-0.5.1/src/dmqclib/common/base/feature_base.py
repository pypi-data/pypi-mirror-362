"""
This module defines an abstract base class, `FeatureBase`, for a standardized approach
to extracting and scaling features using the Polars data manipulation library.

It provides a blueprint for subclasses to implement specific feature engineering
workflows, ensuring consistency in data processing steps across different
feature sets or models.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional

import polars as pl


class FeatureBase(ABC):
    """
    Abstract base class for extracting and scaling features.

    Child classes must implement all abstract methods:

    - :meth:`extract_features`
    - :meth:`scale_first`
    - :meth:`scale_second`

    These methods encompass the steps to:

    1. Extract relevant features from provided data.
    2. Perform an initial scaling or normalization process.
    3. Optionally perform a second scaling pass, depending on
       the specific requirements.
    """

    def __init__(
        self,
        target_name: Optional[str] = None,
        feature_info: Optional[Dict] = None,
        selected_profiles: Optional[pl.DataFrame] = None,
        filtered_input: Optional[pl.DataFrame] = None,
        selected_rows: Optional[Dict[str, pl.DataFrame]] = None,
        summary_stats: Optional[pl.DataFrame] = None,
    ) -> None:
        """
        Initialize the feature-extraction base class with optional data and metadata.

        :param target_name: Name of the target variable to use when extracting features.
        :type target_name: Optional[str]
        :param feature_info: A dictionary containing metadata or configuration
                             about features.
        :type feature_info: Optional[Dict]
        :param selected_profiles: A Polars DataFrame containing pre-selected
                                  profiles or records relevant for feature derivation.
        :type selected_profiles: Optional[pl.DataFrame]
        :param filtered_input: A Polars DataFrame that may already include filters
                               applied to the data prior to feature extraction.
        :type filtered_input: Optional[pl.DataFrame]
        :param selected_rows: A dictionary mapping identifiers to Polars DataFrames,
                              focusing on the target rows for subsequent transformations.
        :type selected_rows: Optional[Dict[str, pl.DataFrame]]
        :param summary_stats: A Polars DataFrame of summary statistics that might
                              guide transformations (e.g., scaling) of features.
        :type summary_stats: Optional[pl.DataFrame]
        :rtype: None
        """
        self.target_name: Optional[str] = target_name
        self.feature_info: Optional[Dict] = feature_info
        self.selected_profiles: Optional[pl.DataFrame] = selected_profiles
        self.filtered_input: Optional[pl.DataFrame] = filtered_input
        self.selected_rows: Optional[Dict[str, pl.DataFrame]] = selected_rows
        self.summary_stats: Optional[pl.DataFrame] = summary_stats
        self.features: Optional[pl.DataFrame] = None

    @abstractmethod
    def extract_features(self) -> None:
        """
        Extract features from the provided data sources.

        This method is responsible for generating the raw features and storing them
        in the `self.features` attribute. Classes that subclass :class:`FeatureBase`
        must implement and tailor this method to their specific feature requirements.
        For instance, transformations on ``self.filtered_input`` or merges with
        ``self.selected_rows`` can occur here.

        :rtype: None
        """
        pass  # pragma: no cover

    @abstractmethod
    def scale_first(self) -> None:
        """
        Apply the first pass of scaling or normalization to the extracted features.

        This is typically used to handle basic transformations,
        removing outliers or applying standard scaling. Child classes
        should decide how and when these transformations are applied.
        The scaled features should update the `self.features` attribute.

        :rtype: None
        """
        pass  # pragma: no cover

    @abstractmethod
    def scale_second(self) -> None:
        """
        Apply a secondary scaling or refinement step to the features.

        This step might be used when further adjustments are needed
        after the initial scaling, such as a domain-specific transformation
        or final normalizations to align with a particular model's requirements.
        The refined features should update the `self.features` attribute.

        :rtype: None
        """
        pass  # pragma: no cover
