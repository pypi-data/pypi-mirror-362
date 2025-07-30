"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.concept._639 import ConceptGearDutyCycleRating
    from mastapy._private.gears.rating.concept._640 import (
        ConceptGearMeshDutyCycleRating,
    )
    from mastapy._private.gears.rating.concept._641 import ConceptGearMeshRating
    from mastapy._private.gears.rating.concept._642 import ConceptGearRating
    from mastapy._private.gears.rating.concept._643 import ConceptGearSetDutyCycleRating
    from mastapy._private.gears.rating.concept._644 import ConceptGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.concept._639": ["ConceptGearDutyCycleRating"],
        "_private.gears.rating.concept._640": ["ConceptGearMeshDutyCycleRating"],
        "_private.gears.rating.concept._641": ["ConceptGearMeshRating"],
        "_private.gears.rating.concept._642": ["ConceptGearRating"],
        "_private.gears.rating.concept._643": ["ConceptGearSetDutyCycleRating"],
        "_private.gears.rating.concept._644": ["ConceptGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConceptGearDutyCycleRating",
    "ConceptGearMeshDutyCycleRating",
    "ConceptGearMeshRating",
    "ConceptGearRating",
    "ConceptGearSetDutyCycleRating",
    "ConceptGearSetRating",
)
