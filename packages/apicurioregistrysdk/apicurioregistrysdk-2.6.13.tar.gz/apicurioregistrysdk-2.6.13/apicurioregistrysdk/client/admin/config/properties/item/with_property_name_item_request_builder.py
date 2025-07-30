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
    from .....models.configuration_property import ConfigurationProperty
    from .....models.error import Error
    from .....models.update_configuration_property import UpdateConfigurationProperty

class WithPropertyNameItemRequestBuilder(BaseRequestBuilder):
    """
    Manage a single configuration property (by name).
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new WithPropertyNameItemRequestBuilder and sets the default values.
        Args:
            path_parameters: The raw url or the Url template parameters for the request.
            request_adapter: The request adapter to use to execute the requests.
        """
        super().__init__(request_adapter, "{+baseurl}/admin/config/properties/{propertyName}", path_parameters)
    
    async def delete(self,request_configuration: Optional[WithPropertyNameItemRequestBuilderDeleteRequestConfiguration] = None) -> None:
        """
        Resets the value of a single configuration property.  This will return the property toits default value (see external documentation for supported properties and their defaultvalues).This operation may fail for one of the following reasons:* Property not found or not configured (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    async def get(self,request_configuration: Optional[WithPropertyNameItemRequestBuilderGetRequestConfiguration] = None) -> Optional[ConfigurationProperty]:
        """
        Returns the value of a single configuration property.This operation may fail for one of the following reasons:* Property not found or not configured (HTTP error `404`)* A server error occurred (HTTP error `500`)
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ConfigurationProperty]
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
        from .....models.configuration_property import ConfigurationProperty

        return await self.request_adapter.send_async(request_info, ConfigurationProperty, error_mapping)
    
    async def put(self,body: Optional[UpdateConfigurationProperty] = None, request_configuration: Optional[WithPropertyNameItemRequestBuilderPutRequestConfiguration] = None) -> None:
        """
        Updates the value of a single configuration property.This operation may fail for one of the following reasons:* Property not found or not configured (HTTP error `404`)* A server error occurred (HTTP error `500`)
        Args:
            body: The request body
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_put_request_information(
            body, request_configuration
        )
        from .....models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[WithPropertyNameItemRequestBuilderDeleteRequestConfiguration] = None) -> RequestInformation:
        """
        Resets the value of a single configuration property.  This will return the property toits default value (see external documentation for supported properties and their defaultvalues).This operation may fail for one of the following reasons:* Property not found or not configured (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def to_get_request_information(self,request_configuration: Optional[WithPropertyNameItemRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Returns the value of a single configuration property.This operation may fail for one of the following reasons:* Property not found or not configured (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
            request_info.add_request_options(request_configuration.options)
        return request_info
    
    def to_put_request_information(self,body: Optional[UpdateConfigurationProperty] = None, request_configuration: Optional[WithPropertyNameItemRequestBuilderPutRequestConfiguration] = None) -> RequestInformation:
        """
        Updates the value of a single configuration property.This operation may fail for one of the following reasons:* Property not found or not configured (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithPropertyNameItemRequestBuilderDeleteRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithPropertyNameItemRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithPropertyNameItemRequestBuilderPutRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    

