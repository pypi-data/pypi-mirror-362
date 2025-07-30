"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.ltca._928 import ConicalGearFilletStressResults
    from mastapy._private.gears.ltca._929 import ConicalGearRootFilletStressResults
    from mastapy._private.gears.ltca._930 import ContactResultType
    from mastapy._private.gears.ltca._931 import CylindricalGearFilletNodeStressResults
    from mastapy._private.gears.ltca._932 import (
        CylindricalGearFilletNodeStressResultsColumn,
    )
    from mastapy._private.gears.ltca._933 import (
        CylindricalGearFilletNodeStressResultsRow,
    )
    from mastapy._private.gears.ltca._934 import CylindricalGearRootFilletStressResults
    from mastapy._private.gears.ltca._935 import (
        CylindricalMeshedGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca._936 import GearBendingStiffness
    from mastapy._private.gears.ltca._937 import GearBendingStiffnessNode
    from mastapy._private.gears.ltca._938 import GearContactStiffness
    from mastapy._private.gears.ltca._939 import GearContactStiffnessNode
    from mastapy._private.gears.ltca._940 import GearFilletNodeStressResults
    from mastapy._private.gears.ltca._941 import GearFilletNodeStressResultsColumn
    from mastapy._private.gears.ltca._942 import GearFilletNodeStressResultsRow
    from mastapy._private.gears.ltca._943 import GearLoadDistributionAnalysis
    from mastapy._private.gears.ltca._944 import GearMeshLoadDistributionAnalysis
    from mastapy._private.gears.ltca._945 import GearMeshLoadDistributionAtRotation
    from mastapy._private.gears.ltca._946 import GearMeshLoadedContactLine
    from mastapy._private.gears.ltca._947 import GearMeshLoadedContactPoint
    from mastapy._private.gears.ltca._948 import GearRootFilletStressResults
    from mastapy._private.gears.ltca._949 import GearSetLoadDistributionAnalysis
    from mastapy._private.gears.ltca._950 import GearStiffness
    from mastapy._private.gears.ltca._951 import GearStiffnessNode
    from mastapy._private.gears.ltca._952 import (
        MeshedGearLoadDistributionAnalysisAtRotation,
    )
    from mastapy._private.gears.ltca._953 import UseAdvancedLTCAOptions
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.ltca._928": ["ConicalGearFilletStressResults"],
        "_private.gears.ltca._929": ["ConicalGearRootFilletStressResults"],
        "_private.gears.ltca._930": ["ContactResultType"],
        "_private.gears.ltca._931": ["CylindricalGearFilletNodeStressResults"],
        "_private.gears.ltca._932": ["CylindricalGearFilletNodeStressResultsColumn"],
        "_private.gears.ltca._933": ["CylindricalGearFilletNodeStressResultsRow"],
        "_private.gears.ltca._934": ["CylindricalGearRootFilletStressResults"],
        "_private.gears.ltca._935": ["CylindricalMeshedGearLoadDistributionAnalysis"],
        "_private.gears.ltca._936": ["GearBendingStiffness"],
        "_private.gears.ltca._937": ["GearBendingStiffnessNode"],
        "_private.gears.ltca._938": ["GearContactStiffness"],
        "_private.gears.ltca._939": ["GearContactStiffnessNode"],
        "_private.gears.ltca._940": ["GearFilletNodeStressResults"],
        "_private.gears.ltca._941": ["GearFilletNodeStressResultsColumn"],
        "_private.gears.ltca._942": ["GearFilletNodeStressResultsRow"],
        "_private.gears.ltca._943": ["GearLoadDistributionAnalysis"],
        "_private.gears.ltca._944": ["GearMeshLoadDistributionAnalysis"],
        "_private.gears.ltca._945": ["GearMeshLoadDistributionAtRotation"],
        "_private.gears.ltca._946": ["GearMeshLoadedContactLine"],
        "_private.gears.ltca._947": ["GearMeshLoadedContactPoint"],
        "_private.gears.ltca._948": ["GearRootFilletStressResults"],
        "_private.gears.ltca._949": ["GearSetLoadDistributionAnalysis"],
        "_private.gears.ltca._950": ["GearStiffness"],
        "_private.gears.ltca._951": ["GearStiffnessNode"],
        "_private.gears.ltca._952": ["MeshedGearLoadDistributionAnalysisAtRotation"],
        "_private.gears.ltca._953": ["UseAdvancedLTCAOptions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearFilletStressResults",
    "ConicalGearRootFilletStressResults",
    "ContactResultType",
    "CylindricalGearFilletNodeStressResults",
    "CylindricalGearFilletNodeStressResultsColumn",
    "CylindricalGearFilletNodeStressResultsRow",
    "CylindricalGearRootFilletStressResults",
    "CylindricalMeshedGearLoadDistributionAnalysis",
    "GearBendingStiffness",
    "GearBendingStiffnessNode",
    "GearContactStiffness",
    "GearContactStiffnessNode",
    "GearFilletNodeStressResults",
    "GearFilletNodeStressResultsColumn",
    "GearFilletNodeStressResultsRow",
    "GearLoadDistributionAnalysis",
    "GearMeshLoadDistributionAnalysis",
    "GearMeshLoadDistributionAtRotation",
    "GearMeshLoadedContactLine",
    "GearMeshLoadedContactPoint",
    "GearRootFilletStressResults",
    "GearSetLoadDistributionAnalysis",
    "GearStiffness",
    "GearStiffnessNode",
    "MeshedGearLoadDistributionAnalysisAtRotation",
    "UseAdvancedLTCAOptions",
)
