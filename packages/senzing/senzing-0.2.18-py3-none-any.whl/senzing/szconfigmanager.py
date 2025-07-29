#! /usr/bin/env python3

"""
szconfigmanager.py is the abstract class for all implementations of SzConfigManager.
"""

# TODO: Determine specific SzErrors, Errors for "Raises:" documentation.

from abc import ABC, abstractmethod

from .szconfig import SzConfig
from .szhelpers import construct_help

# Metadata

__all__ = ["SzConfigManager"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-08"

# -----------------------------------------------------------------------------
# SzConfigManager
# -----------------------------------------------------------------------------


class SzConfigManager(ABC):
    """
    SzConfigManager is the definition of the Senzing Python SDK that is
    implemented by packages such as szconfigmanager.py.
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def create_config_from_config_id(self, config_id: int) -> SzConfig:
        """
        The `create_config_from_config_id` method creates a new SzConfig instance for a configuration ID.

        Args:
            config_id (int): The configuration identifier of the desired Senzing configuration to retrieve.

        Returns:
            SzConfig: Represents an in-memory Senzing configuration that can be modified.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/create_config_from_config_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfigmanager/create_config_from_config_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def create_config_from_string(self, config_definition: str) -> SzConfig:
        """
        The `create_config_from_string` method creates a new SzConfig instance from a configuration definition.

        Args:
            config_definition (str): The Senzing configuration JSON document.

        Returns:
            SzConfig: Represents an in-memory Senzing configuration that can be modified.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/create_config_from_string.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfigmanager/create_config_from_string.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def create_config_from_template(self) -> SzConfig:
        """
        The `create_config_from_template` method creates a new SzConfig instance from the template
        configuration definition.

        The template configuration is located at PIPELINE.RESOURCEPATH/templates/g2config.json

        Args:
            config_definition (str): The Senzing configuration JSON document.

        Returns:
            SzConfig: Represents an in-memory Senzing configuration that can be modified.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/create_config_from_template.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfigmanager/create_config_from_template.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_config_registry(self) -> str:
        """
        The `get_config_registry` method gets the configuration registry.

        Returns:
            str: A JSON document containing Senzing configurations.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/get_config_registry.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfigmanager/get_config_registry.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_default_config_id(self) -> int:
        """
        The `get_default_config_id` method gets the default configuration ID for the repository.

        Returns:
            int:  A configuration identifier which identifies the current configuration in use.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/get_default_config_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfigmanager/get_default_config_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def register_config(self, config_definition: str, config_comment: str) -> int:
        """
        The `register_config` method registers a configuration definition in the repository.

        Args:
            config_definition (str): The Senzing configuration JSON document.
            config_comment (str):  free-form string of comments describing the configuration document.

        Returns:
            int: A configuration identifier.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/register_config.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfigmanager/register_config.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def replace_default_config_id(self, current_default_config_id: int, new_default_config_id: int) -> None:
        """
        The `replace_default_config_id` method replaces the existing default configuration ID with
        a new configuration ID.

        It is like a "compare-and-swap" instruction to serialize concurrent editing of configuration.
        If `current_default_config_id` is no longer the "current configuration identifier", the operation will fail.
        To simply set the default configuration ID, use `set_default_config_id`.

        Args:
            current_default_config_id (int): The configuration identifier to replace.
            new_default_config_id (int): The configuration identifier to use as the default.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/replace_default_config_id.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def set_default_config(self, config_definition: str, config_comment: str) -> int:
        """
        The `set_default_config` method registers a configuration in the repository and sets its ID as the default
        for the repository.

        To serialize modifying of the configuration identifier, see `replace_default_config_id`.

        Args:
            config_definition (str): The Senzing configuration JSON document.
            config_comment (str):  free-form string of comments describing the configuration document.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/set_default_config.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfigmanager/set_default_config.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def set_default_config_id(self, config_id: int) -> None:
        """
        The `set_default_config_id` method sets the default configuration ID.

        To serialize modifying of the configuration identifier, see `replace_default_config_id`.

        Args:
            config_id (int): The configuration identifier of the Senzing Engine configuration to use as the default.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/set_default_config_id.py
                :linenos:
                :language: python
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    def help(self, method_name: str = "") -> str:
        """
        The `help` method returns help for a particular message.

        Args:
            method_name (str): The name of the method. (e.g. "init"). If empty, a list of methods and descriptions is returned.

        Returns:
            str: The Help information about the requested method
        """
        return construct_help(self, method_name=method_name)
