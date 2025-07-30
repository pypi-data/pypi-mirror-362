"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.bevel.cutters._916 import (
        PinionFinishCutter,
    )
    from mastapy._private.gears.manufacturing.bevel.cutters._917 import (
        PinionRoughCutter,
    )
    from mastapy._private.gears.manufacturing.bevel.cutters._918 import (
        WheelFinishCutter,
    )
    from mastapy._private.gears.manufacturing.bevel.cutters._919 import WheelRoughCutter
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.bevel.cutters._916": ["PinionFinishCutter"],
        "_private.gears.manufacturing.bevel.cutters._917": ["PinionRoughCutter"],
        "_private.gears.manufacturing.bevel.cutters._918": ["WheelFinishCutter"],
        "_private.gears.manufacturing.bevel.cutters._919": ["WheelRoughCutter"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "PinionFinishCutter",
    "PinionRoughCutter",
    "WheelFinishCutter",
    "WheelRoughCutter",
)
