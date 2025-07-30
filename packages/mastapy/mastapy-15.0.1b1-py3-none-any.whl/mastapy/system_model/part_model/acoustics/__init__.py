"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.acoustics._2866 import (
        AcousticAnalysisOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2867 import (
        AcousticAnalysisSetup,
    )
    from mastapy._private.system_model.part_model.acoustics._2868 import (
        AcousticAnalysisSetupCacheReporting,
    )
    from mastapy._private.system_model.part_model.acoustics._2869 import (
        AcousticAnalysisSetupCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2870 import (
        AcousticEnvelopeType,
    )
    from mastapy._private.system_model.part_model.acoustics._2871 import (
        AcousticInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2872 import (
        CacheMemoryEstimates,
    )
    from mastapy._private.system_model.part_model.acoustics._2873 import (
        FEPartInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2874 import (
        FESurfaceSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2875 import HoleInFaceGroup
    from mastapy._private.system_model.part_model.acoustics._2876 import (
        MeshedResultPlane,
    )
    from mastapy._private.system_model.part_model.acoustics._2877 import (
        MeshedResultSphere,
    )
    from mastapy._private.system_model.part_model.acoustics._2878 import (
        MeshedResultSurface,
    )
    from mastapy._private.system_model.part_model.acoustics._2879 import (
        MeshedResultSurfaceBase,
    )
    from mastapy._private.system_model.part_model.acoustics._2880 import (
        MicrophoneArrayDesign,
    )
    from mastapy._private.system_model.part_model.acoustics._2881 import (
        PartSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2882 import (
        ResultPlaneOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2883 import (
        ResultSphereOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2884 import (
        ResultSurfaceCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2885 import (
        ResultSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2886 import (
        SphericalEnvelopeCentreDefinition,
    )
    from mastapy._private.system_model.part_model.acoustics._2887 import (
        SphericalEnvelopeType,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.acoustics._2866": ["AcousticAnalysisOptions"],
        "_private.system_model.part_model.acoustics._2867": ["AcousticAnalysisSetup"],
        "_private.system_model.part_model.acoustics._2868": [
            "AcousticAnalysisSetupCacheReporting"
        ],
        "_private.system_model.part_model.acoustics._2869": [
            "AcousticAnalysisSetupCollection"
        ],
        "_private.system_model.part_model.acoustics._2870": ["AcousticEnvelopeType"],
        "_private.system_model.part_model.acoustics._2871": [
            "AcousticInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2872": ["CacheMemoryEstimates"],
        "_private.system_model.part_model.acoustics._2873": [
            "FEPartInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2874": [
            "FESurfaceSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2875": ["HoleInFaceGroup"],
        "_private.system_model.part_model.acoustics._2876": ["MeshedResultPlane"],
        "_private.system_model.part_model.acoustics._2877": ["MeshedResultSphere"],
        "_private.system_model.part_model.acoustics._2878": ["MeshedResultSurface"],
        "_private.system_model.part_model.acoustics._2879": ["MeshedResultSurfaceBase"],
        "_private.system_model.part_model.acoustics._2880": ["MicrophoneArrayDesign"],
        "_private.system_model.part_model.acoustics._2881": [
            "PartSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2882": ["ResultPlaneOptions"],
        "_private.system_model.part_model.acoustics._2883": ["ResultSphereOptions"],
        "_private.system_model.part_model.acoustics._2884": ["ResultSurfaceCollection"],
        "_private.system_model.part_model.acoustics._2885": ["ResultSurfaceOptions"],
        "_private.system_model.part_model.acoustics._2886": [
            "SphericalEnvelopeCentreDefinition"
        ],
        "_private.system_model.part_model.acoustics._2887": ["SphericalEnvelopeType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticAnalysisOptions",
    "AcousticAnalysisSetup",
    "AcousticAnalysisSetupCacheReporting",
    "AcousticAnalysisSetupCollection",
    "AcousticEnvelopeType",
    "AcousticInputSurfaceOptions",
    "CacheMemoryEstimates",
    "FEPartInputSurfaceOptions",
    "FESurfaceSelectionForAcousticEnvelope",
    "HoleInFaceGroup",
    "MeshedResultPlane",
    "MeshedResultSphere",
    "MeshedResultSurface",
    "MeshedResultSurfaceBase",
    "MicrophoneArrayDesign",
    "PartSelectionForAcousticEnvelope",
    "ResultPlaneOptions",
    "ResultSphereOptions",
    "ResultSurfaceCollection",
    "ResultSurfaceOptions",
    "SphericalEnvelopeCentreDefinition",
    "SphericalEnvelopeType",
)
