"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.fe_tools.vis_tools_global._1353 import ElementEdge
    from mastapy._private.fe_tools.vis_tools_global._1354 import ElementFace
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.fe_tools.vis_tools_global._1353": ["ElementEdge"],
        "_private.fe_tools.vis_tools_global._1354": ["ElementFace"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ElementEdge",
    "ElementFace",
)
