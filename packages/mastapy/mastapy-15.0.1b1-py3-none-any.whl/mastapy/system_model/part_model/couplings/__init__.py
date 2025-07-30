"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.couplings._2815 import BeltDrive
    from mastapy._private.system_model.part_model.couplings._2816 import BeltDriveType
    from mastapy._private.system_model.part_model.couplings._2817 import Clutch
    from mastapy._private.system_model.part_model.couplings._2818 import ClutchHalf
    from mastapy._private.system_model.part_model.couplings._2819 import ClutchType
    from mastapy._private.system_model.part_model.couplings._2820 import ConceptCoupling
    from mastapy._private.system_model.part_model.couplings._2821 import (
        ConceptCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2822 import (
        ConceptCouplingHalfPositioning,
    )
    from mastapy._private.system_model.part_model.couplings._2823 import Coupling
    from mastapy._private.system_model.part_model.couplings._2824 import CouplingHalf
    from mastapy._private.system_model.part_model.couplings._2825 import (
        CrowningSpecification,
    )
    from mastapy._private.system_model.part_model.couplings._2826 import CVT
    from mastapy._private.system_model.part_model.couplings._2827 import CVTPulley
    from mastapy._private.system_model.part_model.couplings._2828 import (
        PartToPartShearCoupling,
    )
    from mastapy._private.system_model.part_model.couplings._2829 import (
        PartToPartShearCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2830 import (
        PitchErrorFlankOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2831 import Pulley
    from mastapy._private.system_model.part_model.couplings._2832 import (
        RigidConnectorSettings,
    )
    from mastapy._private.system_model.part_model.couplings._2833 import (
        RigidConnectorStiffnessType,
    )
    from mastapy._private.system_model.part_model.couplings._2834 import (
        RigidConnectorTiltStiffnessTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2835 import (
        RigidConnectorToothLocation,
    )
    from mastapy._private.system_model.part_model.couplings._2836 import (
        RigidConnectorToothSpacingType,
    )
    from mastapy._private.system_model.part_model.couplings._2837 import (
        RigidConnectorTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2838 import RollingRing
    from mastapy._private.system_model.part_model.couplings._2839 import (
        RollingRingAssembly,
    )
    from mastapy._private.system_model.part_model.couplings._2840 import (
        ShaftHubConnection,
    )
    from mastapy._private.system_model.part_model.couplings._2841 import (
        SplineFitOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2842 import (
        SplineHalfManufacturingError,
    )
    from mastapy._private.system_model.part_model.couplings._2843 import (
        SplineLeadRelief,
    )
    from mastapy._private.system_model.part_model.couplings._2844 import (
        SplinePitchErrorInputType,
    )
    from mastapy._private.system_model.part_model.couplings._2845 import (
        SplinePitchErrorOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2846 import SpringDamper
    from mastapy._private.system_model.part_model.couplings._2847 import (
        SpringDamperHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2848 import Synchroniser
    from mastapy._private.system_model.part_model.couplings._2849 import (
        SynchroniserCone,
    )
    from mastapy._private.system_model.part_model.couplings._2850 import (
        SynchroniserHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2851 import (
        SynchroniserPart,
    )
    from mastapy._private.system_model.part_model.couplings._2852 import (
        SynchroniserSleeve,
    )
    from mastapy._private.system_model.part_model.couplings._2853 import TorqueConverter
    from mastapy._private.system_model.part_model.couplings._2854 import (
        TorqueConverterPump,
    )
    from mastapy._private.system_model.part_model.couplings._2855 import (
        TorqueConverterSpeedRatio,
    )
    from mastapy._private.system_model.part_model.couplings._2856 import (
        TorqueConverterTurbine,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.couplings._2815": ["BeltDrive"],
        "_private.system_model.part_model.couplings._2816": ["BeltDriveType"],
        "_private.system_model.part_model.couplings._2817": ["Clutch"],
        "_private.system_model.part_model.couplings._2818": ["ClutchHalf"],
        "_private.system_model.part_model.couplings._2819": ["ClutchType"],
        "_private.system_model.part_model.couplings._2820": ["ConceptCoupling"],
        "_private.system_model.part_model.couplings._2821": ["ConceptCouplingHalf"],
        "_private.system_model.part_model.couplings._2822": [
            "ConceptCouplingHalfPositioning"
        ],
        "_private.system_model.part_model.couplings._2823": ["Coupling"],
        "_private.system_model.part_model.couplings._2824": ["CouplingHalf"],
        "_private.system_model.part_model.couplings._2825": ["CrowningSpecification"],
        "_private.system_model.part_model.couplings._2826": ["CVT"],
        "_private.system_model.part_model.couplings._2827": ["CVTPulley"],
        "_private.system_model.part_model.couplings._2828": ["PartToPartShearCoupling"],
        "_private.system_model.part_model.couplings._2829": [
            "PartToPartShearCouplingHalf"
        ],
        "_private.system_model.part_model.couplings._2830": ["PitchErrorFlankOptions"],
        "_private.system_model.part_model.couplings._2831": ["Pulley"],
        "_private.system_model.part_model.couplings._2832": ["RigidConnectorSettings"],
        "_private.system_model.part_model.couplings._2833": [
            "RigidConnectorStiffnessType"
        ],
        "_private.system_model.part_model.couplings._2834": [
            "RigidConnectorTiltStiffnessTypes"
        ],
        "_private.system_model.part_model.couplings._2835": [
            "RigidConnectorToothLocation"
        ],
        "_private.system_model.part_model.couplings._2836": [
            "RigidConnectorToothSpacingType"
        ],
        "_private.system_model.part_model.couplings._2837": ["RigidConnectorTypes"],
        "_private.system_model.part_model.couplings._2838": ["RollingRing"],
        "_private.system_model.part_model.couplings._2839": ["RollingRingAssembly"],
        "_private.system_model.part_model.couplings._2840": ["ShaftHubConnection"],
        "_private.system_model.part_model.couplings._2841": ["SplineFitOptions"],
        "_private.system_model.part_model.couplings._2842": [
            "SplineHalfManufacturingError"
        ],
        "_private.system_model.part_model.couplings._2843": ["SplineLeadRelief"],
        "_private.system_model.part_model.couplings._2844": [
            "SplinePitchErrorInputType"
        ],
        "_private.system_model.part_model.couplings._2845": ["SplinePitchErrorOptions"],
        "_private.system_model.part_model.couplings._2846": ["SpringDamper"],
        "_private.system_model.part_model.couplings._2847": ["SpringDamperHalf"],
        "_private.system_model.part_model.couplings._2848": ["Synchroniser"],
        "_private.system_model.part_model.couplings._2849": ["SynchroniserCone"],
        "_private.system_model.part_model.couplings._2850": ["SynchroniserHalf"],
        "_private.system_model.part_model.couplings._2851": ["SynchroniserPart"],
        "_private.system_model.part_model.couplings._2852": ["SynchroniserSleeve"],
        "_private.system_model.part_model.couplings._2853": ["TorqueConverter"],
        "_private.system_model.part_model.couplings._2854": ["TorqueConverterPump"],
        "_private.system_model.part_model.couplings._2855": [
            "TorqueConverterSpeedRatio"
        ],
        "_private.system_model.part_model.couplings._2856": ["TorqueConverterTurbine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeltDrive",
    "BeltDriveType",
    "Clutch",
    "ClutchHalf",
    "ClutchType",
    "ConceptCoupling",
    "ConceptCouplingHalf",
    "ConceptCouplingHalfPositioning",
    "Coupling",
    "CouplingHalf",
    "CrowningSpecification",
    "CVT",
    "CVTPulley",
    "PartToPartShearCoupling",
    "PartToPartShearCouplingHalf",
    "PitchErrorFlankOptions",
    "Pulley",
    "RigidConnectorSettings",
    "RigidConnectorStiffnessType",
    "RigidConnectorTiltStiffnessTypes",
    "RigidConnectorToothLocation",
    "RigidConnectorToothSpacingType",
    "RigidConnectorTypes",
    "RollingRing",
    "RollingRingAssembly",
    "ShaftHubConnection",
    "SplineFitOptions",
    "SplineHalfManufacturingError",
    "SplineLeadRelief",
    "SplinePitchErrorInputType",
    "SplinePitchErrorOptions",
    "SpringDamper",
    "SpringDamperHalf",
    "Synchroniser",
    "SynchroniserCone",
    "SynchroniserHalf",
    "SynchroniserPart",
    "SynchroniserSleeve",
    "TorqueConverter",
    "TorqueConverterPump",
    "TorqueConverterSpeedRatio",
    "TorqueConverterTurbine",
)
