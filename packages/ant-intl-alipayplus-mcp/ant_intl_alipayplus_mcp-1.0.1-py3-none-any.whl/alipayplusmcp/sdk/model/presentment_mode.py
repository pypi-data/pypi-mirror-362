from enum import Enum, unique


@unique
class PresentmentMode(Enum):
    BUNDLE = "BUNDLE"
    TILED = "TILED"
    UNIFIED = "UNIFIED"

    def to_aps_dict(self):
        return self.name
