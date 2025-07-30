from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_global_item_request_builder import WithGlobalItemRequestBuilder

class GlobalIdsRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /ids/globalIds
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new GlobalIdsRequestBuilder and sets the default values.
        Args:
            path_parameters: The raw url or the Url template parameters for the request.
            request_adapter: The request adapter to use to execute the requests.
        """
        super().__init__(request_adapter, "{+baseurl}/ids/globalIds", path_parameters)
    
    def by_global_id(self,global_id: str) -> WithGlobalItemRequestBuilder:
        """
        Access artifact content utilizing an artifact version's globally unique identifier.
        Args:
            global_id: Unique identifier of the item
        Returns: WithGlobalItemRequestBuilder
        """
        if not global_id:
            raise TypeError("global_id cannot be null.")
        from .item.with_global_item_request_builder import WithGlobalItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["globalId"] = global_id
        return WithGlobalItemRequestBuilder(self.request_adapter, url_tpl_params)
    

