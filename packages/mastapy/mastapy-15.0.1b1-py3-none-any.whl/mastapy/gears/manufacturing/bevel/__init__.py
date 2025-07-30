"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.bevel._875 import AbstractTCA
    from mastapy._private.gears.manufacturing.bevel._876 import (
        BevelMachineSettingOptimizationResult,
    )
    from mastapy._private.gears.manufacturing.bevel._877 import (
        ConicalFlankDeviationsData,
    )
    from mastapy._private.gears.manufacturing.bevel._878 import (
        ConicalGearManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._879 import (
        ConicalGearManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._880 import (
        ConicalGearMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._881 import (
        ConicalGearMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._882 import (
        ConicalMeshedGearManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._883 import (
        ConicalMeshedWheelFlankManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._884 import (
        ConicalMeshFlankManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._885 import (
        ConicalMeshFlankMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._886 import (
        ConicalMeshFlankNURBSMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._887 import (
        ConicalMeshManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._888 import (
        ConicalMeshManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._889 import (
        ConicalMeshMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._890 import (
        ConicalMeshMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._891 import (
        ConicalPinionManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._892 import (
        ConicalPinionMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._893 import (
        ConicalSetManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._894 import (
        ConicalSetManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._895 import (
        ConicalSetMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._896 import (
        ConicalSetMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._897 import (
        ConicalWheelManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._898 import EaseOffBasedTCA
    from mastapy._private.gears.manufacturing.bevel._899 import FlankMeasurementBorder
    from mastapy._private.gears.manufacturing.bevel._900 import HypoidAdvancedLibrary
    from mastapy._private.gears.manufacturing.bevel._901 import MachineTypes
    from mastapy._private.gears.manufacturing.bevel._902 import ManufacturingMachine
    from mastapy._private.gears.manufacturing.bevel._903 import (
        ManufacturingMachineDatabase,
    )
    from mastapy._private.gears.manufacturing.bevel._904 import (
        PinionBevelGeneratingModifiedRollMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._905 import (
        PinionBevelGeneratingTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._906 import PinionConcave
    from mastapy._private.gears.manufacturing.bevel._907 import (
        PinionConicalMachineSettingsSpecified,
    )
    from mastapy._private.gears.manufacturing.bevel._908 import PinionConvex
    from mastapy._private.gears.manufacturing.bevel._909 import (
        PinionFinishMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._910 import (
        PinionHypoidFormateTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._911 import (
        PinionHypoidGeneratingTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._912 import PinionMachineSettingsSMT
    from mastapy._private.gears.manufacturing.bevel._913 import (
        PinionRoughMachineSetting,
    )
    from mastapy._private.gears.manufacturing.bevel._914 import Wheel
    from mastapy._private.gears.manufacturing.bevel._915 import WheelFormatMachineTypes
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.bevel._875": ["AbstractTCA"],
        "_private.gears.manufacturing.bevel._876": [
            "BevelMachineSettingOptimizationResult"
        ],
        "_private.gears.manufacturing.bevel._877": ["ConicalFlankDeviationsData"],
        "_private.gears.manufacturing.bevel._878": ["ConicalGearManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._879": ["ConicalGearManufacturingConfig"],
        "_private.gears.manufacturing.bevel._880": ["ConicalGearMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._881": [
            "ConicalGearMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._882": [
            "ConicalMeshedGearManufacturingAnalysis"
        ],
        "_private.gears.manufacturing.bevel._883": [
            "ConicalMeshedWheelFlankManufacturingConfig"
        ],
        "_private.gears.manufacturing.bevel._884": [
            "ConicalMeshFlankManufacturingConfig"
        ],
        "_private.gears.manufacturing.bevel._885": [
            "ConicalMeshFlankMicroGeometryConfig"
        ],
        "_private.gears.manufacturing.bevel._886": [
            "ConicalMeshFlankNURBSMicroGeometryConfig"
        ],
        "_private.gears.manufacturing.bevel._887": ["ConicalMeshManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._888": ["ConicalMeshManufacturingConfig"],
        "_private.gears.manufacturing.bevel._889": ["ConicalMeshMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._890": [
            "ConicalMeshMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._891": ["ConicalPinionManufacturingConfig"],
        "_private.gears.manufacturing.bevel._892": ["ConicalPinionMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._893": ["ConicalSetManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._894": ["ConicalSetManufacturingConfig"],
        "_private.gears.manufacturing.bevel._895": ["ConicalSetMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._896": [
            "ConicalSetMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._897": ["ConicalWheelManufacturingConfig"],
        "_private.gears.manufacturing.bevel._898": ["EaseOffBasedTCA"],
        "_private.gears.manufacturing.bevel._899": ["FlankMeasurementBorder"],
        "_private.gears.manufacturing.bevel._900": ["HypoidAdvancedLibrary"],
        "_private.gears.manufacturing.bevel._901": ["MachineTypes"],
        "_private.gears.manufacturing.bevel._902": ["ManufacturingMachine"],
        "_private.gears.manufacturing.bevel._903": ["ManufacturingMachineDatabase"],
        "_private.gears.manufacturing.bevel._904": [
            "PinionBevelGeneratingModifiedRollMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._905": [
            "PinionBevelGeneratingTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._906": ["PinionConcave"],
        "_private.gears.manufacturing.bevel._907": [
            "PinionConicalMachineSettingsSpecified"
        ],
        "_private.gears.manufacturing.bevel._908": ["PinionConvex"],
        "_private.gears.manufacturing.bevel._909": ["PinionFinishMachineSettings"],
        "_private.gears.manufacturing.bevel._910": [
            "PinionHypoidFormateTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._911": [
            "PinionHypoidGeneratingTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._912": ["PinionMachineSettingsSMT"],
        "_private.gears.manufacturing.bevel._913": ["PinionRoughMachineSetting"],
        "_private.gears.manufacturing.bevel._914": ["Wheel"],
        "_private.gears.manufacturing.bevel._915": ["WheelFormatMachineTypes"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractTCA",
    "BevelMachineSettingOptimizationResult",
    "ConicalFlankDeviationsData",
    "ConicalGearManufacturingAnalysis",
    "ConicalGearManufacturingConfig",
    "ConicalGearMicroGeometryConfig",
    "ConicalGearMicroGeometryConfigBase",
    "ConicalMeshedGearManufacturingAnalysis",
    "ConicalMeshedWheelFlankManufacturingConfig",
    "ConicalMeshFlankManufacturingConfig",
    "ConicalMeshFlankMicroGeometryConfig",
    "ConicalMeshFlankNURBSMicroGeometryConfig",
    "ConicalMeshManufacturingAnalysis",
    "ConicalMeshManufacturingConfig",
    "ConicalMeshMicroGeometryConfig",
    "ConicalMeshMicroGeometryConfigBase",
    "ConicalPinionManufacturingConfig",
    "ConicalPinionMicroGeometryConfig",
    "ConicalSetManufacturingAnalysis",
    "ConicalSetManufacturingConfig",
    "ConicalSetMicroGeometryConfig",
    "ConicalSetMicroGeometryConfigBase",
    "ConicalWheelManufacturingConfig",
    "EaseOffBasedTCA",
    "FlankMeasurementBorder",
    "HypoidAdvancedLibrary",
    "MachineTypes",
    "ManufacturingMachine",
    "ManufacturingMachineDatabase",
    "PinionBevelGeneratingModifiedRollMachineSettings",
    "PinionBevelGeneratingTiltMachineSettings",
    "PinionConcave",
    "PinionConicalMachineSettingsSpecified",
    "PinionConvex",
    "PinionFinishMachineSettings",
    "PinionHypoidFormateTiltMachineSettings",
    "PinionHypoidGeneratingTiltMachineSettings",
    "PinionMachineSettingsSMT",
    "PinionRoughMachineSetting",
    "Wheel",
    "WheelFormatMachineTypes",
)
