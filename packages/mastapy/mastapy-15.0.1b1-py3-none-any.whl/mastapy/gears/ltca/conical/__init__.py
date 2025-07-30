"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.ltca.conical._966 import ConicalGearBendingStiffness
    from mastapy._private.gears.ltca.conical._967 import ConicalGearBendingStiffnessNode
    from mastapy._private.gears.ltca.conical._968 import ConicalGearContactStiffness
    from mastapy._private.gears.ltca.conical._969 import ConicalGearContactStiffnessNode
    from mastapy._private.gears.ltca.conical._970 import (
        ConicalGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._971 import (
        ConicalGearSetLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._972 import (
        ConicalMeshedGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._973 import (
        ConicalMeshLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._974 import (
        ConicalMeshLoadDistributionAtRotation,
    )
    from mastapy._private.gears.ltca.conical._975 import ConicalMeshLoadedContactLine
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.ltca.conical._966": ["ConicalGearBendingStiffness"],
        "_private.gears.ltca.conical._967": ["ConicalGearBendingStiffnessNode"],
        "_private.gears.ltca.conical._968": ["ConicalGearContactStiffness"],
        "_private.gears.ltca.conical._969": ["ConicalGearContactStiffnessNode"],
        "_private.gears.ltca.conical._970": ["ConicalGearLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._971": ["ConicalGearSetLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._972": [
            "ConicalMeshedGearLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.conical._973": ["ConicalMeshLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._974": ["ConicalMeshLoadDistributionAtRotation"],
        "_private.gears.ltca.conical._975": ["ConicalMeshLoadedContactLine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearBendingStiffness",
    "ConicalGearBendingStiffnessNode",
    "ConicalGearContactStiffness",
    "ConicalGearContactStiffnessNode",
    "ConicalGearLoadDistributionAnalysis",
    "ConicalGearSetLoadDistributionAnalysis",
    "ConicalMeshedGearLoadDistributionAnalysis",
    "ConicalMeshLoadDistributionAnalysis",
    "ConicalMeshLoadDistributionAtRotation",
    "ConicalMeshLoadedContactLine",
)
