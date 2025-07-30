"""
Module defining the global registry for feature classes.

This module provides ``FEATURE_REGISTRY``, a central mapping of string
identifiers to specific feature-extraction classes within the `dmqclib`
pipeline. Each entry allows for dynamic loading and instantiation of
feature generators based on configuration settings, facilitating the
preparation of datasets by applying various data transformations and
extractions.
"""

from typing import Dict, Type

from dmqclib.common.base.feature_base import FeatureBase
from dmqclib.prepare.features.basic_values import BasicValues
from dmqclib.prepare.features.day_of_year import DayOfYearFeat
from dmqclib.prepare.features.flank_down import FlankDown
from dmqclib.prepare.features.flank_up import FlankUp
from dmqclib.prepare.features.location import LocationFeat
from dmqclib.prepare.features.profile_summary import ProfileSummaryStats5

#: A dictionary mapping feature identifiers (str) to classes that inherit
#: from :class:`FeatureBase`. These classes are dynamically loaded based
#: on the "feature" key in a feature configuration dictionary.
FEATURE_REGISTRY: Dict[str, Type[FeatureBase]] = {
    "location": LocationFeat,
    "day_of_year": DayOfYearFeat,
    "profile_summary_stats5": ProfileSummaryStats5,
    "basic_values": BasicValues,
    "flank_up": FlankUp,
    "flank_down": FlankDown,
}
