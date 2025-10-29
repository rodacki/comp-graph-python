# src/cg_examples/ex07_2D_Editor_Qt/state/transform_mode.py
from enum import Enum, auto


class TransformMode(Enum):
    TRANSLATE = auto()
    SCALE = auto()
    ROTATE = auto()

    def __str__(self) -> str:
        return self.name.lower()
