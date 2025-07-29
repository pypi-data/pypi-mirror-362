#! /usr/bin/env python3

"""
szengine.py is the abstract class for all implementations of SzEngine.
"""

# pylint: disable=C0302

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from .szengineflags import SzEngineFlags
from .szhelpers import construct_help

# Metadata

__all__ = ["SzEngine"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2025-01-28"


# -------------------------------------------------------------------------
# Classes
# -------------------------------------------------------------------------


class SzEngine(ABC):
    """
    Senzing engine module access library
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def add_record(
        self,
        data_source_code: str,
        record_id: str,
        record_definition: str,
        flags: int = SzEngineFlags.SZ_ADD_RECORD_DEFAULT_FLAGS,
    ) -> str:
        """
        The `add_record` method loads a record into the repository and performs entity resolution.

        Can be called as many times as desired and from multiple threads at the same time.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            record_definition (str): A JSON document containing the record to be added to the Senzing repository.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_ADD_RECORD_DEFAULT_FLAGS.

        Returns:
            str: If flags are set to return the WITH_INFO response a JSON document containing the details, otherwise an empty string.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/add_record.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/add_record.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def close_export_report(self, export_handle: int) -> None:
        """
        The `close_export_report` method closes an export report.

        It is part of the `export_json_entity_report`, `fetch_next`, `close_export_report`
        lifecycle of a list of sized entities.

        Args:
            export_handle (int): A handle created by `export_json_entity_report` or `export_csv_entity_report`.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def count_redo_records(self) -> int:
        """
        The `count_redo_records` method gets the number of redo records pending processing.

        Returns:
            int: The number of redo records in Senzing's redo queue.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/count_redo_records.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/count_redo_records.txt
                :linenos:
                :language: guess
        """

    @abstractmethod
    def delete_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_DELETE_RECORD_DEFAULT_FLAGS,
    ) -> str:
        """
        The `delete_record` method deletes a record from the repository and performs entity resolution.

        Can be called as many times as desired and from multiple threads at the same time.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_DELETE_RECORD_DEFAULT_FLAGS.

        Returns:
            str: If flags are set to return the WITH_INFO response a JSON document containing the details, otherwise an empty string.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/delete_record.py
                :linenos:

            **Output:**

            .. literalinclude:: ../../examples/szengine/delete_record.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def export_csv_entity_report(
        self,
        csv_column_list: str,
        flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS,
    ) -> int:
        """
        The `export_csv_entity_report` method initiates an export report of entity data in CSV format.

        **Warning:** `export_csv_entity_report` is not recommended for large systems as it does not scale.
        It is recommended larger systems implement real-time replication to a data warehouse.

        It is part of the `export_csv_entity_report`, `fetch_next`, `close_export_report`
        lifecycle of a list of entities to export.

        Available CSV columns: RESOLVED_ENTITY_ID, RESOLVED_ENTITY_NAME, RELATED_ENTITY_ID, MATCH_LEVEL,
                               MATCH_LEVEL_CODE, MATCH_KEY, MATCH_KEY_DETAILS,I S_DISCLOSED, IS_AMBIGUOUS,
                               DATA_SOURCE, RECORD_ID, JSON_DATA, FIRST_SEEN_DT, LAST_SEEN_DT, UNMAPPED_DATA,
                               ERRULE_CODE, RELATED_ENTITY_NAME

        Suggested CSV columns: RESOLVED_ENTITY_ID, RELATED_ENTITY_ID, RESOLVED_ENTITY_NAME, MATCH_LEVEL,
                               MATCH_KEY, DATA_SOURCE, RECORD_ID

        Args:
            csv_column_list (str): A comma-separated list of column names for the CSV export.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS.

        Returns:
            int: A handle that identifies the document to be scrolled through using `fetch_next`.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/export_csv_fetch_close.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/export_csv_fetch_close.txt
                :linenos:
                :language: guess
        """

    @abstractmethod
    def export_json_entity_report(self, flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS) -> int:
        """
        The `export_json_entity_report` method initiates an export report of entity data in JSON Lines format.

        **Warning:** `export_json_entity_report` is not recommended for large systems as it does not scale.
        It is recommended larger systems implement real-time replication to a data warehouse.

        It is part of the `export_json_entity_report`, `fetch_next`, `close_export_report`
        lifecycle of a list of entities to export.

        Args:
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS.

        Returns:
            int: A handle that identifies the document to be scrolled through using `fetch_next`.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def fetch_next(self, export_handle: int) -> str:
        """
        The `fetch_next` method fetches the next line of entity data from an open export report.

        Successive calls of `fetch_next` will export successive rows of entity data until there is no more.
        It is part of the `export_json_entity_report` or `export_json_entity_report`, `fetch_next`, `close_export_report`
        lifecycle of a list of exported entities.

        Args:
            export_handle (int): A handle created by `export_json_entity_report` or `export_json_entity_report`.

        Returns:
            str: TODO:

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.txt
                :linenos:
                :language: json
        """

    # pylint: disable=empty-docstring
    # NOTE - Not to be documented or examples, early adaptor feature, needs manual additions to config
    @abstractmethod
    def find_interesting_entities_by_entity_id(
        self, entity_id: int, flags: int = SzEngineFlags.SZ_FIND_INTERESTING_ENTITIES_DEFAULT_FLAGS
    ) -> str:
        """
        Experimental method.

        Contact Senzing support.
        """

    # NOTE - Not to be documented or examples, early adaptor feature, needs manual additions to config
    @abstractmethod
    def find_interesting_entities_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_FIND_INTERESTING_ENTITIES_DEFAULT_FLAGS,
    ) -> str:
        """
        Experimental method.

        Contact Senzing support.
        """

    # pylint: enable=empty-docstring

    @abstractmethod
    def find_network_by_entity_id(
        self,
        entity_ids: List[int],
        max_degrees: int,
        build_out_degrees: int,
        build_out_max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS,
    ) -> str:
        """
        The `find_network_by_entity_id` method retrieves a network of relationships among entities based on entity IDs.

        This includes the requested entities, paths between them, and relations to other nearby entities.
        Returns a JSON document that identifies the path between the each set of search entities (if the path exists),
        and the information for the entities in the path.

        Args:
            entity_ids (list(int)): The entity IDs to find the network between.
            max_degrees (int): The maximum number of degrees in paths between search entities.
            build_out_degrees (int): The number of degrees of relationships to show around each search entity.
            build_out_max_entities (int): The maximum number of entities to return in the discovered network.
            flags (int, optional): The maximum number of entities to return in the discovered network. Defaults to SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/find_network_by_entity_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/find_network_by_entity_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def find_network_by_record_id(
        self,
        record_keys: List[Tuple[str, str]],
        max_degrees: int,
        build_out_degrees: int,
        build_out_max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS,
    ) -> str:
        """
        The `find_network_by_record_id` method retrieves a network of relationships among entities based on record IDs.

        This includes the requested entities, paths between them, and relations to other nearby entities.
        Returns a JSON document that identifies the path between the each set of search entities (if the path exists),
        and the information for the entities in the path.

        Args:
            record_keys (list(tuple(str, str))): The data source codes and record IDs to find the network between.
            max_degrees (int): The maximum number of degrees in paths between search entities.
            build_out_degrees (int): The number of degrees of relationships to show around each search entity.
            build_out_max_entities (int): The maximum number of entities to return in the discovered network.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/find_network_by_record_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/find_network_by_record_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def find_path_by_entity_id(
        self,
        start_entity_id: int,
        end_entity_id: int,
        max_degrees: int,
        avoid_entity_ids: Optional[List[int]] = None,
        required_data_sources: Optional[List[str]] = None,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
    ) -> str:
        """
        The `find_path_by_entity_id` method searches for the shortest relationship path between two entities based
        on entity IDs.

        It finds the most efficient relationship between two entities path based on the parameters
        and returns a JSON document with an ENTITY_PATHS section that details the path between the entities.
        The ENTITIES sections details information on the entities. Paths are found using known relationships with other entities.
        Paths are found using known relationships with other entities.

        Args:
            start_entity_id (int): The entity ID for the starting entity of the search path.
            end_entity_id (int): The entity ID for the ending entity of the search path.
            max_degrees (int): The maximum number of degrees in paths between search entities.
            avoid_entity_ids (list(int), optional): The entity IDs to avoid when finding a path.
            required_data_sources (list(str), optional): The data source code(s) that must be in a path.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS.

        Returns:
            str: A JSON document with an ENTITY_PATHS section that details the path between the entities.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/find_path_by_entity_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/find_path_by_entity_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def find_path_by_record_id(
        self,
        start_data_source_code: str,
        start_record_id: str,
        end_data_source_code: str,
        end_record_id: str,
        max_degrees: int,
        avoid_record_keys: Optional[List[Tuple[str, str]]] = None,
        required_data_sources: Optional[List[str]] = None,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
    ) -> str:
        """
        The `find_path_by_record_id` method searches for the shortest relationship path between two entities based
        on record IDs.

        It finds the most efficient relationship between
        two entities path based on the parameters by RECORD_ID values
        and returns a JSON document with an ENTITY_PATHS section that details the path between the entities.
        The ENTITIES sections details information on the entities.
        Paths are found using known relationships with other entities.
        The entities are identified by starting and ending records.

        Args:
            start_data_source_code (str): Identifies the provenance of the record for the starting entity of the search path.
            start_record_id (str): The unique identifier within the records of the same data source for the starting entity of the search path.
            end_data_source_code (str): Identifies the provenance of the record for the ending entity of the search path.
            end_record_id (str): The unique identifier within the records of the same data source for the ending entity of the search path.
            max_degrees (int): The maximum number of degrees in paths between search entities.
            avoid_record_keys (list(tuple(str, str)), optional): The data source codes and record IDs to avoid when finding a path.
            required_data_sources (list(str), optional): The data source code(s) that must be in a path.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/find_path_by_record_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/find_path_by_record_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_active_config_id(self) -> int:
        """
        The `get_active_config_id` method gets the currently active configuration ID.

        Returns:
            int: The identifier of the active Senzing Engine configuration.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_active_config_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_active_config_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
    ) -> str:
        """
        The `get_entity_by_entity_id` method retrieves information about an entity based on entity ID.

        Args:
            entity_id (int): The unique identifier of an entity.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_entity_by_entity_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_entity_by_entity_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_entity_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
    ) -> str:
        """
        The `get_entity_by_record_id` method retrieves information about an entity based on record ID.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_entity_by_record_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_entity_by_record_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS,
    ) -> str:
        """
        The `get_record` method retrieves information about a record.

        Can be called as many times as desired and from multiple threads at the same time.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS.

        Returns:
            str: A JSON document of a single record.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_record.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_record.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_record_preview(
        self,
        record_definition: str,
        flags: int = SzEngineFlags.SZ_RECORD_PREVIEW_DEFAULT_FLAGS,
    ) -> str:
        """
        The `get_record_preview` method describes the features resulting from the hypothetical load of a record.

        Args:
            record_definition (str): A JSON document containing the record to be tested.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_RECORD_PREVIEW_DEFAULT_FLAGS.

        Returns:
            str: A JSON document containing metadata as specified by the flags.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_record_preview.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_record_preview.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_redo_record(self) -> str:
        """
        The `get_redo_record` method retrieves and removes a pending redo record.

        The `process_redo_record` method is called to process the redo record retrieved by `get_redo_record`.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_redo_record.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_redo_record.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_stats(self) -> str:
        """
        The `get_stats` method gets and resets the internal engine workload statistics for the current
        operating system process.

        These statistics will automatically reset after retrieval.

        Returns:
            str:  A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_stats.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_stats.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_virtual_entity_by_record_id(
        self,
        record_keys: List[Tuple[str, str]],
        flags: int = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS,
    ) -> str:
        """
        The `get_virtual_entity_by_record_id` method describes how an entity would look if composed of a given
        set of records.

        The virtual entity is composed of only those records and their features.
        Entity resolution is not performed.

        Args:
            record_keys (list(tuple(str, str))): The data source codes and record IDs identifying records to create the virtual entity from.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS.

        Returns:
            str:  A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_virtual_entity_by_record_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_virtual_entity_by_record_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def how_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS,
    ) -> str:
        """
        The `how_entity_by_entity_id` method explains how an entity was constructed from its records.

        In most cases, *how* provides more detailed information than *why* as the resolution is detailed step-by-step.

        Args:
            entity_id (int): The unique identifier of an entity.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/how_entity_by_entity_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/how_entity_by_entity_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def prime_engine(self) -> None:
        """
        The `prime_engine` method pre-loads engine resources.

        If this call is not made, these resources are initialized the
        first time they are needed and can cause unusually long processing times the first time
        a function is called that requires these resources.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/prime_engine.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def process_redo_record(self, redo_record: str, flags: int = 0) -> str:
        """
        The `process_redo_record` method processes the provided redo record.

        Args:
            redo_record (str): A redo record retrieved from get_redo_record.
            flags (int, optional): Flags used to control information returned. Defaults to 0.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/process_redo_record.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/process_redo_record.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def reevaluate_entity(self, entity_id: int, flags: int = SzEngineFlags.SZ_REEVALUATE_ENTITY_DEFAULT_FLAGS) -> str:
        """
        The `reevaluate_entity` method reevaluates an entity by entity ID.

        Args:
            entity_id (int): The unique identifier of an entity.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_REEVALUATE_ENTITY_DEFAULT_FLAGS.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/reevaluate_entity.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/reevaluate_entity.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def reevaluate_record(
        self, data_source_code: str, record_id: str, flags: int = SzEngineFlags.SZ_REEVALUATE_RECORD_DEFAULT_FLAGS
    ) -> str:
        """
        The `reevaluate_record` method reevaluates an entity by record ID.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            flags (int, optional):  Flags used to control information returned. Defaults to SzEngineFlags.SZ_REEVALUATE_RECORD_DEFAULT_FLAGS.

        Returns:
            str: If flags are set to return the WITH_INFO response a JSON document containing the details, otherwise an empty string.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/reevaluate_record.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/reevaluate_record.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def search_by_attributes(
        self,
        attributes: str,
        flags: int = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS,
        search_profile: str = "",
    ) -> str:
        """
        The `search_by_attributes` method searches for entities that match or relate to the provided attributes.

        Args:
            attributes (str): A JSON document with the attribute data to search for.
            flags (int, optional): _description_. Defaults to SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS.
            search_profile (str): The name of a configured search profile. Defaults to SEARCH.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/search_by_attributes.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/search_by_attributes.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def why_entities(
        self,
        entity_id_1: int,
        entity_id_2: int,
        flags: int = SzEngineFlags.SZ_WHY_ENTITIES_DEFAULT_FLAGS,
    ) -> str:
        """
        The `why_entities` method describes the ways two entities relate to each other.

        Args:
            entity_id_1 (int): The entity ID for the starting entity of the search path.
            entity_id_2 (int): The entity ID for the ending entity of the search path.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_WHY_ENTITIES_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/why_entities.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/why_entities.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def why_record_in_entity(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORD_IN_ENTITY_DEFAULT_FLAGS,
    ) -> str:
        """
        The `why_record_in_entity` method describes the ways a record relates to the rest of its respective entity.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_WHY_RECORD_IN_ENTITY_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/why_record_in_entity.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/why_record_in_entity.txt
                    :linenos:
                    :language: json
        """

    @abstractmethod
    def why_records(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS,
    ) -> str:
        """
        The `why_records` method describes the ways two records relate to each other.

        Args:
            data_source_code_1 (str): Identifies the provenance of the data.
            record_id_1 (str): The unique identifier within the records of the same data source.
            data_source_code_2 (str): Identifies the provenance of the data.
            record_id_2 (str): The unique identifier within the records of the same data source.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/why_records.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/why_records.txt
                    :linenos:
                    :language: json
        """

    @abstractmethod
    def why_search(
        self,
        attributes: str,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_WHY_SEARCH_DEFAULT_FLAGS,
        search_profile: str = "",
    ) -> str:
        """
        The `why_search` method describes the ways a set of search attributes relate to an entity.

        Args:
            attributes (str): A JSON document with the attribute data to search for.
            entity_id (int): The identifier of the entity to retrieve.
            flags (int, optional): _description_. Defaults to SzEngineFlags.SZ_WHY_SEARCH_DEFAULT_FLAGS.
            search_profile (str): The name of a configured search profile. Defaults to SEARCH.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/why_search.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/why_search.txt
                :linenos:
                :language: json
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
