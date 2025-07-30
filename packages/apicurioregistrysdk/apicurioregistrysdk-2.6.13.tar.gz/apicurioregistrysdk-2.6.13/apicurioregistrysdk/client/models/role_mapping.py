from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .role_type import RoleType

@dataclass
class RoleMapping(AdditionalDataHolder, Parsable):
    """
    The mapping between a user/principal and their role.
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The principalId property
    principal_id: Optional[str] = None
    # A friendly name for the principal.
    principal_name: Optional[str] = None
    # The role property
    role: Optional[RoleType] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> RoleMapping:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RoleMapping
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return RoleMapping()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .role_type import RoleType

        from .role_type import RoleType

        fields: Dict[str, Callable[[Any], None]] = {
            "principalId": lambda n : setattr(self, 'principal_id', n.get_str_value()),
            "principalName": lambda n : setattr(self, 'principal_name', n.get_str_value()),
            "role": lambda n : setattr(self, 'role', n.get_enum_value(RoleType)),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("principalId", self.principal_id)
        writer.write_str_value("principalName", self.principal_name)
        writer.write_enum_value("role", self.role)
        writer.write_additional_data_value(self.additional_data)
    

