"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.face._536 import FaceGearDutyCycleRating
    from mastapy._private.gears.rating.face._537 import FaceGearMeshDutyCycleRating
    from mastapy._private.gears.rating.face._538 import FaceGearMeshRating
    from mastapy._private.gears.rating.face._539 import FaceGearRating
    from mastapy._private.gears.rating.face._540 import FaceGearSetDutyCycleRating
    from mastapy._private.gears.rating.face._541 import FaceGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.face._536": ["FaceGearDutyCycleRating"],
        "_private.gears.rating.face._537": ["FaceGearMeshDutyCycleRating"],
        "_private.gears.rating.face._538": ["FaceGearMeshRating"],
        "_private.gears.rating.face._539": ["FaceGearRating"],
        "_private.gears.rating.face._540": ["FaceGearSetDutyCycleRating"],
        "_private.gears.rating.face._541": ["FaceGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FaceGearDutyCycleRating",
    "FaceGearMeshDutyCycleRating",
    "FaceGearMeshRating",
    "FaceGearRating",
    "FaceGearSetDutyCycleRating",
    "FaceGearSetRating",
)
