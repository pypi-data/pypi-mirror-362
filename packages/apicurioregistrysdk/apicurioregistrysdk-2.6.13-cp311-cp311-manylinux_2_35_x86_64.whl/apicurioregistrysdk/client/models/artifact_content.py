from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .artifact_reference import ArtifactReference

@dataclass
class ArtifactContent(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Raw content of the artifact or a valid (and accessible) URL where the content can be found.
    content: Optional[str] = None
    # Collection of references to other artifacts.
    references: Optional[List[ArtifactReference]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> ArtifactContent:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ArtifactContent
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ArtifactContent()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .artifact_reference import ArtifactReference

        from .artifact_reference import ArtifactReference

        fields: Dict[str, Callable[[Any], None]] = {
            "content": lambda n : setattr(self, 'content', n.get_str_value()),
            "references": lambda n : setattr(self, 'references', n.get_collection_of_object_values(ArtifactReference)),
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
        writer.write_str_value("content", self.content)
        writer.write_collection_of_object_values("references", self.references)
        writer.write_additional_data_value(self.additional_data)
    

