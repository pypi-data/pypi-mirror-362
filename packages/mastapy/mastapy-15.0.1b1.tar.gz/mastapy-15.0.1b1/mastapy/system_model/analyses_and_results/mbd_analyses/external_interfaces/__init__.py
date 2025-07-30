"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.external_interfaces._5816 import (
        DynamicExternalInterfaceOptions,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.mbd_analyses.external_interfaces._5816": [
            "DynamicExternalInterfaceOptions"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = ("DynamicExternalInterfaceOptions",)
