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
    from ....models.error import Error
    from ....models.rule import Rule

class WithRuleItemRequestBuilder(BaseRequestBuilder):
    """
    Manage the configuration of a single global artifact rule.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new WithRuleItemRequestBuilder and sets the default values.
        Args:
            path_parameters: The raw url or the Url template parameters for the request.
            request_adapter: The request adapter to use to execute the requests.
        """
        super().__init__(request_adapter, "{+baseurl}/admin/rules/{rule}", path_parameters)
    
    async def delete(self,request_configuration: Optional[WithRuleItemRequestBuilderDeleteRequestConfiguration] = None) -> None:
        """
        Deletes a single global rule.  If this is the only rule configured, this is the sameas deleting **all** rules.This operation can fail for the following reasons:* Invalid rule name/type (HTTP error `400`)* No rule with name/type `rule` exists (HTTP error `404`)* Rule cannot be deleted (HTTP error `409`)* A server error occurred (HTTP error `500`)
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        """
        request_info = self.to_delete_request_information(
            request_configuration
        )
        from ....models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    async def get(self,request_configuration: Optional[WithRuleItemRequestBuilderGetRequestConfiguration] = None) -> Optional[Rule]:
        """
        Returns information about the named globally configured rule.This operation can fail for the following reasons:* Invalid rule name/type (HTTP error `400`)* No rule with name/type `rule` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Rule]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ....models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.rule import Rule

        return await self.request_adapter.send_async(request_info, Rule, error_mapping)
    
    async def put(self,body: Optional[Rule] = None, request_configuration: Optional[WithRuleItemRequestBuilderPutRequestConfiguration] = None) -> Optional[Rule]:
        """
        Updates the configuration for a globally configured rule.This operation can fail for the following reasons:* Invalid rule name/type (HTTP error `400`)* No rule with name/type `rule` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        Args:
            body: The request body
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Rule]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_put_request_information(
            body, request_configuration
        )
        from ....models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.rule import Rule

        return await self.request_adapter.send_async(request_info, Rule, error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[WithRuleItemRequestBuilderDeleteRequestConfiguration] = None) -> RequestInformation:
        """
        Deletes a single global rule.  If this is the only rule configured, this is the sameas deleting **all** rules.This operation can fail for the following reasons:* Invalid rule name/type (HTTP error `400`)* No rule with name/type `rule` exists (HTTP error `404`)* Rule cannot be deleted (HTTP error `409`)* A server error occurred (HTTP error `500`)
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
    
    def to_get_request_information(self,request_configuration: Optional[WithRuleItemRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Returns information about the named globally configured rule.This operation can fail for the following reasons:* Invalid rule name/type (HTTP error `400`)* No rule with name/type `rule` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def to_put_request_information(self,body: Optional[Rule] = None, request_configuration: Optional[WithRuleItemRequestBuilderPutRequestConfiguration] = None) -> RequestInformation:
        """
        Updates the configuration for a globally configured rule.This operation can fail for the following reasons:* Invalid rule name/type (HTTP error `400`)* No rule with name/type `rule` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithRuleItemRequestBuilderDeleteRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithRuleItemRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithRuleItemRequestBuilderPutRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    

