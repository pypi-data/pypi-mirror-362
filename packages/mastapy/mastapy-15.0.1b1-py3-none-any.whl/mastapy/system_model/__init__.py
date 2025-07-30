"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model._2411 import Design
    from mastapy._private.system_model._2412 import ComponentDampingOption
    from mastapy._private.system_model._2413 import (
        ConceptCouplingSpeedRatioSpecificationMethod,
    )
    from mastapy._private.system_model._2414 import DesignEntity
    from mastapy._private.system_model._2415 import DesignEntityId
    from mastapy._private.system_model._2416 import DesignSettings
    from mastapy._private.system_model._2417 import DutyCycleImporter
    from mastapy._private.system_model._2418 import DutyCycleImporterDesignEntityMatch
    from mastapy._private.system_model._2419 import ExternalFullFELoader
    from mastapy._private.system_model._2420 import HypoidWindUpRemovalMethod
    from mastapy._private.system_model._2421 import IncludeDutyCycleOption
    from mastapy._private.system_model._2422 import MAAElectricMachineGroup
    from mastapy._private.system_model._2423 import MASTASettings
    from mastapy._private.system_model._2424 import MemorySummary
    from mastapy._private.system_model._2425 import MeshStiffnessModel
    from mastapy._private.system_model._2426 import (
        PlanetPinManufacturingErrorsCoordinateSystem,
    )
    from mastapy._private.system_model._2427 import (
        PowerLoadDragTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2428 import (
        PowerLoadInputTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2429 import PowerLoadPIDControlSpeedInputType
    from mastapy._private.system_model._2430 import PowerLoadType
    from mastapy._private.system_model._2431 import RelativeComponentAlignment
    from mastapy._private.system_model._2432 import RelativeOffsetOption
    from mastapy._private.system_model._2433 import SystemReporting
    from mastapy._private.system_model._2434 import (
        ThermalExpansionOptionForGroundedNodes,
    )
    from mastapy._private.system_model._2435 import TransmissionTemperatureSet
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model._2411": ["Design"],
        "_private.system_model._2412": ["ComponentDampingOption"],
        "_private.system_model._2413": ["ConceptCouplingSpeedRatioSpecificationMethod"],
        "_private.system_model._2414": ["DesignEntity"],
        "_private.system_model._2415": ["DesignEntityId"],
        "_private.system_model._2416": ["DesignSettings"],
        "_private.system_model._2417": ["DutyCycleImporter"],
        "_private.system_model._2418": ["DutyCycleImporterDesignEntityMatch"],
        "_private.system_model._2419": ["ExternalFullFELoader"],
        "_private.system_model._2420": ["HypoidWindUpRemovalMethod"],
        "_private.system_model._2421": ["IncludeDutyCycleOption"],
        "_private.system_model._2422": ["MAAElectricMachineGroup"],
        "_private.system_model._2423": ["MASTASettings"],
        "_private.system_model._2424": ["MemorySummary"],
        "_private.system_model._2425": ["MeshStiffnessModel"],
        "_private.system_model._2426": ["PlanetPinManufacturingErrorsCoordinateSystem"],
        "_private.system_model._2427": ["PowerLoadDragTorqueSpecificationMethod"],
        "_private.system_model._2428": ["PowerLoadInputTorqueSpecificationMethod"],
        "_private.system_model._2429": ["PowerLoadPIDControlSpeedInputType"],
        "_private.system_model._2430": ["PowerLoadType"],
        "_private.system_model._2431": ["RelativeComponentAlignment"],
        "_private.system_model._2432": ["RelativeOffsetOption"],
        "_private.system_model._2433": ["SystemReporting"],
        "_private.system_model._2434": ["ThermalExpansionOptionForGroundedNodes"],
        "_private.system_model._2435": ["TransmissionTemperatureSet"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Design",
    "ComponentDampingOption",
    "ConceptCouplingSpeedRatioSpecificationMethod",
    "DesignEntity",
    "DesignEntityId",
    "DesignSettings",
    "DutyCycleImporter",
    "DutyCycleImporterDesignEntityMatch",
    "ExternalFullFELoader",
    "HypoidWindUpRemovalMethod",
    "IncludeDutyCycleOption",
    "MAAElectricMachineGroup",
    "MASTASettings",
    "MemorySummary",
    "MeshStiffnessModel",
    "PlanetPinManufacturingErrorsCoordinateSystem",
    "PowerLoadDragTorqueSpecificationMethod",
    "PowerLoadInputTorqueSpecificationMethod",
    "PowerLoadPIDControlSpeedInputType",
    "PowerLoadType",
    "RelativeComponentAlignment",
    "RelativeOffsetOption",
    "SystemReporting",
    "ThermalExpansionOptionForGroundedNodes",
    "TransmissionTemperatureSet",
)
