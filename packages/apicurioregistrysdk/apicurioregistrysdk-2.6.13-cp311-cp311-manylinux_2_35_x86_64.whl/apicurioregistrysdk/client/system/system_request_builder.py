from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .info.info_request_builder import InfoRequestBuilder
    from .limits.limits_request_builder import LimitsRequestBuilder

class SystemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /system
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new SystemRequestBuilder and sets the default values.
        Args:
            path_parameters: The raw url or the Url template parameters for the request.
            request_adapter: The request adapter to use to execute the requests.
        """
        super().__init__(request_adapter, "{+baseurl}/system", path_parameters)
    
    @property
    def info(self) -> InfoRequestBuilder:
        """
        Retrieve system information
        """
        from .info.info_request_builder import InfoRequestBuilder

        return InfoRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def limits(self) -> LimitsRequestBuilder:
        """
        Retrieve resource limits information
        """
        from .limits.limits_request_builder import LimitsRequestBuilder

        return LimitsRequestBuilder(self.request_adapter, self.path_parameters)
    

