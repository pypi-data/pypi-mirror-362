"""__init__.

All modules in this sub-package were hand-written.
"""

from .color import Color
from .matrix_2x2 import Matrix2x2
from .matrix_3x3 import Matrix3x3
from .matrix_4x4 import Matrix4x4
from .scalar import approximately_equal, clamp, fract, sign, smoothstep, step
from .types import Long
from .vector_2d import Vector2D
from .vector_3d import Vector3D
from .vector_4d import Vector4D

__all__ = (
    "clamp",
    "sign",
    "fract",
    "step",
    "smoothstep",
    "approximately_equal",
    "Long",
    "Vector2D",
    "Vector3D",
    "Vector4D",
    "Color",
    "Matrix2x2",
    "Matrix3x3",
    "Matrix4x4",
)
