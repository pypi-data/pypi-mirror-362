from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_content_item_request_builder import WithContentItemRequestBuilder

class ContentIdsRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /ids/contentIds
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new ContentIdsRequestBuilder and sets the default values.
        Args:
            path_parameters: The raw url or the Url template parameters for the request.
            request_adapter: The request adapter to use to execute the requests.
        """
        super().__init__(request_adapter, "{+baseurl}/ids/contentIds", path_parameters)
    
    def by_content_id(self,content_id: str) -> WithContentItemRequestBuilder:
        """
        Access artifact content utilizing the unique content identifier for that content.
        Args:
            content_id: Unique identifier of the item
        Returns: WithContentItemRequestBuilder
        """
        if not content_id:
            raise TypeError("content_id cannot be null.")
        from .item.with_content_item_request_builder import WithContentItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["contentId"] = content_id
        return WithContentItemRequestBuilder(self.request_adapter, url_tpl_params)
    

