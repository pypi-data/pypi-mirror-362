"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.gears.materials._2804 import (
        GearMaterialExpertSystemMaterialDetails,
    )
    from mastapy._private.system_model.part_model.gears.materials._2805 import (
        GearMaterialExpertSystemMaterialOptions,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.gears.materials._2804": [
            "GearMaterialExpertSystemMaterialDetails"
        ],
        "_private.system_model.part_model.gears.materials._2805": [
            "GearMaterialExpertSystemMaterialOptions"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "GearMaterialExpertSystemMaterialDetails",
    "GearMaterialExpertSystemMaterialOptions",
)
