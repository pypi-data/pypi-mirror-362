"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.part_groups._2721 import (
        ConcentricOrParallelPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2722 import (
        ConcentricPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2723 import (
        ConcentricPartGroupParallelToThis,
    )
    from mastapy._private.system_model.part_model.part_groups._2724 import (
        DesignMeasurements,
    )
    from mastapy._private.system_model.part_model.part_groups._2725 import (
        ParallelPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2726 import (
        ParallelPartGroupSelection,
    )
    from mastapy._private.system_model.part_model.part_groups._2727 import PartGroup
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.part_groups._2721": [
            "ConcentricOrParallelPartGroup"
        ],
        "_private.system_model.part_model.part_groups._2722": ["ConcentricPartGroup"],
        "_private.system_model.part_model.part_groups._2723": [
            "ConcentricPartGroupParallelToThis"
        ],
        "_private.system_model.part_model.part_groups._2724": ["DesignMeasurements"],
        "_private.system_model.part_model.part_groups._2725": ["ParallelPartGroup"],
        "_private.system_model.part_model.part_groups._2726": [
            "ParallelPartGroupSelection"
        ],
        "_private.system_model.part_model.part_groups._2727": ["PartGroup"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConcentricOrParallelPartGroup",
    "ConcentricPartGroup",
    "ConcentricPartGroupParallelToThis",
    "DesignMeasurements",
    "ParallelPartGroup",
    "ParallelPartGroupSelection",
    "PartGroup",
)
