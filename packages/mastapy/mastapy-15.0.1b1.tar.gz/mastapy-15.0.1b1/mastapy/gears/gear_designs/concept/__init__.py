"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.concept._1296 import ConceptGearDesign
    from mastapy._private.gears.gear_designs.concept._1297 import ConceptGearMeshDesign
    from mastapy._private.gears.gear_designs.concept._1298 import ConceptGearSetDesign
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.concept._1296": ["ConceptGearDesign"],
        "_private.gears.gear_designs.concept._1297": ["ConceptGearMeshDesign"],
        "_private.gears.gear_designs.concept._1298": ["ConceptGearSetDesign"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConceptGearDesign",
    "ConceptGearMeshDesign",
    "ConceptGearSetDesign",
)
