from __future__ import annotations
from kiota_abstractions.api_client_builder import enable_backing_store_for_serialization_writer_factory, register_default_deserializer, register_default_serializer
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.serialization import ParseNodeFactoryRegistry, SerializationWriterFactoryRegistry
from kiota_serialization_json.json_parse_node_factory import JsonParseNodeFactory
from kiota_serialization_json.json_serialization_writer_factory import JsonSerializationWriterFactory
from kiota_serialization_text.text_parse_node_factory import TextParseNodeFactory
from kiota_serialization_text.text_serialization_writer_factory import TextSerializationWriterFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .admin.admin_request_builder import AdminRequestBuilder
    from .groups.groups_request_builder import GroupsRequestBuilder
    from .ids.ids_request_builder import IdsRequestBuilder
    from .search.search_request_builder import SearchRequestBuilder
    from .system.system_request_builder import SystemRequestBuilder
    from .users.users_request_builder import UsersRequestBuilder

class RegistryClient(BaseRequestBuilder):
    """
    The main entry point of the SDK, exposes the configuration and the fluent API.
    """
    def __init__(self,request_adapter: RequestAdapter) -> None:
        """
        Instantiates a new RegistryClient and sets the default values.
        Args:
            request_adapter: The request adapter to use to execute the requests.
        """
        if not request_adapter:
            raise TypeError("request_adapter cannot be null.")
        super().__init__(request_adapter, "{+baseurl}", None)
        register_default_serializer(JsonSerializationWriterFactory)
        register_default_serializer(TextSerializationWriterFactory)
        register_default_deserializer(JsonParseNodeFactory)
        register_default_deserializer(TextParseNodeFactory)
    
    @property
    def admin(self) -> AdminRequestBuilder:
        """
        The admin property
        """
        from .admin.admin_request_builder import AdminRequestBuilder

        return AdminRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def groups(self) -> GroupsRequestBuilder:
        """
        Collection of the groups in the registry.
        """
        from .groups.groups_request_builder import GroupsRequestBuilder

        return GroupsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def ids(self) -> IdsRequestBuilder:
        """
        The ids property
        """
        from .ids.ids_request_builder import IdsRequestBuilder

        return IdsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def search(self) -> SearchRequestBuilder:
        """
        The search property
        """
        from .search.search_request_builder import SearchRequestBuilder

        return SearchRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def system(self) -> SystemRequestBuilder:
        """
        The system property
        """
        from .system.system_request_builder import SystemRequestBuilder

        return SystemRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def users(self) -> UsersRequestBuilder:
        """
        The users property
        """
        from .users.users_request_builder import UsersRequestBuilder

        return UsersRequestBuilder(self.request_adapter, self.path_parameters)
    

