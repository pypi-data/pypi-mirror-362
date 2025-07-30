"""
This module defines the `InputDataSetAll` class, which is responsible for
loading and preparing a specific combination of input datasets, namely
Copernicus CTD data. It extends `InputDataSetBase` and leverages
a configuration object to manage data retrieval and processing.
"""

from dmqclib.common.base.config_base import ConfigBase
from dmqclib.prepare.step1_read_input.input_base import InputDataSetBase


class InputDataSetAll(InputDataSetBase):
    """
    A subclass of :class:`dmqclib.prepare.step1_read_input.input_base.InputDataSetBase`
    providing specific logic for reading Copernicus CTD data.

    This class sets the :attr:`expected_class_name` to ``InputDataSetAll``,
    ensuring the correct YAML configuration is matched for data loading
    and validation within the larger system.
    """

    expected_class_name: str = "InputDataSetAll"

    def __init__(self, config: ConfigBase) -> None:
        """
        Initializes the InputDataSetAll instance with a given configuration.

        This constructor calls the parent class's constructor, passing the
        provided configuration object to set up the base dataset properties.

        :param config: A configuration object derived from :class:`dmqclib.common.base.config_base.ConfigBase`,
                       containing paths and parameters necessary for retrieving
                       Copernicus CTD data.
        :type config: ConfigBase
        """
        super().__init__(config=config)
