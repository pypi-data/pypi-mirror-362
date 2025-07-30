"""
This module defines the LocationFeat class, a specialized feature extractor
for geographical coordinates (longitude, latitude) within a specified dataset.

It extends the generic FeatureBase to handle the specific requirements of
location data, including extraction from raw profiles and optional scaling.
"""

from typing import Optional, Dict

import polars as pl

from dmqclib.common.base.feature_base import FeatureBase


class LocationFeat(FeatureBase):
    """
    A feature extraction class designed specifically for location-based fields
    (e.g., longitude, latitude) within the Copernicus CTD dataset.

    This class uses the provided data frames to gather location-related fields
    and optionally apply scaling methods. It inherits from
    :class:`~dmqclib.common.base.feature_base.FeatureBase` which defines a generic
    feature extraction workflow.
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
        Initialize the location feature extractor with relevant data frames.

        :param target_name: The key for the target variable in :attr:`selected_rows`.
                            Defaults to None.
        :type target_name: Optional[str]
        :param feature_info: A dictionary describing feature parameters, typically
                             including scaling statistics. Defaults to None.
        :type feature_info: Optional[Dict]
        :param selected_profiles: A Polars DataFrame containing a subset of profiles
                                  relevant to feature extraction, including location data.
                                  Defaults to None.
        :type selected_profiles: Optional[pl.DataFrame]
        :param filtered_input: A filtered Polars DataFrame of input data,
                               potentially used for advanced merging or lookups.
                               Defaults to None.
        :type filtered_input: Optional[pl.DataFrame]
        :param selected_rows: A dictionary keyed by target names, each mapping to
                              a Polars DataFrame of rows relevant for that target.
                              Defaults to None.
        :type selected_rows: Optional[Dict[str, pl.DataFrame]]
        :param summary_stats: A Polars DataFrame containing statistical
                              information that may aid in feature scaling.
                              Defaults to None.
        :type summary_stats: Optional[pl.DataFrame]
        """
        super().__init__(
            target_name=target_name,
            feature_info=feature_info,
            selected_profiles=selected_profiles,
            filtered_input=filtered_input,
            selected_rows=selected_rows,
            summary_stats=summary_stats,
        )

    def extract_features(self) -> None:
        """
        Gather and merge location columns (e.g., longitude and latitude) from
        :attr:`selected_profiles` into :attr:`selected_rows` to form the final
        feature set in :attr:`features`.

        Specifically:

          1. Selects columns like ``row_id``, ``platform_code``, and ``profile_no``
             from the DataFrame in :attr:`selected_rows[target_name]`.
          2. Joins this subset with corresponding columns from :attr:`selected_profiles`
             (including ``longitude`` and ``latitude``) on ``platform_code``
             and ``profile_no``.
          3. Drops those join columns from the final feature set, leaving
             ``row_id``, ``longitude``, and ``latitude`` among others.

        :returns: None. The result is stored in the :attr:`features` attribute.
        :rtype: None
        """
        self.features = (
            self.selected_rows[self.target_name]
            .select(["row_id", "platform_code", "profile_no"])
            .join(
                self.selected_profiles.select(
                    ["platform_code", "profile_no", "longitude", "latitude"]
                ).unique(),
                on=["platform_code", "profile_no"],
                how="left",  # Changed from maintain_order to how for clarity and standard Polars usage
            )
            .drop(["platform_code", "profile_no"])
        )

    def scale_first(self) -> None:
        """
        (Optional) Initial scaling or normalization procedure.

        Currently, this method is unimplemented for location features and serves
        as a placeholder for future extensions, e.g., if location data requires
        pre-processing or transformation steps before the final scaling.

        :returns: None. Operations are performed in-place on :attr:`features`.
        :rtype: None
        """
        pass  # pragma: no cover

    def scale_second(self) -> None:
        """
        Apply a min-max scaling pass to each feature (column) specified in
        :attr:`feature_info["stats"]`.

        This method iterates through the keys of the ``"stats"`` dictionary within
        :attr:`feature_info`. For each key `k` (representing a feature name),
        it expects a dictionary ``v`` with ``"min"`` and ``"max"`` keys to
        perform the min-max scaling: ``(value - min) / (max - min)``.

        Example structure for ``feature_info["stats"]``::

            {
                "longitude": {"min": -180.0, "max": 180.0},
                "latitude": {"min": -90.0, "max": 90.0},
                ...
            }

        :returns: None. Scaling is applied in-place to the :attr:`features` DataFrame.
        :rtype: None
        """
        for k, v in self.feature_info["stats"].items():
            self.features = self.features.with_columns(
                ((pl.col(k) - v["min"]) / (v["max"] - v["min"])).alias(k)
            )
