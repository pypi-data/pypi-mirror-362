"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_set_pareto_optimiser._1005 import BarForPareto
    from mastapy._private.gears.gear_set_pareto_optimiser._1006 import (
        CandidateDisplayChoice,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1007 import ChartInfoBase
    from mastapy._private.gears.gear_set_pareto_optimiser._1008 import (
        CylindricalGearSetParetoOptimiser,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1009 import (
        DesignSpaceSearchBase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1010 import (
        DesignSpaceSearchCandidateBase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1011 import (
        FaceGearSetParetoOptimiser,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1012 import GearNameMapper
    from mastapy._private.gears.gear_set_pareto_optimiser._1013 import GearNamePicker
    from mastapy._private.gears.gear_set_pareto_optimiser._1014 import (
        GearSetOptimiserCandidate,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1015 import (
        GearSetParetoOptimiser,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1016 import (
        HypoidGearSetParetoOptimiser,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1017 import (
        InputSliderForPareto,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1018 import LargerOrSmaller
    from mastapy._private.gears.gear_set_pareto_optimiser._1019 import (
        MicroGeometryDesignSpaceSearch,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1020 import (
        MicroGeometryDesignSpaceSearchCandidate,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1021 import (
        MicroGeometryDesignSpaceSearchChartInformation,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1022 import (
        MicroGeometryDesignSpaceSearchStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1023 import (
        MicroGeometryGearSetDesignSpaceSearch,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1024 import (
        MicroGeometryGearSetDesignSpaceSearchStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1025 import (
        MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1026 import (
        OptimisationTarget,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1027 import (
        ParetoConicalRatingOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1028 import (
        ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1029 import (
        ParetoCylindricalGearSetOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1030 import (
        ParetoCylindricalRatingOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1031 import (
        ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1032 import (
        ParetoFaceGearSetOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1033 import (
        ParetoFaceRatingOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1034 import (
        ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1035 import (
        ParetoHypoidGearSetOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1036 import (
        ParetoOptimiserChartInformation,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1037 import (
        ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1038 import (
        ParetoSpiralBevelGearSetOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1039 import (
        ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1040 import (
        ParetoStraightBevelGearSetOptimisationStrategyDatabase,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1041 import (
        ReasonsForInvalidDesigns,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1042 import (
        SpiralBevelGearSetParetoOptimiser,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser._1043 import (
        StraightBevelGearSetParetoOptimiser,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_set_pareto_optimiser._1005": ["BarForPareto"],
        "_private.gears.gear_set_pareto_optimiser._1006": ["CandidateDisplayChoice"],
        "_private.gears.gear_set_pareto_optimiser._1007": ["ChartInfoBase"],
        "_private.gears.gear_set_pareto_optimiser._1008": [
            "CylindricalGearSetParetoOptimiser"
        ],
        "_private.gears.gear_set_pareto_optimiser._1009": ["DesignSpaceSearchBase"],
        "_private.gears.gear_set_pareto_optimiser._1010": [
            "DesignSpaceSearchCandidateBase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1011": [
            "FaceGearSetParetoOptimiser"
        ],
        "_private.gears.gear_set_pareto_optimiser._1012": ["GearNameMapper"],
        "_private.gears.gear_set_pareto_optimiser._1013": ["GearNamePicker"],
        "_private.gears.gear_set_pareto_optimiser._1014": ["GearSetOptimiserCandidate"],
        "_private.gears.gear_set_pareto_optimiser._1015": ["GearSetParetoOptimiser"],
        "_private.gears.gear_set_pareto_optimiser._1016": [
            "HypoidGearSetParetoOptimiser"
        ],
        "_private.gears.gear_set_pareto_optimiser._1017": ["InputSliderForPareto"],
        "_private.gears.gear_set_pareto_optimiser._1018": ["LargerOrSmaller"],
        "_private.gears.gear_set_pareto_optimiser._1019": [
            "MicroGeometryDesignSpaceSearch"
        ],
        "_private.gears.gear_set_pareto_optimiser._1020": [
            "MicroGeometryDesignSpaceSearchCandidate"
        ],
        "_private.gears.gear_set_pareto_optimiser._1021": [
            "MicroGeometryDesignSpaceSearchChartInformation"
        ],
        "_private.gears.gear_set_pareto_optimiser._1022": [
            "MicroGeometryDesignSpaceSearchStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1023": [
            "MicroGeometryGearSetDesignSpaceSearch"
        ],
        "_private.gears.gear_set_pareto_optimiser._1024": [
            "MicroGeometryGearSetDesignSpaceSearchStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1025": [
            "MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1026": ["OptimisationTarget"],
        "_private.gears.gear_set_pareto_optimiser._1027": [
            "ParetoConicalRatingOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1028": [
            "ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1029": [
            "ParetoCylindricalGearSetOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1030": [
            "ParetoCylindricalRatingOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1031": [
            "ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1032": [
            "ParetoFaceGearSetOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1033": [
            "ParetoFaceRatingOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1034": [
            "ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1035": [
            "ParetoHypoidGearSetOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1036": [
            "ParetoOptimiserChartInformation"
        ],
        "_private.gears.gear_set_pareto_optimiser._1037": [
            "ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1038": [
            "ParetoSpiralBevelGearSetOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1039": [
            "ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1040": [
            "ParetoStraightBevelGearSetOptimisationStrategyDatabase"
        ],
        "_private.gears.gear_set_pareto_optimiser._1041": ["ReasonsForInvalidDesigns"],
        "_private.gears.gear_set_pareto_optimiser._1042": [
            "SpiralBevelGearSetParetoOptimiser"
        ],
        "_private.gears.gear_set_pareto_optimiser._1043": [
            "StraightBevelGearSetParetoOptimiser"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BarForPareto",
    "CandidateDisplayChoice",
    "ChartInfoBase",
    "CylindricalGearSetParetoOptimiser",
    "DesignSpaceSearchBase",
    "DesignSpaceSearchCandidateBase",
    "FaceGearSetParetoOptimiser",
    "GearNameMapper",
    "GearNamePicker",
    "GearSetOptimiserCandidate",
    "GearSetParetoOptimiser",
    "HypoidGearSetParetoOptimiser",
    "InputSliderForPareto",
    "LargerOrSmaller",
    "MicroGeometryDesignSpaceSearch",
    "MicroGeometryDesignSpaceSearchCandidate",
    "MicroGeometryDesignSpaceSearchChartInformation",
    "MicroGeometryDesignSpaceSearchStrategyDatabase",
    "MicroGeometryGearSetDesignSpaceSearch",
    "MicroGeometryGearSetDesignSpaceSearchStrategyDatabase",
    "MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase",
    "OptimisationTarget",
    "ParetoConicalRatingOptimisationStrategyDatabase",
    "ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase",
    "ParetoCylindricalGearSetOptimisationStrategyDatabase",
    "ParetoCylindricalRatingOptimisationStrategyDatabase",
    "ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase",
    "ParetoFaceGearSetOptimisationStrategyDatabase",
    "ParetoFaceRatingOptimisationStrategyDatabase",
    "ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase",
    "ParetoHypoidGearSetOptimisationStrategyDatabase",
    "ParetoOptimiserChartInformation",
    "ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase",
    "ParetoSpiralBevelGearSetOptimisationStrategyDatabase",
    "ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase",
    "ParetoStraightBevelGearSetOptimisationStrategyDatabase",
    "ReasonsForInvalidDesigns",
    "SpiralBevelGearSetParetoOptimiser",
    "StraightBevelGearSetParetoOptimiser",
)
