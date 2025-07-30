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
    from .....models.artifact_content import ArtifactContent
    from .....models.artifact_meta_data import ArtifactMetaData
    from .....models.error import Error
    from .meta.meta_request_builder import MetaRequestBuilder
    from .owner.owner_request_builder import OwnerRequestBuilder
    from .rules.rules_request_builder import RulesRequestBuilder
    from .state.state_request_builder import StateRequestBuilder
    from .test.test_request_builder import TestRequestBuilder
    from .versions.versions_request_builder import VersionsRequestBuilder

class WithArtifactItemRequestBuilder(BaseRequestBuilder):
    """
    Manage a single artifact.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new WithArtifactItemRequestBuilder and sets the default values.
        Args:
            path_parameters: The raw url or the Url template parameters for the request.
            request_adapter: The request adapter to use to execute the requests.
        """
        super().__init__(request_adapter, "{+baseurl}/groups/{groupId}/artifacts/{artifactId}{?dereference*}", path_parameters)
    
    async def delete(self,request_configuration: Optional[WithArtifactItemRequestBuilderDeleteRequestConfiguration] = None) -> None:
        """
        Deletes an artifact completely, resulting in all versions of the artifact also beingdeleted.  This may fail for one of the following reasons:* No artifact with the `artifactId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        """
        request_info = self.to_delete_request_information(
            request_configuration
        )
        from .....models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    async def get(self,request_configuration: Optional[WithArtifactItemRequestBuilderGetRequestConfiguration] = None) -> bytes:
        """
        Returns the latest version of the artifact in its raw form.  The `Content-Type` of theresponse depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).If the latest version of the artifact is marked as `DISABLED`, the next available non-disabled version will be used.This operation may fail for one of the following reasons:* No artifact with this `artifactId` exists or all versions are `DISABLED` (HTTP error `404`)* A server error occurred (HTTP error `500`)
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from .....models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "bytes", error_mapping)
    
    async def put(self,body: Optional[ArtifactContent] = None, request_configuration: Optional[WithArtifactItemRequestBuilderPutRequestConfiguration] = None) -> Optional[ArtifactMetaData]:
        """
        Updates an artifact by uploading new content.  The body of the request canbe the raw content of the artifact or a JSON object containing both the raw content anda set of references to other artifacts..  This is typically in JSON format for *most*of the supported types, but may be in another format for a few (for example, `PROTOBUF`).The type of the content should be compatible with the artifact's type (it would bean error to update an `AVRO` artifact with new `OPENAPI` content, for example).The update could fail for a number of reasons including:* Provided content (request body) was empty (HTTP error `400`)* No artifact with the `artifactId` exists (HTTP error `404`)* The new content violates one of the rules configured for the artifact (HTTP error `409`)* A server error occurred (HTTP error `500`)When successful, this creates a new version of the artifact, making it the most recent(and therefore official) version of the artifact.
        Args:
            body: The request body
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ArtifactMetaData]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_put_request_information(
            body, request_configuration
        )
        from .....models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "409": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.artifact_meta_data import ArtifactMetaData

        return await self.request_adapter.send_async(request_info, ArtifactMetaData, error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[WithArtifactItemRequestBuilderDeleteRequestConfiguration] = None) -> RequestInformation:
        """
        Deletes an artifact completely, resulting in all versions of the artifact also beingdeleted.  This may fail for one of the following reasons:* No artifact with the `artifactId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def to_get_request_information(self,request_configuration: Optional[WithArtifactItemRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Returns the latest version of the artifact in its raw form.  The `Content-Type` of theresponse depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).If the latest version of the artifact is marked as `DISABLED`, the next available non-disabled version will be used.This operation may fail for one of the following reasons:* No artifact with this `artifactId` exists or all versions are `DISABLED` (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def to_put_request_information(self,body: Optional[ArtifactContent] = None, request_configuration: Optional[WithArtifactItemRequestBuilderPutRequestConfiguration] = None) -> RequestInformation:
        """
        Updates an artifact by uploading new content.  The body of the request canbe the raw content of the artifact or a JSON object containing both the raw content anda set of references to other artifacts..  This is typically in JSON format for *most*of the supported types, but may be in another format for a few (for example, `PROTOBUF`).The type of the content should be compatible with the artifact's type (it would bean error to update an `AVRO` artifact with new `OPENAPI` content, for example).The update could fail for a number of reasons including:* Provided content (request body) was empty (HTTP error `400`)* No artifact with the `artifactId` exists (HTTP error `404`)* The new content violates one of the rules configured for the artifact (HTTP error `409`)* A server error occurred (HTTP error `500`)When successful, this creates a new version of the artifact, making it the most recent(and therefore official) version of the artifact.
        Args:
            body: The request body
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.PUT
        request_info.headers["Accept"] = ["application/json"]
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        request_info.set_content_from_parsable(self.request_adapter, "application/create.extended+json", body)
        return request_info
    
    @property
    def meta(self) -> MetaRequestBuilder:
        """
        Manage the metadata of a single artifact.
        """
        from .meta.meta_request_builder import MetaRequestBuilder

        return MetaRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def owner(self) -> OwnerRequestBuilder:
        """
        Manage the ownership of a single artifact.
        """
        from .owner.owner_request_builder import OwnerRequestBuilder

        return OwnerRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def rules(self) -> RulesRequestBuilder:
        """
        Manage the rules for a single artifact.
        """
        from .rules.rules_request_builder import RulesRequestBuilder

        return RulesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def state(self) -> StateRequestBuilder:
        """
        Manage the state of an artifact.
        """
        from .state.state_request_builder import StateRequestBuilder

        return StateRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def test(self) -> TestRequestBuilder:
        """
        Test whether content would pass update rules.
        """
        from .test.test_request_builder import TestRequestBuilder

        return TestRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def versions(self) -> VersionsRequestBuilder:
        """
        Manage all the versions of an artifact in the registry.
        """
        from .versions.versions_request_builder import VersionsRequestBuilder

        return VersionsRequestBuilder(self.request_adapter, self.path_parameters)
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithArtifactItemRequestBuilderDeleteRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    @dataclass
    class WithArtifactItemRequestBuilderGetQueryParameters():
        """
        Returns the latest version of the artifact in its raw form.  The `Content-Type` of theresponse depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).If the latest version of the artifact is marked as `DISABLED`, the next available non-disabled version will be used.This operation may fail for one of the following reasons:* No artifact with this `artifactId` exists or all versions are `DISABLED` (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    class WithArtifactItemRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request query parameters
        query_parameters: Optional[WithArtifactItemRequestBuilder.WithArtifactItemRequestBuilderGetQueryParameters] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithArtifactItemRequestBuilderPutRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    

