from enum import Enum

class ArtifactState(str, Enum):
    ENABLED = "ENABLED",
    DISABLED = "DISABLED",
    DEPRECATED = "DEPRECATED",

