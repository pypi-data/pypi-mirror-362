from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.response_handler import ResponseHandler
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .......models.error import Error
    from .comments.comments_request_builder import CommentsRequestBuilder
    from .meta.meta_request_builder import MetaRequestBuilder
    from .references.references_request_builder import ReferencesRequestBuilder
    from .state.state_request_builder import StateRequestBuilder

class WithVersionItemRequestBuilder(BaseRequestBuilder):
    """
    Manage a single version of a single artifact in the registry.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new WithVersionItemRequestBuilder and sets the default values.
        Args:
            path_parameters: The raw url or the Url template parameters for the request.
            request_adapter: The request adapter to use to execute the requests.
        """
        super().__init__(request_adapter, "{+baseurl}/groups/{groupId}/artifacts/{artifactId}/versions/{version}{?dereference*}", path_parameters)
    
    async def delete(self,request_configuration: Optional[WithVersionItemRequestBuilderDeleteRequestConfiguration] = None) -> None:
        """
        Deletes a single version of the artifact. Parameters `groupId`, `artifactId` and the unique `version`are needed. If this is the only version of the artifact, this operation is the same as deleting the entire artifact.This feature is disabled by default and it's discouraged for normal usage. To enable it, set the `registry.rest.artifact.deletion.enabled` property to true. This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`) * Feature is disabled (HTTP error `405`) * A server error occurred (HTTP error `500`)
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        """
        request_info = self.to_delete_request_information(
            request_configuration
        )
        from .......models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "405": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    async def get(self,request_configuration: Optional[WithVersionItemRequestBuilderGetRequestConfiguration] = None) -> bytes:
        """
        Retrieves a single version of the artifact content.  Both the `artifactId` and theunique `version` number must be provided.  The `Content-Type` of the response depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from .......models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "bytes", error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[WithVersionItemRequestBuilderDeleteRequestConfiguration] = None) -> RequestInformation:
        """
        Deletes a single version of the artifact. Parameters `groupId`, `artifactId` and the unique `version`are needed. If this is the only version of the artifact, this operation is the same as deleting the entire artifact.This feature is disabled by default and it's discouraged for normal usage. To enable it, set the `registry.rest.artifact.deletion.enabled` property to true. This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`) * Feature is disabled (HTTP error `405`) * A server error occurred (HTTP error `500`)
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.DELETE
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        return request_info
    
    def to_get_request_information(self,request_configuration: Optional[WithVersionItemRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Retrieves a single version of the artifact content.  Both the `artifactId` and theunique `version` number must be provided.  The `Content-Type` of the response depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.GET
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.set_query_string_parameters_from_raw_object(request_configuration.query_parameters)
            request_info.add_request_options(request_configuration.options)
        return request_info
    
    @property
    def comments(self) -> CommentsRequestBuilder:
        """
        Manage a collection of comments for an artifact version
        """
        from .comments.comments_request_builder import CommentsRequestBuilder

        return CommentsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def meta(self) -> MetaRequestBuilder:
        """
        Manage the metadata for a single version of an artifact in the registry.
        """
        from .meta.meta_request_builder import MetaRequestBuilder

        return MetaRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def references(self) -> ReferencesRequestBuilder:
        """
        Manage the references for a single version of an artifact in the registry.
        """
        from .references.references_request_builder import ReferencesRequestBuilder

        return ReferencesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def state(self) -> StateRequestBuilder:
        """
        Manage the state of a specific artifact version.
        """
        from .state.state_request_builder import StateRequestBuilder

        return StateRequestBuilder(self.request_adapter, self.path_parameters)
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithVersionItemRequestBuilderDeleteRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    @dataclass
    class WithVersionItemRequestBuilderGetQueryParameters():
        """
        Retrieves a single version of the artifact content.  Both the `artifactId` and theunique `version` number must be provided.  The `Content-Type` of the response depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        """
        def get_query_parameter(self,original_name: Optional[str] = None) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            Args:
                original_name: The original query parameter name in the class.
            Returns: str
            """
            if not original_name:
                raise TypeError("original_name cannot be null.")
            if original_name == "dereference":
                return "dereference"
            return original_name
        
        # Allows the user to specify if the content should be dereferenced when being returned
        dereference: Optional[bool] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithVersionItemRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request query parameters
        query_parameters: Optional[WithVersionItemRequestBuilder.WithVersionItemRequestBuilderGetQueryParameters] = None

    

