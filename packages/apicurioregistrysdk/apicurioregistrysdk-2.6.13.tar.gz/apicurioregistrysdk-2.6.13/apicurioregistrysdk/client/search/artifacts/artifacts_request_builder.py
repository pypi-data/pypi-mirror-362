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
    from ...models.artifact_search_results import ArtifactSearchResults
    from ...models.error import Error

class ArtifactsRequestBuilder(BaseRequestBuilder):
    """
    Search for artifacts in the registry.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new ArtifactsRequestBuilder and sets the default values.
        Args:
            path_parameters: The raw url or the Url template parameters for the request.
            request_adapter: The request adapter to use to execute the requests.
        """
        super().__init__(request_adapter, "{+baseurl}/search/artifacts{?name*,offset*,limit*,order*,orderby*,labels*,properties*,description*,group*,globalId*,contentId*,canonical*,artifactType*}", path_parameters)
    
    async def get(self,request_configuration: Optional[ArtifactsRequestBuilderGetRequestConfiguration] = None) -> Optional[ArtifactSearchResults]:
        """
        Returns a paginated list of all artifacts that match the provided filter criteria.
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ArtifactSearchResults]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ...models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ...models.artifact_search_results import ArtifactSearchResults

        return await self.request_adapter.send_async(request_info, ArtifactSearchResults, error_mapping)
    
    async def post(self,body: bytes, request_configuration: Optional[ArtifactsRequestBuilderPostRequestConfiguration] = None) -> Optional[ArtifactSearchResults]:
        """
        Returns a paginated list of all artifacts with at least one version that matches theposted content.
        Args:
            body: Binary request body
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ArtifactSearchResults]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from ...models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ...models.artifact_search_results import ArtifactSearchResults

        return await self.request_adapter.send_async(request_info, ArtifactSearchResults, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[ArtifactsRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Returns a paginated list of all artifacts that match the provided filter criteria.
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.GET
        request_info.headers["Accept"] = ["application/json"]
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.set_query_string_parameters_from_raw_object(request_configuration.query_parameters)
            request_info.add_request_options(request_configuration.options)
        return request_info
    
    def to_post_request_information(self,body: bytes, request_configuration: Optional[ArtifactsRequestBuilderPostRequestConfiguration] = None) -> RequestInformation:
        """
        Returns a paginated list of all artifacts with at least one version that matches theposted content.
        Args:
            body: Binary request body
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.POST
        request_info.headers["Accept"] = ["application/json"]
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.set_query_string_parameters_from_raw_object(request_configuration.query_parameters)
            request_info.add_request_options(request_configuration.options)
        request_info.set_stream_content(body)
        return request_info
    
    @dataclass
    class ArtifactsRequestBuilderGetQueryParameters():
        """
        Returns a paginated list of all artifacts that match the provided filter criteria.
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
            if original_name == "content_id":
                return "contentId"
            if original_name == "description":
                return "description"
            if original_name == "global_id":
                return "globalId"
            if original_name == "group":
                return "group"
            if original_name == "labels":
                return "labels"
            if original_name == "limit":
                return "limit"
            if original_name == "name":
                return "name"
            if original_name == "offset":
                return "offset"
            if original_name == "order":
                return "order"
            if original_name == "orderby":
                return "orderby"
            if original_name == "properties":
                return "properties"
            return original_name
        
        # Filter by contentId.
        content_id: Optional[int] = None

        # Filter by description.
        description: Optional[str] = None

        # Filter by globalId.
        global_id: Optional[int] = None

        # Filter by artifact group.
        group: Optional[str] = None

        # Filter by label.  Include one or more label to only return artifacts containing all of thespecified labels.
        labels: Optional[List[str]] = None

        # The number of artifacts to return.  Defaults to 20.
        limit: Optional[int] = None

        # Filter by artifact name.
        name: Optional[str] = None

        # The number of artifacts to skip before starting to collect the result set.  Defaults to 0.
        offset: Optional[int] = None

        # Sort order, ascending (`asc`) or descending (`desc`).
        order: Optional[str] = None

        # The field to sort by.  Can be one of:* `name`* `createdOn`
        orderby: Optional[str] = None

        # Filter by one or more name/value property.  Separate each name/value pair using a colon.  Forexample `properties=foo:bar` will return only artifacts with a custom property named `foo`and value `bar`.
        properties: Optional[List[str]] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class ArtifactsRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request query parameters
        query_parameters: Optional[ArtifactsRequestBuilder.ArtifactsRequestBuilderGetQueryParameters] = None

    
    @dataclass
    class ArtifactsRequestBuilderPostQueryParameters():
        """
        Returns a paginated list of all artifacts with at least one version that matches theposted content.
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
            if original_name == "artifact_type":
                return "artifactType"
            if original_name == "canonical":
                return "canonical"
            if original_name == "limit":
                return "limit"
            if original_name == "offset":
                return "offset"
            if original_name == "order":
                return "order"
            if original_name == "orderby":
                return "orderby"
            return original_name
        
        # Indicates the type of artifact represented by the content being used for the search.  This is only needed when using the `canonical` query parameter, so that the server knows how to canonicalize the content prior to searching for matching artifacts.
        artifact_type: Optional[str] = None

        # Parameter that can be set to `true` to indicate that the server should "canonicalize" the content when searching for matching artifacts.  Canonicalization is unique to each artifact type, but typically involves removing any extra whitespace and formatting the content in a consistent manner.  Must be used along with the `artifactType` query parameter.
        canonical: Optional[bool] = None

        # The number of artifacts to return.  Defaults to 20.
        limit: Optional[int] = None

        # The number of artifacts to skip before starting to collect the result set.  Defaults to 0.
        offset: Optional[int] = None

        # Sort order, ascending (`asc`) or descending (`desc`).
        order: Optional[str] = None

        # The field to sort by.  Can be one of:* `name`* `createdOn`
        orderby: Optional[str] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class ArtifactsRequestBuilderPostRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request query parameters
        query_parameters: Optional[ArtifactsRequestBuilder.ArtifactsRequestBuilderPostQueryParameters] = None

    

