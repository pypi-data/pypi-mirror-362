"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.tolerances._2104 import BearingConnectionComponent
    from mastapy._private.bearings.tolerances._2105 import InternalClearanceClass
    from mastapy._private.bearings.tolerances._2106 import BearingToleranceClass
    from mastapy._private.bearings.tolerances._2107 import (
        BearingToleranceDefinitionOptions,
    )
    from mastapy._private.bearings.tolerances._2108 import FitType
    from mastapy._private.bearings.tolerances._2109 import InnerRingTolerance
    from mastapy._private.bearings.tolerances._2110 import InnerSupportTolerance
    from mastapy._private.bearings.tolerances._2111 import InterferenceDetail
    from mastapy._private.bearings.tolerances._2112 import InterferenceTolerance
    from mastapy._private.bearings.tolerances._2113 import ITDesignation
    from mastapy._private.bearings.tolerances._2114 import MountingSleeveDiameterDetail
    from mastapy._private.bearings.tolerances._2115 import OuterRingTolerance
    from mastapy._private.bearings.tolerances._2116 import OuterSupportTolerance
    from mastapy._private.bearings.tolerances._2117 import RaceRoundnessAtAngle
    from mastapy._private.bearings.tolerances._2118 import RadialSpecificationMethod
    from mastapy._private.bearings.tolerances._2119 import RingDetail
    from mastapy._private.bearings.tolerances._2120 import RingTolerance
    from mastapy._private.bearings.tolerances._2121 import RoundnessSpecification
    from mastapy._private.bearings.tolerances._2122 import RoundnessSpecificationType
    from mastapy._private.bearings.tolerances._2123 import SupportDetail
    from mastapy._private.bearings.tolerances._2124 import SupportMaterialSource
    from mastapy._private.bearings.tolerances._2125 import SupportTolerance
    from mastapy._private.bearings.tolerances._2126 import (
        SupportToleranceLocationDesignation,
    )
    from mastapy._private.bearings.tolerances._2127 import ToleranceCombination
    from mastapy._private.bearings.tolerances._2128 import TypeOfFit
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.tolerances._2104": ["BearingConnectionComponent"],
        "_private.bearings.tolerances._2105": ["InternalClearanceClass"],
        "_private.bearings.tolerances._2106": ["BearingToleranceClass"],
        "_private.bearings.tolerances._2107": ["BearingToleranceDefinitionOptions"],
        "_private.bearings.tolerances._2108": ["FitType"],
        "_private.bearings.tolerances._2109": ["InnerRingTolerance"],
        "_private.bearings.tolerances._2110": ["InnerSupportTolerance"],
        "_private.bearings.tolerances._2111": ["InterferenceDetail"],
        "_private.bearings.tolerances._2112": ["InterferenceTolerance"],
        "_private.bearings.tolerances._2113": ["ITDesignation"],
        "_private.bearings.tolerances._2114": ["MountingSleeveDiameterDetail"],
        "_private.bearings.tolerances._2115": ["OuterRingTolerance"],
        "_private.bearings.tolerances._2116": ["OuterSupportTolerance"],
        "_private.bearings.tolerances._2117": ["RaceRoundnessAtAngle"],
        "_private.bearings.tolerances._2118": ["RadialSpecificationMethod"],
        "_private.bearings.tolerances._2119": ["RingDetail"],
        "_private.bearings.tolerances._2120": ["RingTolerance"],
        "_private.bearings.tolerances._2121": ["RoundnessSpecification"],
        "_private.bearings.tolerances._2122": ["RoundnessSpecificationType"],
        "_private.bearings.tolerances._2123": ["SupportDetail"],
        "_private.bearings.tolerances._2124": ["SupportMaterialSource"],
        "_private.bearings.tolerances._2125": ["SupportTolerance"],
        "_private.bearings.tolerances._2126": ["SupportToleranceLocationDesignation"],
        "_private.bearings.tolerances._2127": ["ToleranceCombination"],
        "_private.bearings.tolerances._2128": ["TypeOfFit"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingConnectionComponent",
    "InternalClearanceClass",
    "BearingToleranceClass",
    "BearingToleranceDefinitionOptions",
    "FitType",
    "InnerRingTolerance",
    "InnerSupportTolerance",
    "InterferenceDetail",
    "InterferenceTolerance",
    "ITDesignation",
    "MountingSleeveDiameterDetail",
    "OuterRingTolerance",
    "OuterSupportTolerance",
    "RaceRoundnessAtAngle",
    "RadialSpecificationMethod",
    "RingDetail",
    "RingTolerance",
    "RoundnessSpecification",
    "RoundnessSpecificationType",
    "SupportDetail",
    "SupportMaterialSource",
    "SupportTolerance",
    "SupportToleranceLocationDesignation",
    "ToleranceCombination",
    "TypeOfFit",
)
