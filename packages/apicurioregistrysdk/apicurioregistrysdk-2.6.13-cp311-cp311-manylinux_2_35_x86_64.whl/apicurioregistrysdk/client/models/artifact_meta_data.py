from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .artifact_reference import ArtifactReference
    from .artifact_state import ArtifactState
    from .properties import Properties

@dataclass
class ArtifactMetaData(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The contentId property
    content_id: Optional[int] = None
    # The createdBy property
    created_by: Optional[str] = None
    # The createdOn property
    created_on: Optional[datetime.datetime] = None
    # The description property
    description: Optional[str] = None
    # The globalId property
    global_id: Optional[int] = None
    # An ID of a single artifact group.
    group_id: Optional[str] = None
    # The ID of a single artifact.
    id: Optional[str] = None
    # The labels property
    labels: Optional[List[str]] = None
    # The modifiedBy property
    modified_by: Optional[str] = None
    # The modifiedOn property
    modified_on: Optional[datetime.datetime] = None
    # The name property
    name: Optional[str] = None
    # User-defined name-value pairs. Name and value must be strings.
    properties: Optional[Properties] = None
    # The references property
    references: Optional[List[ArtifactReference]] = None
    # Describes the state of an artifact or artifact version.  The following statesare possible:* ENABLED* DISABLED* DEPRECATED
    state: Optional[ArtifactState] = None
    # The type property
    type: Optional[str] = None
    # The version property
    version: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> ArtifactMetaData:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ArtifactMetaData
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ArtifactMetaData()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .artifact_reference import ArtifactReference
        from .artifact_state import ArtifactState
        from .properties import Properties

        from .artifact_reference import ArtifactReference
        from .artifact_state import ArtifactState
        from .properties import Properties

        fields: Dict[str, Callable[[Any], None]] = {
            "contentId": lambda n : setattr(self, 'content_id', n.get_int_value()),
            "createdBy": lambda n : setattr(self, 'created_by', n.get_str_value()),
            "createdOn": lambda n : setattr(self, 'created_on', n.get_datetime_value()),
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "globalId": lambda n : setattr(self, 'global_id', n.get_int_value()),
            "groupId": lambda n : setattr(self, 'group_id', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "labels": lambda n : setattr(self, 'labels', n.get_collection_of_primitive_values(str)),
            "modifiedBy": lambda n : setattr(self, 'modified_by', n.get_str_value()),
            "modifiedOn": lambda n : setattr(self, 'modified_on', n.get_datetime_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "properties": lambda n : setattr(self, 'properties', n.get_object_value(Properties)),
            "references": lambda n : setattr(self, 'references', n.get_collection_of_object_values(ArtifactReference)),
            "state": lambda n : setattr(self, 'state', n.get_enum_value(ArtifactState)),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
            "version": lambda n : setattr(self, 'version', n.get_str_value()),
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
        writer.write_int_value("contentId", self.content_id)
        writer.write_str_value("createdBy", self.created_by)
        writer.write_datetime_value("createdOn", self.created_on)
        writer.write_str_value("description", self.description)
        writer.write_int_value("globalId", self.global_id)
        writer.write_str_value("groupId", self.group_id)
        writer.write_str_value("id", self.id)
        writer.write_collection_of_primitive_values("labels", self.labels)
        writer.write_str_value("modifiedBy", self.modified_by)
        writer.write_datetime_value("modifiedOn", self.modified_on)
        writer.write_str_value("name", self.name)
        writer.write_object_value("properties", self.properties)
        writer.write_collection_of_object_values("references", self.references)
        writer.write_enum_value("state", self.state)
        writer.write_str_value("type", self.type)
        writer.write_str_value("version", self.version)
        writer.write_additional_data_value(self.additional_data)
    

