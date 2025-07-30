"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.modal_analysis.gears._1994 import GearMeshForTE
    from mastapy._private.utility.modal_analysis.gears._1995 import GearOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1996 import GearPositions
    from mastapy._private.utility.modal_analysis.gears._1997 import HarmonicOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1998 import LabelOnlyOrder
    from mastapy._private.utility.modal_analysis.gears._1999 import OrderForTE
    from mastapy._private.utility.modal_analysis.gears._2000 import OrderSelector
    from mastapy._private.utility.modal_analysis.gears._2001 import OrderWithRadius
    from mastapy._private.utility.modal_analysis.gears._2002 import RollingBearingOrder
    from mastapy._private.utility.modal_analysis.gears._2003 import ShaftOrderForTE
    from mastapy._private.utility.modal_analysis.gears._2004 import (
        UserDefinedOrderForTE,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.modal_analysis.gears._1994": ["GearMeshForTE"],
        "_private.utility.modal_analysis.gears._1995": ["GearOrderForTE"],
        "_private.utility.modal_analysis.gears._1996": ["GearPositions"],
        "_private.utility.modal_analysis.gears._1997": ["HarmonicOrderForTE"],
        "_private.utility.modal_analysis.gears._1998": ["LabelOnlyOrder"],
        "_private.utility.modal_analysis.gears._1999": ["OrderForTE"],
        "_private.utility.modal_analysis.gears._2000": ["OrderSelector"],
        "_private.utility.modal_analysis.gears._2001": ["OrderWithRadius"],
        "_private.utility.modal_analysis.gears._2002": ["RollingBearingOrder"],
        "_private.utility.modal_analysis.gears._2003": ["ShaftOrderForTE"],
        "_private.utility.modal_analysis.gears._2004": ["UserDefinedOrderForTE"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "GearMeshForTE",
    "GearOrderForTE",
    "GearPositions",
    "HarmonicOrderForTE",
    "LabelOnlyOrder",
    "OrderForTE",
    "OrderSelector",
    "OrderWithRadius",
    "RollingBearingOrder",
    "ShaftOrderForTE",
    "UserDefinedOrderForTE",
)
