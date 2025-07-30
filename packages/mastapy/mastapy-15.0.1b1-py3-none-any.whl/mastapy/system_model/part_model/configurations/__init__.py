"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.configurations._2857 import (
        ActiveFESubstructureSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2858 import (
        ActiveFESubstructureSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2859 import (
        ActiveShaftDesignSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2860 import (
        ActiveShaftDesignSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2861 import (
        BearingDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2862 import (
        BearingDetailSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2863 import (
        DesignConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2864 import (
        PartDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2865 import (
        PartDetailSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.configurations._2857": [
            "ActiveFESubstructureSelection"
        ],
        "_private.system_model.part_model.configurations._2858": [
            "ActiveFESubstructureSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2859": [
            "ActiveShaftDesignSelection"
        ],
        "_private.system_model.part_model.configurations._2860": [
            "ActiveShaftDesignSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2861": [
            "BearingDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2862": [
            "BearingDetailSelection"
        ],
        "_private.system_model.part_model.configurations._2863": [
            "DesignConfiguration"
        ],
        "_private.system_model.part_model.configurations._2864": [
            "PartDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2865": [
            "PartDetailSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ActiveFESubstructureSelection",
    "ActiveFESubstructureSelectionGroup",
    "ActiveShaftDesignSelection",
    "ActiveShaftDesignSelectionGroup",
    "BearingDetailConfiguration",
    "BearingDetailSelection",
    "DesignConfiguration",
    "PartDetailConfiguration",
    "PartDetailSelection",
)
