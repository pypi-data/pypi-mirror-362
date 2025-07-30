from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .error import Error

from .error import Error

@dataclass
class RuleViolationError(Error):
    """
    All error responses, whether `4xx` or `5xx` will include one of these as the responsebody.
    """
    # Full details about the error.  This might contain a server stack trace, for example.
    detail: Optional[str] = None
    # The server-side error code.
    error_code: Optional[int] = None
    # The short error message.
    message: Optional[str] = None
    # The error name - typically the classname of the exception thrown by the server.
    name: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> RuleViolationError:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RuleViolationError
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return RuleViolationError()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .error import Error

        from .error import Error

        fields: Dict[str, Callable[[Any], None]] = {
        }
        super_fields = super().get_field_deserializers()
        fields.update(super_fields)
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if not writer:
            raise TypeError("writer cannot be null.")
        super().serialize(writer)
    

