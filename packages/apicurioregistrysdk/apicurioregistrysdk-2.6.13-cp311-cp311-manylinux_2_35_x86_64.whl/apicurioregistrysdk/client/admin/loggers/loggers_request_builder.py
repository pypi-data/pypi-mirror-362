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
    from ...models.error import Error
    from ...models.log_configuration import LogConfiguration
    from .item.with_logger_item_request_builder import WithLoggerItemRequestBuilder

class LoggersRequestBuilder(BaseRequestBuilder):
    """
    Manage logger settings/configurations.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new LoggersRequestBuilder and sets the default values.
        Args:
            path_parameters: The raw url or the Url template parameters for the request.
            request_adapter: The request adapter to use to execute the requests.
        """
        super().__init__(request_adapter, "{+baseurl}/admin/loggers", path_parameters)
    
    def by_logger(self,logger: str) -> WithLoggerItemRequestBuilder:
        """
        Manage logger settings/configurations.
        Args:
            logger: Unique identifier of the item
        Returns: WithLoggerItemRequestBuilder
        """
        if not logger:
            raise TypeError("logger cannot be null.")
        from .item.with_logger_item_request_builder import WithLoggerItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["logger"] = logger
        return WithLoggerItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[LoggersRequestBuilderGetRequestConfiguration] = None) -> Optional[List[LogConfiguration]]:
        """
        List all of the configured logging levels.  These override the defaultlogging configuration.
        Args:
            request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[List[LogConfiguration]]
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
        from ...models.log_configuration import LogConfiguration

        return await self.request_adapter.send_collection_async(request_info, LogConfiguration, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[LoggersRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        List all of the configured logging levels.  These override the defaultlogging configuration.
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
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class LoggersRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    

