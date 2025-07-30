"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.ltca.cylindrical._954 import (
        CylindricalGearBendingStiffness,
    )
    from mastapy._private.gears.ltca.cylindrical._955 import (
        CylindricalGearBendingStiffnessNode,
    )
    from mastapy._private.gears.ltca.cylindrical._956 import (
        CylindricalGearContactStiffness,
    )
    from mastapy._private.gears.ltca.cylindrical._957 import (
        CylindricalGearContactStiffnessNode,
    )
    from mastapy._private.gears.ltca.cylindrical._958 import CylindricalGearFESettings
    from mastapy._private.gears.ltca.cylindrical._959 import (
        CylindricalGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.cylindrical._960 import (
        CylindricalGearMeshLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.cylindrical._961 import (
        CylindricalGearMeshLoadedContactLine,
    )
    from mastapy._private.gears.ltca.cylindrical._962 import (
        CylindricalGearMeshLoadedContactPoint,
    )
    from mastapy._private.gears.ltca.cylindrical._963 import (
        CylindricalGearSetLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.cylindrical._964 import (
        CylindricalMeshLoadDistributionAtRotation,
    )
    from mastapy._private.gears.ltca.cylindrical._965 import (
        FaceGearSetLoadDistributionAnalysis,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.ltca.cylindrical._954": ["CylindricalGearBendingStiffness"],
        "_private.gears.ltca.cylindrical._955": ["CylindricalGearBendingStiffnessNode"],
        "_private.gears.ltca.cylindrical._956": ["CylindricalGearContactStiffness"],
        "_private.gears.ltca.cylindrical._957": ["CylindricalGearContactStiffnessNode"],
        "_private.gears.ltca.cylindrical._958": ["CylindricalGearFESettings"],
        "_private.gears.ltca.cylindrical._959": [
            "CylindricalGearLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.cylindrical._960": [
            "CylindricalGearMeshLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.cylindrical._961": [
            "CylindricalGearMeshLoadedContactLine"
        ],
        "_private.gears.ltca.cylindrical._962": [
            "CylindricalGearMeshLoadedContactPoint"
        ],
        "_private.gears.ltca.cylindrical._963": [
            "CylindricalGearSetLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.cylindrical._964": [
            "CylindricalMeshLoadDistributionAtRotation"
        ],
        "_private.gears.ltca.cylindrical._965": ["FaceGearSetLoadDistributionAnalysis"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearBendingStiffness",
    "CylindricalGearBendingStiffnessNode",
    "CylindricalGearContactStiffness",
    "CylindricalGearContactStiffnessNode",
    "CylindricalGearFESettings",
    "CylindricalGearLoadDistributionAnalysis",
    "CylindricalGearMeshLoadDistributionAnalysis",
    "CylindricalGearMeshLoadedContactLine",
    "CylindricalGearMeshLoadedContactPoint",
    "CylindricalGearSetLoadDistributionAnalysis",
    "CylindricalMeshLoadDistributionAtRotation",
    "FaceGearSetLoadDistributionAnalysis",
)
