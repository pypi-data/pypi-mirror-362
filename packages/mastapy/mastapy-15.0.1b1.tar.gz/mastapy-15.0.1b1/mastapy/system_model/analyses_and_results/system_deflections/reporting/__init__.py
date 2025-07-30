"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3085 import (
        CylindricalGearMeshMisalignmentValue,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3086 import (
        FlexibleGearChart,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3087 import (
        GearInMeshDeflectionResults,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3088 import (
        GearMeshResultsAtOffset,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3089 import (
        PlanetCarrierWindup,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3090 import (
        PlanetPinWindup,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3091 import (
        RigidlyConnectedComponentGroupSystemDeflection,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3092 import (
        ShaftSystemDeflectionSectionsReport,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3093 import (
        SplineFlankContactReporting,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.system_deflections.reporting._3085": [
            "CylindricalGearMeshMisalignmentValue"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3086": [
            "FlexibleGearChart"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3087": [
            "GearInMeshDeflectionResults"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3088": [
            "GearMeshResultsAtOffset"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3089": [
            "PlanetCarrierWindup"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3090": [
            "PlanetPinWindup"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3091": [
            "RigidlyConnectedComponentGroupSystemDeflection"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3092": [
            "ShaftSystemDeflectionSectionsReport"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3093": [
            "SplineFlankContactReporting"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearMeshMisalignmentValue",
    "FlexibleGearChart",
    "GearInMeshDeflectionResults",
    "GearMeshResultsAtOffset",
    "PlanetCarrierWindup",
    "PlanetPinWindup",
    "RigidlyConnectedComponentGroupSystemDeflection",
    "ShaftSystemDeflectionSectionsReport",
    "SplineFlankContactReporting",
)
