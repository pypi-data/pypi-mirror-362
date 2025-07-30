"""ParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7877

_CLUTCH_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "ClutchConnection"
)
_CONCEPT_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "ConceptCouplingConnection",
)
_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "CouplingConnection"
)
_SPRING_DAMPER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "SpringDamperConnection"
)
_TORQUE_CONVERTER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "TorqueConverterConnection",
)
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "PartToPartShearCouplingConnection",
)
_CLUTCH_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ClutchConnectionLoadCase",
)
_CONCEPT_COUPLING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ConceptCouplingConnectionLoadCase",
)
_COUPLING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CouplingConnectionLoadCase",
)
_SPRING_DAMPER_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpringDamperConnectionLoadCase",
)
_TORQUE_CONVERTER_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "TorqueConverterConnectionLoadCase",
)
_STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelGearSetLoadCase",
)
_STRAIGHT_BEVEL_PLANET_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelPlanetGearLoadCase",
)
_STRAIGHT_BEVEL_SUN_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelSunGearLoadCase",
)
_WORM_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "WormGearLoadCase"
)
_WORM_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "WormGearSetLoadCase"
)
_ZEROL_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ZerolBevelGearLoadCase"
)
_ZEROL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ZerolBevelGearSetLoadCase",
)
_CYCLOIDAL_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CycloidalAssemblyLoadCase",
)
_CYCLOIDAL_DISC_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CycloidalDiscLoadCase"
)
_RING_PINS_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "RingPinsLoadCase"
)
_PART_TO_PART_SHEAR_COUPLING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PartToPartShearCouplingLoadCase",
)
_PART_TO_PART_SHEAR_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PartToPartShearCouplingHalfLoadCase",
)
_BELT_DRIVE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BeltDriveLoadCase"
)
_CLUTCH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ClutchLoadCase"
)
_CLUTCH_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ClutchHalfLoadCase"
)
_CONCEPT_COUPLING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptCouplingLoadCase"
)
_CONCEPT_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ConceptCouplingHalfLoadCase",
)
_COUPLING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CouplingLoadCase"
)
_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CouplingHalfLoadCase"
)
_CVT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CVTLoadCase"
)
_CVT_PULLEY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CVTPulleyLoadCase"
)
_PULLEY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PulleyLoadCase"
)
_SHAFT_HUB_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ShaftHubConnectionLoadCase",
)
_ROLLING_RING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "RollingRingLoadCase"
)
_ROLLING_RING_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "RollingRingAssemblyLoadCase",
)
_SPRING_DAMPER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SpringDamperLoadCase"
)
_SPRING_DAMPER_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpringDamperHalfLoadCase",
)
_SYNCHRONISER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SynchroniserLoadCase"
)
_SYNCHRONISER_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SynchroniserHalfLoadCase",
)
_SYNCHRONISER_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SynchroniserPartLoadCase",
)
_SYNCHRONISER_SLEEVE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SynchroniserSleeveLoadCase",
)
_TORQUE_CONVERTER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "TorqueConverterLoadCase"
)
_TORQUE_CONVERTER_PUMP_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "TorqueConverterPumpLoadCase",
)
_TORQUE_CONVERTER_TURBINE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "TorqueConverterTurbineLoadCase",
)
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ShaftToMountableComponentConnectionLoadCase",
)
_CVT_BELT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CVTBeltConnectionLoadCase",
)
_BELT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BeltConnectionLoadCase"
)
_COAXIAL_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CoaxialConnectionLoadCase",
)
_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConnectionLoadCase"
)
_INTER_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "InterMountableComponentConnectionLoadCase",
)
_PLANETARY_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PlanetaryConnectionLoadCase",
)
_ROLLING_RING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "RollingRingConnectionLoadCase",
)
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractShaftToMountableComponentConnectionLoadCase",
)
_BEVEL_DIFFERENTIAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialGearMeshLoadCase",
)
_CONCEPT_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptGearMeshLoadCase"
)
_FACE_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FaceGearMeshLoadCase"
)
_STRAIGHT_BEVEL_DIFF_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelDiffGearMeshLoadCase",
)
_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearMeshLoadCase"
)
_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConicalGearMeshLoadCase"
)
_AGMA_GLEASON_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AGMAGleasonConicalGearMeshLoadCase",
)
_CYLINDRICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalGearMeshLoadCase",
)
_HYPOID_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "HypoidGearMeshLoadCase"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearMeshLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidHypoidGearMeshLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase",
)
_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpiralBevelGearMeshLoadCase",
)
_STRAIGHT_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelGearMeshLoadCase",
)
_WORM_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "WormGearMeshLoadCase"
)
_ZEROL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ZerolBevelGearMeshLoadCase",
)
_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearMeshLoadCase"
)
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CycloidalDiscCentralBearingConnectionLoadCase",
)
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CycloidalDiscPlanetaryBearingConnectionLoadCase",
)
_RING_PINS_TO_DISC_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "RingPinsToDiscConnectionLoadCase",
)
_PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PartToPartShearCouplingConnectionLoadCase",
)
_ABSTRACT_SHAFT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "AbstractShaftLoadCase"
)
_MICROPHONE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "MicrophoneLoadCase"
)
_MICROPHONE_ARRAY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "MicrophoneArrayLoadCase"
)
_ABSTRACT_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractAssemblyLoadCase",
)
_ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractShaftOrHousingLoadCase",
)
_BEARING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BearingLoadCase"
)
_BOLT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BoltLoadCase"
)
_BOLTED_JOINT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BoltedJointLoadCase"
)
_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ComponentLoadCase"
)
_CONNECTOR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConnectorLoadCase"
)
_DATUM_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "DatumLoadCase"
)
_EXTERNAL_CAD_MODEL_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ExternalCADModelLoadCase",
)
_FE_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FEPartLoadCase"
)
_FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "FlexiblePinAssemblyLoadCase",
)
_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "AssemblyLoadCase"
)
_GUIDE_DXF_MODEL_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GuideDxfModelLoadCase"
)
_MASS_DISC_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "MassDiscLoadCase"
)
_MEASUREMENT_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "MeasurementComponentLoadCase",
)
_MOUNTABLE_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "MountableComponentLoadCase",
)
_OIL_SEAL_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "OilSealLoadCase"
)
_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PartLoadCase"
)
_PLANET_CARRIER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PlanetCarrierLoadCase"
)
_POINT_LOAD_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PointLoadLoadCase"
)
_POWER_LOAD_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PowerLoadLoadCase"
)
_ROOT_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "RootAssemblyLoadCase"
)
_SPECIALISED_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpecialisedAssemblyLoadCase",
)
_UNBALANCED_MASS_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "UnbalancedMassLoadCase"
)
_VIRTUAL_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "VirtualComponentLoadCase",
)
_SHAFT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ShaftLoadCase"
)
_CONCEPT_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptGearLoadCase"
)
_CONCEPT_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConceptGearSetLoadCase"
)
_FACE_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FaceGearLoadCase"
)
_FACE_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FaceGearSetLoadCase"
)
_AGMA_GLEASON_CONICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AGMAGleasonConicalGearLoadCase",
)
_AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AGMAGleasonConicalGearSetLoadCase",
)
_BEVEL_DIFFERENTIAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialGearLoadCase",
)
_BEVEL_DIFFERENTIAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialGearSetLoadCase",
)
_BEVEL_DIFFERENTIAL_PLANET_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialPlanetGearLoadCase",
)
_BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialSunGearLoadCase",
)
_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearLoadCase"
)
_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearSetLoadCase"
)
_CONICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConicalGearLoadCase"
)
_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConicalGearSetLoadCase"
)
_CYLINDRICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CylindricalGearLoadCase"
)
_CYLINDRICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalGearSetLoadCase",
)
_CYLINDRICAL_PLANET_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalPlanetGearLoadCase",
)
_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearLoadCase"
)
_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearSetLoadCase"
)
_HYPOID_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "HypoidGearLoadCase"
)
_HYPOID_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "HypoidGearSetLoadCase"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearSetLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidHypoidGearLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidHypoidGearSetLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidSpiralBevelGearLoadCase",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase",
)
_PLANETARY_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PlanetaryGearSetLoadCase",
)
_SPIRAL_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SpiralBevelGearLoadCase"
)
_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpiralBevelGearSetLoadCase",
)
_STRAIGHT_BEVEL_DIFF_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelDiffGearLoadCase",
)
_STRAIGHT_BEVEL_DIFF_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelDiffGearSetLoadCase",
)
_STRAIGHT_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelGearLoadCase",
)
_STRAIGHT_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGearSet"
)
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelPlanetGear"
)
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelSunGear"
)
_WORM_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGear")
_WORM_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGearSet"
)
_ZEROL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGear"
)
_ZEROL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGearSet"
)
_CONCEPT_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGear"
)
_CONCEPT_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGearSet"
)
_FACE_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGear")
_FACE_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGearSet"
)
_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
)
_BEVEL_DIFFERENTIAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGear"
)
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGearSet"
)
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialPlanetGear"
)
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialSunGear"
)
_BEVEL_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGear")
_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
)
_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
)
_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
)
_CYLINDRICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGear"
)
_CYLINDRICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGearSet"
)
_CYLINDRICAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalPlanetGear"
)
_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear")
_GEAR_SET = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSet")
_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGear"
)
_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGear"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGear"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGear",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearSet",
)
_PLANETARY_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "PlanetaryGearSet"
)
_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGear"
)
_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGearSet"
)
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGear"
)
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGearSet"
)
_STRAIGHT_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGear"
)
_CYCLOIDAL_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalAssembly"
)
_CYCLOIDAL_DISC = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalDisc"
)
_RING_PINS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "RingPins"
)
_PART_TO_PART_SHEAR_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
)
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCouplingHalf"
)
_BELT_DRIVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDrive"
)
_CLUTCH = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Clutch")
_CLUTCH_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ClutchHalf"
)
_CONCEPT_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCoupling"
)
_CONCEPT_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCouplingHalf"
)
_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Coupling"
)
_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
)
_CVT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVT")
_CVT_PULLEY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVTPulley"
)
_PULLEY = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Pulley")
_SHAFT_HUB_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ShaftHubConnection"
)
_ROLLING_RING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRing"
)
_ROLLING_RING_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRingAssembly"
)
_SPRING_DAMPER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
)
_SPRING_DAMPER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamperHalf"
)
_SYNCHRONISER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Synchroniser"
)
_SYNCHRONISER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserHalf"
)
_SYNCHRONISER_PART = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserPart"
)
_SYNCHRONISER_SLEEVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserSleeve"
)
_TORQUE_CONVERTER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverter"
)
_TORQUE_CONVERTER_PUMP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterPump"
)
_TORQUE_CONVERTER_TURBINE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterTurbine"
)
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "ShaftToMountableComponentConnection",
)
_CVT_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CVTBeltConnection"
)
_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "BeltConnection"
)
_COAXIAL_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CoaxialConnection"
)
_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Connection"
)
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "InterMountableComponentConnection",
)
_PLANETARY_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "PlanetaryConnection"
)
_ROLLING_RING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "RollingRingConnection"
)
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "AbstractShaftToMountableComponentConnection",
)
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelDifferentialGearMesh"
)
_CONCEPT_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConceptGearMesh"
)
_FACE_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "FaceGearMesh"
)
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelDiffGearMesh"
)
_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelGearMesh"
)
_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConicalGearMesh"
)
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "AGMAGleasonConicalGearMesh"
)
_CYLINDRICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "CylindricalGearMesh"
)
_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "HypoidGearMesh"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidConicalGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidHypoidGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearMesh",
)
_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "SpiralBevelGearMesh"
)
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelGearMesh"
)
_WORM_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "WormGearMesh"
)
_ZEROL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ZerolBevelGearMesh"
)
_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "GearMesh"
)
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscCentralBearingConnection",
)
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscPlanetaryBearingConnection",
)
_RING_PINS_TO_DISC_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "RingPinsToDiscConnection",
)
_ABSTRACT_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaft"
)
_MICROPHONE = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Microphone")
_MICROPHONE_ARRAY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MicrophoneArray"
)
_ABSTRACT_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractAssembly"
)
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaftOrHousing"
)
_BEARING = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bearing")
_BOLT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bolt")
_BOLTED_JOINT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "BoltedJoint")
_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_CONNECTOR = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Connector")
_DATUM = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Datum")
_EXTERNAL_CAD_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "ExternalCADModel"
)
_FE_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "FEPart")
_FLEXIBLE_PIN_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "FlexiblePinAssembly"
)
_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Assembly")
_GUIDE_DXF_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "GuideDxfModel"
)
_MASS_DISC = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "MassDisc")
_MEASUREMENT_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MeasurementComponent"
)
_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)
_OIL_SEAL = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "OilSeal")
_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
_PLANET_CARRIER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "PlanetCarrier"
)
_POINT_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PointLoad")
_POWER_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PowerLoad")
_ROOT_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "RootAssembly")
_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)
_UNBALANCED_MASS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "UnbalancedMass"
)
_VIRTUAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
)
_SHAFT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.ShaftModel", "Shaft")
_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2891
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4561,
        _4562,
        _4563,
        _4564,
        _4565,
        _4566,
        _4567,
        _4568,
        _4569,
        _4570,
        _4571,
        _4572,
        _4573,
        _4574,
        _4575,
        _4576,
        _4577,
        _4578,
        _4579,
        _4580,
        _4581,
        _4582,
        _4583,
        _4584,
        _4585,
        _4586,
        _4587,
        _4588,
        _4589,
        _4590,
        _4591,
        _4592,
        _4593,
        _4594,
        _4595,
        _4596,
        _4597,
        _4598,
        _4599,
        _4600,
        _4601,
        _4602,
        _4603,
        _4604,
        _4605,
        _4606,
        _4607,
        _4608,
        _4609,
        _4610,
        _4611,
        _4612,
        _4620,
        _4621,
        _4622,
        _4623,
        _4624,
        _4625,
        _4626,
        _4627,
        _4628,
        _4629,
        _4630,
        _4631,
        _4632,
        _4633,
        _4634,
        _4635,
        _4636,
        _4637,
        _4638,
        _4639,
        _4640,
        _4641,
        _4642,
        _4643,
        _4644,
        _4645,
        _4646,
        _4648,
        _4649,
        _4656,
        _4661,
        _4662,
        _4663,
        _4664,
        _4665,
        _4666,
        _4667,
        _4668,
        _4669,
        _4670,
        _4671,
        _4672,
        _4673,
        _4674,
        _4675,
        _4676,
        _4677,
        _4678,
        _4679,
        _4680,
        _4681,
        _4682,
        _4683,
        _4684,
        _4685,
        _4686,
        _4687,
        _4688,
        _4689,
        _4690,
        _4691,
        _4692,
        _4693,
        _4694,
        _4695,
        _4696,
        _4697,
        _4698,
        _4699,
        _4700,
        _4701,
        _4702,
        _4703,
        _4704,
        _4705,
        _4706,
        _4707,
        _4708,
        _4709,
        _4710,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7674,
        _7675,
        _7676,
        _7677,
        _7678,
        _7682,
        _7683,
        _7684,
        _7687,
        _7688,
        _7689,
        _7690,
        _7691,
        _7692,
        _7693,
        _7694,
        _7695,
        _7696,
        _7697,
        _7698,
        _7699,
        _7700,
        _7701,
        _7702,
        _7703,
        _7705,
        _7706,
        _7707,
        _7708,
        _7709,
        _7710,
        _7711,
        _7712,
        _7713,
        _7715,
        _7717,
        _7718,
        _7719,
        _7720,
        _7721,
        _7722,
        _7723,
        _7724,
        _7725,
        _7726,
        _7727,
        _7728,
        _7729,
        _7730,
        _7732,
        _7734,
        _7735,
        _7738,
        _7752,
        _7753,
        _7754,
        _7755,
        _7756,
        _7757,
        _7759,
        _7761,
        _7764,
        _7765,
        _7774,
        _7775,
        _7776,
        _7780,
        _7781,
        _7782,
        _7783,
        _7784,
        _7785,
        _7786,
        _7787,
        _7788,
        _7789,
        _7790,
        _7791,
        _7793,
        _7794,
        _7795,
        _7797,
        _7799,
        _7800,
        _7801,
        _7802,
        _7803,
        _7804,
        _7806,
        _7809,
        _7810,
        _7811,
        _7814,
        _7815,
        _7816,
        _7817,
        _7818,
        _7819,
        _7820,
        _7821,
        _7822,
        _7823,
        _7824,
        _7825,
        _7826,
        _7827,
        _7828,
        _7829,
        _7830,
        _7831,
        _7832,
        _7833,
        _7834,
        _7835,
        _7836,
        _7837,
        _7838,
        _7839,
        _7840,
        _7841,
        _7843,
        _7844,
        _7845,
        _7846,
        _7847,
        _7852,
        _7853,
        _7854,
        _7855,
        _7856,
        _7857,
        _7858,
        _7859,
    )
    from mastapy._private.system_model.connections_and_sockets import (
        _2486,
        _2489,
        _2490,
        _2493,
        _2494,
        _2502,
        _2508,
        _2513,
        _2516,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2563,
        _2565,
        _2567,
        _2569,
        _2571,
        _2573,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2556,
        _2559,
        _2562,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2520,
        _2522,
        _2524,
        _2526,
        _2528,
        _2530,
        _2532,
        _2534,
        _2536,
        _2539,
        _2540,
        _2541,
        _2544,
        _2546,
        _2548,
        _2550,
        _2552,
    )
    from mastapy._private.system_model.part_model import (
        _2658,
        _2659,
        _2660,
        _2661,
        _2664,
        _2667,
        _2668,
        _2670,
        _2673,
        _2674,
        _2679,
        _2680,
        _2681,
        _2682,
        _2689,
        _2690,
        _2691,
        _2692,
        _2693,
        _2695,
        _2698,
        _2700,
        _2702,
        _2703,
        _2706,
        _2708,
        _2709,
        _2711,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2815,
        _2817,
        _2818,
        _2820,
        _2821,
        _2823,
        _2824,
        _2826,
        _2827,
        _2828,
        _2829,
        _2831,
        _2838,
        _2839,
        _2840,
        _2846,
        _2847,
        _2848,
        _2850,
        _2851,
        _2852,
        _2853,
        _2854,
        _2856,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2806, _2807, _2808
    from mastapy._private.system_model.part_model.gears import (
        _2750,
        _2751,
        _2752,
        _2753,
        _2754,
        _2755,
        _2756,
        _2757,
        _2758,
        _2759,
        _2760,
        _2761,
        _2762,
        _2763,
        _2764,
        _2765,
        _2766,
        _2767,
        _2769,
        _2771,
        _2772,
        _2773,
        _2774,
        _2775,
        _2776,
        _2777,
        _2778,
        _2779,
        _2781,
        _2782,
        _2783,
        _2784,
        _2785,
        _2786,
        _2787,
        _2788,
        _2789,
        _2790,
        _2791,
        _2792,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2714

    Self = TypeVar("Self", bound="ParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf", bound="ParametricStudyTool._Cast_ParametricStudyTool"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParametricStudyTool:
    """Special nested class for casting ParametricStudyTool to subclasses."""

    __parent__: "ParametricStudyTool"

    @property
    def analysis_case(self: "CastSelf") -> "_7877.AnalysisCase":
        return self.__parent__._cast(_7877.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2891.Context":
        from mastapy._private.system_model.analyses_and_results import _2891

        return self.__parent__._cast(_2891.Context)

    @property
    def parametric_study_tool(self: "CastSelf") -> "ParametricStudyTool":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class ParametricStudyTool(_7877.AnalysisCase):
    """ParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def load_case(self: "Self") -> "_7674.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def parametric_analysis_options(self: "Self") -> "_4656.ParametricStudyToolOptions":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyToolOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParametricAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def time_series_load_case(self: "Self") -> "_7843.TimeSeriesLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TimeSeriesLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeSeriesLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch_connection(
        self: "Self", design_entity: "_2563.ClutchConnection"
    ) -> "_4582.ClutchConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch_connection_load_case(
        self: "Self", design_entity_analysis: "_7701.ClutchConnectionLoadCase"
    ) -> "_4582.ClutchConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling_connection(
        self: "Self", design_entity: "_2565.ConceptCouplingConnection"
    ) -> "_4587.ConceptCouplingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling_connection_load_case(
        self: "Self", design_entity_analysis: "_7707.ConceptCouplingConnectionLoadCase"
    ) -> "_4587.ConceptCouplingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling_connection(
        self: "Self", design_entity: "_2567.CouplingConnection"
    ) -> "_4598.CouplingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling_connection_load_case(
        self: "Self", design_entity_analysis: "_7720.CouplingConnectionLoadCase"
    ) -> "_4598.CouplingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper_connection(
        self: "Self", design_entity: "_2571.SpringDamperConnection"
    ) -> "_4684.SpringDamperConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper_connection_load_case(
        self: "Self", design_entity_analysis: "_7827.SpringDamperConnectionLoadCase"
    ) -> "_4684.SpringDamperConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_connection(
        self: "Self", design_entity: "_2573.TorqueConverterConnection"
    ) -> "_4699.TorqueConverterConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_connection_load_case(
        self: "Self", design_entity_analysis: "_7844.TorqueConverterConnectionLoadCase"
    ) -> "_4699.TorqueConverterConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear_set(
        self: "Self", design_entity: "_2786.StraightBevelGearSet"
    ) -> "_4692.StraightBevelGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7835.StraightBevelGearSetLoadCase"
    ) -> "_4692.StraightBevelGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_planet_gear(
        self: "Self", design_entity: "_2787.StraightBevelPlanetGear"
    ) -> "_4693.StraightBevelPlanetGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelPlanetGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_planet_gear_load_case(
        self: "Self", design_entity_analysis: "_7836.StraightBevelPlanetGearLoadCase"
    ) -> "_4693.StraightBevelPlanetGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelPlanetGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_PLANET_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_sun_gear(
        self: "Self", design_entity: "_2788.StraightBevelSunGear"
    ) -> "_4694.StraightBevelSunGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelSunGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_SUN_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_sun_gear_load_case(
        self: "Self", design_entity_analysis: "_7837.StraightBevelSunGearLoadCase"
    ) -> "_4694.StraightBevelSunGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelSunGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_SUN_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear(
        self: "Self", design_entity: "_2789.WormGear"
    ) -> "_4706.WormGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear_load_case(
        self: "Self", design_entity_analysis: "_7854.WormGearLoadCase"
    ) -> "_4706.WormGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear_set(
        self: "Self", design_entity: "_2790.WormGearSet"
    ) -> "_4707.WormGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7856.WormGearSetLoadCase"
    ) -> "_4707.WormGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear(
        self: "Self", design_entity: "_2791.ZerolBevelGear"
    ) -> "_4709.ZerolBevelGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_7857.ZerolBevelGearLoadCase"
    ) -> "_4709.ZerolBevelGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear_set(
        self: "Self", design_entity: "_2792.ZerolBevelGearSet"
    ) -> "_4710.ZerolBevelGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7859.ZerolBevelGearSetLoadCase"
    ) -> "_4710.ZerolBevelGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_assembly(
        self: "Self", design_entity: "_2806.CycloidalAssembly"
    ) -> "_4604.CycloidalAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalAssemblyParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_assembly_load_case(
        self: "Self", design_entity_analysis: "_7726.CycloidalAssemblyLoadCase"
    ) -> "_4604.CycloidalAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalAssemblyParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc(
        self: "Self", design_entity: "_2807.CycloidalDisc"
    ) -> "_4606.CycloidalDiscParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalDiscParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc_load_case(
        self: "Self", design_entity_analysis: "_7728.CycloidalDiscLoadCase"
    ) -> "_4606.CycloidalDiscParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalDiscParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_ring_pins(
        self: "Self", design_entity: "_2808.RingPins"
    ) -> "_4671.RingPinsParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RingPinsParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_ring_pins_load_case(
        self: "Self", design_entity_analysis: "_7814.RingPinsLoadCase"
    ) -> "_4671.RingPinsParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RingPinsParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RingPinsLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling(
        self: "Self", design_entity: "_2828.PartToPartShearCoupling"
    ) -> "_4664.PartToPartShearCouplingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_load_case(
        self: "Self", design_entity_analysis: "_7802.PartToPartShearCouplingLoadCase"
    ) -> "_4664.PartToPartShearCouplingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_half(
        self: "Self", design_entity: "_2829.PartToPartShearCouplingHalf"
    ) -> "_4663.PartToPartShearCouplingHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingHalfParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_half_load_case(
        self: "Self",
        design_entity_analysis: "_7801.PartToPartShearCouplingHalfLoadCase",
    ) -> "_4663.PartToPartShearCouplingHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingHalfParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_belt_drive(
        self: "Self", design_entity: "_2815.BeltDrive"
    ) -> "_4571.BeltDriveParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BeltDriveParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_DRIVE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_belt_drive_load_case(
        self: "Self", design_entity_analysis: "_7690.BeltDriveLoadCase"
    ) -> "_4571.BeltDriveParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BeltDriveParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_DRIVE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch(
        self: "Self", design_entity: "_2817.Clutch"
    ) -> "_4584.ClutchParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch_load_case(
        self: "Self", design_entity_analysis: "_7703.ClutchLoadCase"
    ) -> "_4584.ClutchParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch_half(
        self: "Self", design_entity: "_2818.ClutchHalf"
    ) -> "_4583.ClutchHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchHalfParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_clutch_half_load_case(
        self: "Self", design_entity_analysis: "_7702.ClutchHalfLoadCase"
    ) -> "_4583.ClutchHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchHalfParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CLUTCH_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling(
        self: "Self", design_entity: "_2820.ConceptCoupling"
    ) -> "_4589.ConceptCouplingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling_load_case(
        self: "Self", design_entity_analysis: "_7709.ConceptCouplingLoadCase"
    ) -> "_4589.ConceptCouplingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling_half(
        self: "Self", design_entity: "_2821.ConceptCouplingHalf"
    ) -> "_4588.ConceptCouplingHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingHalfParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_coupling_half_load_case(
        self: "Self", design_entity_analysis: "_7708.ConceptCouplingHalfLoadCase"
    ) -> "_4588.ConceptCouplingHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingHalfParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_COUPLING_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling(
        self: "Self", design_entity: "_2823.Coupling"
    ) -> "_4600.CouplingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling_load_case(
        self: "Self", design_entity_analysis: "_7722.CouplingLoadCase"
    ) -> "_4600.CouplingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling_half(
        self: "Self", design_entity: "_2824.CouplingHalf"
    ) -> "_4599.CouplingHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingHalfParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_coupling_half_load_case(
        self: "Self", design_entity_analysis: "_7721.CouplingHalfLoadCase"
    ) -> "_4599.CouplingHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingHalfParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COUPLING_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt(
        self: "Self", design_entity: "_2826.CVT"
    ) -> "_4602.CVTParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CVTParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt_load_case(
        self: "Self", design_entity_analysis: "_7724.CVTLoadCase"
    ) -> "_4602.CVTParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CVTParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt_pulley(
        self: "Self", design_entity: "_2827.CVTPulley"
    ) -> "_4603.CVTPulleyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CVTPulleyParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_PULLEY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt_pulley_load_case(
        self: "Self", design_entity_analysis: "_7725.CVTPulleyLoadCase"
    ) -> "_4603.CVTPulleyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CVTPulleyParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_PULLEY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_pulley(
        self: "Self", design_entity: "_2831.Pulley"
    ) -> "_4670.PulleyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PulleyParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PULLEY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_pulley_load_case(
        self: "Self", design_entity_analysis: "_7811.PulleyLoadCase"
    ) -> "_4670.PulleyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PulleyParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PULLEY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft_hub_connection(
        self: "Self", design_entity: "_2840.ShaftHubConnection"
    ) -> "_4677.ShaftHubConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftHubConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_HUB_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft_hub_connection_load_case(
        self: "Self", design_entity_analysis: "_7820.ShaftHubConnectionLoadCase"
    ) -> "_4677.ShaftHubConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftHubConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_HUB_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring(
        self: "Self", design_entity: "_2838.RollingRing"
    ) -> "_4675.RollingRingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring_load_case(
        self: "Self", design_entity_analysis: "_7818.RollingRingLoadCase"
    ) -> "_4675.RollingRingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring_assembly(
        self: "Self", design_entity: "_2839.RollingRingAssembly"
    ) -> "_4673.RollingRingAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingAssemblyParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring_assembly_load_case(
        self: "Self", design_entity_analysis: "_7816.RollingRingAssemblyLoadCase"
    ) -> "_4673.RollingRingAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingAssemblyParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper(
        self: "Self", design_entity: "_2846.SpringDamper"
    ) -> "_4686.SpringDamperParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper_load_case(
        self: "Self", design_entity_analysis: "_7829.SpringDamperLoadCase"
    ) -> "_4686.SpringDamperParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper_half(
        self: "Self", design_entity: "_2847.SpringDamperHalf"
    ) -> "_4685.SpringDamperHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperHalfParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spring_damper_half_load_case(
        self: "Self", design_entity_analysis: "_7828.SpringDamperHalfLoadCase"
    ) -> "_4685.SpringDamperHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperHalfParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPRING_DAMPER_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser(
        self: "Self", design_entity: "_2848.Synchroniser"
    ) -> "_4696.SynchroniserParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_load_case(
        self: "Self", design_entity_analysis: "_7839.SynchroniserLoadCase"
    ) -> "_4696.SynchroniserParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_half(
        self: "Self", design_entity: "_2850.SynchroniserHalf"
    ) -> "_4695.SynchroniserHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserHalfParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_HALF],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_half_load_case(
        self: "Self", design_entity_analysis: "_7838.SynchroniserHalfLoadCase"
    ) -> "_4695.SynchroniserHalfParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserHalfParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_HALF_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_part(
        self: "Self", design_entity: "_2851.SynchroniserPart"
    ) -> "_4697.SynchroniserPartParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserPartParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_PART],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_part_load_case(
        self: "Self", design_entity_analysis: "_7840.SynchroniserPartLoadCase"
    ) -> "_4697.SynchroniserPartParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserPartParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_PART_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_sleeve(
        self: "Self", design_entity: "_2852.SynchroniserSleeve"
    ) -> "_4698.SynchroniserSleeveParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserSleeveParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_SLEEVE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_synchroniser_sleeve_load_case(
        self: "Self", design_entity_analysis: "_7841.SynchroniserSleeveLoadCase"
    ) -> "_4698.SynchroniserSleeveParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserSleeveParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SYNCHRONISER_SLEEVE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter(
        self: "Self", design_entity: "_2853.TorqueConverter"
    ) -> "_4700.TorqueConverterParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_load_case(
        self: "Self", design_entity_analysis: "_7845.TorqueConverterLoadCase"
    ) -> "_4700.TorqueConverterParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_pump(
        self: "Self", design_entity: "_2854.TorqueConverterPump"
    ) -> "_4701.TorqueConverterPumpParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterPumpParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_PUMP],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_pump_load_case(
        self: "Self", design_entity_analysis: "_7846.TorqueConverterPumpLoadCase"
    ) -> "_4701.TorqueConverterPumpParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterPumpParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_PUMP_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_turbine(
        self: "Self", design_entity: "_2856.TorqueConverterTurbine"
    ) -> "_4702.TorqueConverterTurbineParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterTurbineParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_TURBINE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_torque_converter_turbine_load_case(
        self: "Self", design_entity_analysis: "_7847.TorqueConverterTurbineLoadCase"
    ) -> "_4702.TorqueConverterTurbineParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterTurbineParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_TORQUE_CONVERTER_TURBINE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2516.ShaftToMountableComponentConnection"
    ) -> "_4679.ShaftToMountableComponentConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftToMountableComponentConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft_to_mountable_component_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7822.ShaftToMountableComponentConnectionLoadCase",
    ) -> "_4679.ShaftToMountableComponentConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftToMountableComponentConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt_belt_connection(
        self: "Self", design_entity: "_2494.CVTBeltConnection"
    ) -> "_4601.CVTBeltConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CVTBeltConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_BELT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cvt_belt_connection_load_case(
        self: "Self", design_entity_analysis: "_7723.CVTBeltConnectionLoadCase"
    ) -> "_4601.CVTBeltConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CVTBeltConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CVT_BELT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_belt_connection(
        self: "Self", design_entity: "_2489.BeltConnection"
    ) -> "_4570.BeltConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BeltConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_belt_connection_load_case(
        self: "Self", design_entity_analysis: "_7689.BeltConnectionLoadCase"
    ) -> "_4570.BeltConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BeltConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BELT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_coaxial_connection(
        self: "Self", design_entity: "_2490.CoaxialConnection"
    ) -> "_4585.CoaxialConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CoaxialConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COAXIAL_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_coaxial_connection_load_case(
        self: "Self", design_entity_analysis: "_7705.CoaxialConnectionLoadCase"
    ) -> "_4585.CoaxialConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CoaxialConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COAXIAL_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_connection(
        self: "Self", design_entity: "_2493.Connection"
    ) -> "_4596.ConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_connection_load_case(
        self: "Self", design_entity_analysis: "_7718.ConnectionLoadCase"
    ) -> "_4596.ConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_inter_mountable_component_connection(
        self: "Self", design_entity: "_2502.InterMountableComponentConnection"
    ) -> "_4633.InterMountableComponentConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.InterMountableComponentConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_INTER_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_inter_mountable_component_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7780.InterMountableComponentConnectionLoadCase",
    ) -> "_4633.InterMountableComponentConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.InterMountableComponentConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_INTER_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_planetary_connection(
        self: "Self", design_entity: "_2508.PlanetaryConnection"
    ) -> "_4665.PlanetaryConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_planetary_connection_load_case(
        self: "Self", design_entity_analysis: "_7803.PlanetaryConnectionLoadCase"
    ) -> "_4665.PlanetaryConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring_connection(
        self: "Self", design_entity: "_2513.RollingRingConnection"
    ) -> "_4674.RollingRingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_rolling_ring_connection_load_case(
        self: "Self", design_entity_analysis: "_7817.RollingRingConnectionLoadCase"
    ) -> "_4674.RollingRingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROLLING_RING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2486.AbstractShaftToMountableComponentConnection"
    ) -> "_4564.AbstractShaftToMountableComponentConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftToMountableComponentConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft_to_mountable_component_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7678.AbstractShaftToMountableComponentConnectionLoadCase",
    ) -> "_4564.AbstractShaftToMountableComponentConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftToMountableComponentConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftToMountableComponentConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear_mesh(
        self: "Self", design_entity: "_2522.BevelDifferentialGearMesh"
    ) -> "_4572.BevelDifferentialGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7692.BevelDifferentialGearMeshLoadCase"
    ) -> "_4572.BevelDifferentialGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear_mesh(
        self: "Self", design_entity: "_2526.ConceptGearMesh"
    ) -> "_4590.ConceptGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7711.ConceptGearMeshLoadCase"
    ) -> "_4590.ConceptGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear_mesh(
        self: "Self", design_entity: "_2532.FaceGearMesh"
    ) -> "_4621.FaceGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7754.FaceGearMeshLoadCase"
    ) -> "_4621.FaceGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_mesh(
        self: "Self", design_entity: "_2546.StraightBevelDiffGearMesh"
    ) -> "_4687.StraightBevelDiffGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7831.StraightBevelDiffGearMeshLoadCase"
    ) -> "_4687.StraightBevelDiffGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear_mesh(
        self: "Self", design_entity: "_2524.BevelGearMesh"
    ) -> "_4577.BevelGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7697.BevelGearMeshLoadCase"
    ) -> "_4577.BevelGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear_mesh(
        self: "Self", design_entity: "_2528.ConicalGearMesh"
    ) -> "_4593.ConicalGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7715.ConicalGearMeshLoadCase"
    ) -> "_4593.ConicalGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_mesh(
        self: "Self", design_entity: "_2520.AGMAGleasonConicalGearMesh"
    ) -> "_4565.AGMAGleasonConicalGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7683.AGMAGleasonConicalGearMeshLoadCase"
    ) -> "_4565.AGMAGleasonConicalGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear_mesh(
        self: "Self", design_entity: "_2530.CylindricalGearMesh"
    ) -> "_4608.CylindricalGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7732.CylindricalGearMeshLoadCase"
    ) -> "_4608.CylindricalGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear_mesh(
        self: "Self", design_entity: "_2536.HypoidGearMesh"
    ) -> "_4630.HypoidGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7775.HypoidGearMeshLoadCase"
    ) -> "_4630.HypoidGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "Self", design_entity: "_2539.KlingelnbergCycloPalloidConicalGearMesh"
    ) -> "_4634.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(
        self: "Self",
        design_entity_analysis: "_7782.KlingelnbergCycloPalloidConicalGearMeshLoadCase",
    ) -> "_4634.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "Self", design_entity: "_2540.KlingelnbergCycloPalloidHypoidGearMesh"
    ) -> "_4637.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(
        self: "Self",
        design_entity_analysis: "_7785.KlingelnbergCycloPalloidHypoidGearMeshLoadCase",
    ) -> "_4637.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2541.KlingelnbergCycloPalloidSpiralBevelGearMesh"
    ) -> "_4640.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(
        self: "Self",
        design_entity_analysis: "_7788.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase",
    ) -> "_4640.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2544.SpiralBevelGearMesh"
    ) -> "_4681.SpiralBevelGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7825.SpiralBevelGearMeshLoadCase"
    ) -> "_4681.SpiralBevelGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear_mesh(
        self: "Self", design_entity: "_2548.StraightBevelGearMesh"
    ) -> "_4690.StraightBevelGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7834.StraightBevelGearMeshLoadCase"
    ) -> "_4690.StraightBevelGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear_mesh(
        self: "Self", design_entity: "_2550.WormGearMesh"
    ) -> "_4705.WormGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_worm_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7855.WormGearMeshLoadCase"
    ) -> "_4705.WormGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_WORM_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear_mesh(
        self: "Self", design_entity: "_2552.ZerolBevelGearMesh"
    ) -> "_4708.ZerolBevelGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_zerol_bevel_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7858.ZerolBevelGearMeshLoadCase"
    ) -> "_4708.ZerolBevelGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ZEROL_BEVEL_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear_mesh(
        self: "Self", design_entity: "_2534.GearMesh"
    ) -> "_4626.GearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.GearMeshParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_MESH],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear_mesh_load_case(
        self: "Self", design_entity_analysis: "_7761.GearMeshLoadCase"
    ) -> "_4626.GearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.GearMeshParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_MESH_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc_central_bearing_connection(
        self: "Self", design_entity: "_2556.CycloidalDiscCentralBearingConnection"
    ) -> "_4605.CycloidalDiscCentralBearingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalDiscCentralBearingConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc_central_bearing_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7727.CycloidalDiscCentralBearingConnectionLoadCase",
    ) -> "_4605.CycloidalDiscCentralBearingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalDiscCentralBearingConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscCentralBearingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc_planetary_bearing_connection(
        self: "Self", design_entity: "_2559.CycloidalDiscPlanetaryBearingConnection"
    ) -> "_4607.CycloidalDiscPlanetaryBearingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalDiscPlanetaryBearingConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cycloidal_disc_planetary_bearing_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7729.CycloidalDiscPlanetaryBearingConnectionLoadCase",
    ) -> "_4607.CycloidalDiscPlanetaryBearingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalDiscPlanetaryBearingConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscPlanetaryBearingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_ring_pins_to_disc_connection(
        self: "Self", design_entity: "_2562.RingPinsToDiscConnection"
    ) -> "_4672.RingPinsToDiscConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RingPinsToDiscConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS_TO_DISC_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_ring_pins_to_disc_connection_load_case(
        self: "Self", design_entity_analysis: "_7815.RingPinsToDiscConnectionLoadCase"
    ) -> "_4672.RingPinsToDiscConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RingPinsToDiscConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RingPinsToDiscConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_RING_PINS_TO_DISC_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_connection(
        self: "Self", design_entity: "_2569.PartToPartShearCouplingConnection"
    ) -> "_4662.PartToPartShearCouplingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingConnectionParametricStudyTool

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_CONNECTION],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_connection_load_case(
        self: "Self",
        design_entity_analysis: "_7800.PartToPartShearCouplingConnectionLoadCase",
    ) -> "_4662.PartToPartShearCouplingConnectionParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingConnectionParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft(
        self: "Self", design_entity: "_2660.AbstractShaft"
    ) -> "_4563.AbstractShaftParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft_load_case(
        self: "Self", design_entity_analysis: "_7676.AbstractShaftLoadCase"
    ) -> "_4563.AbstractShaftParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_microphone(
        self: "Self", design_entity: "_2691.Microphone"
    ) -> "_4646.MicrophoneParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.MicrophoneParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.Microphone)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_microphone_load_case(
        self: "Self", design_entity_analysis: "_7794.MicrophoneLoadCase"
    ) -> "_4646.MicrophoneParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.MicrophoneParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MicrophoneLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_microphone_array(
        self: "Self", design_entity: "_2692.MicrophoneArray"
    ) -> "_4645.MicrophoneArrayParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.MicrophoneArrayParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.MicrophoneArray)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE_ARRAY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_microphone_array_load_case(
        self: "Self", design_entity_analysis: "_7793.MicrophoneArrayLoadCase"
    ) -> "_4645.MicrophoneArrayParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.MicrophoneArrayParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MicrophoneArrayLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MICROPHONE_ARRAY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_assembly(
        self: "Self", design_entity: "_2659.AbstractAssembly"
    ) -> "_4561.AbstractAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractAssemblyParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_assembly_load_case(
        self: "Self", design_entity_analysis: "_7675.AbstractAssemblyLoadCase"
    ) -> "_4561.AbstractAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractAssemblyParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft_or_housing(
        self: "Self", design_entity: "_2661.AbstractShaftOrHousing"
    ) -> "_4562.AbstractShaftOrHousingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftOrHousingParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_OR_HOUSING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_abstract_shaft_or_housing_load_case(
        self: "Self", design_entity_analysis: "_7677.AbstractShaftOrHousingLoadCase"
    ) -> "_4562.AbstractShaftOrHousingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftOrHousingParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bearing(
        self: "Self", design_entity: "_2664.Bearing"
    ) -> "_4569.BearingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BearingParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEARING],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bearing_load_case(
        self: "Self", design_entity_analysis: "_7688.BearingLoadCase"
    ) -> "_4569.BearingParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BearingParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEARING_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bolt(
        self: "Self", design_entity: "_2667.Bolt"
    ) -> "_4581.BoltParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BoltParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bolt_load_case(
        self: "Self", design_entity_analysis: "_7700.BoltLoadCase"
    ) -> "_4581.BoltParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BoltParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bolted_joint(
        self: "Self", design_entity: "_2668.BoltedJoint"
    ) -> "_4580.BoltedJointParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BoltedJointParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLTED_JOINT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bolted_joint_load_case(
        self: "Self", design_entity_analysis: "_7699.BoltedJointLoadCase"
    ) -> "_4580.BoltedJointParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BoltedJointParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BOLTED_JOINT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_component(
        self: "Self", design_entity: "_2670.Component"
    ) -> "_4586.ComponentParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ComponentParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_component_load_case(
        self: "Self", design_entity_analysis: "_7706.ComponentLoadCase"
    ) -> "_4586.ComponentParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ComponentParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_connector(
        self: "Self", design_entity: "_2673.Connector"
    ) -> "_4597.ConnectorParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectorParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.Connector)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTOR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_connector_load_case(
        self: "Self", design_entity_analysis: "_7719.ConnectorLoadCase"
    ) -> "_4597.ConnectorParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectorParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONNECTOR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_datum(
        self: "Self", design_entity: "_2674.Datum"
    ) -> "_4612.DatumParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.DatumParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.Datum)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_DATUM],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_datum_load_case(
        self: "Self", design_entity_analysis: "_7738.DatumLoadCase"
    ) -> "_4612.DatumParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.DatumParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_DATUM_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_external_cad_model(
        self: "Self", design_entity: "_2679.ExternalCADModel"
    ) -> "_4620.ExternalCADModelParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ExternalCADModelParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_EXTERNAL_CAD_MODEL],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_external_cad_model_load_case(
        self: "Self", design_entity_analysis: "_7752.ExternalCADModelLoadCase"
    ) -> "_4620.ExternalCADModelParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ExternalCADModelParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_EXTERNAL_CAD_MODEL_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_fe_part(
        self: "Self", design_entity: "_2680.FEPart"
    ) -> "_4624.FEPartParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.FEPartParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FE_PART],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_fe_part_load_case(
        self: "Self", design_entity_analysis: "_7756.FEPartLoadCase"
    ) -> "_4624.FEPartParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.FEPartParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FE_PART_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_flexible_pin_assembly(
        self: "Self", design_entity: "_2681.FlexiblePinAssembly"
    ) -> "_4625.FlexiblePinAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.FlexiblePinAssemblyParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FLEXIBLE_PIN_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_flexible_pin_assembly_load_case(
        self: "Self", design_entity_analysis: "_7757.FlexiblePinAssemblyLoadCase"
    ) -> "_4625.FlexiblePinAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.FlexiblePinAssemblyParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_assembly(
        self: "Self", design_entity: "_2658.Assembly"
    ) -> "_4568.AssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AssemblyParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_assembly_load_case(
        self: "Self", design_entity_analysis: "_7687.AssemblyLoadCase"
    ) -> "_4568.AssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AssemblyParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_guide_dxf_model(
        self: "Self", design_entity: "_2682.GuideDxfModel"
    ) -> "_4629.GuideDxfModelParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.GuideDxfModelParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GUIDE_DXF_MODEL],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_guide_dxf_model_load_case(
        self: "Self", design_entity_analysis: "_7765.GuideDxfModelLoadCase"
    ) -> "_4629.GuideDxfModelParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.GuideDxfModelParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GUIDE_DXF_MODEL_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_mass_disc(
        self: "Self", design_entity: "_2689.MassDisc"
    ) -> "_4643.MassDiscParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.MassDiscParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MASS_DISC],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_mass_disc_load_case(
        self: "Self", design_entity_analysis: "_7790.MassDiscLoadCase"
    ) -> "_4643.MassDiscParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.MassDiscParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MASS_DISC_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_measurement_component(
        self: "Self", design_entity: "_2690.MeasurementComponent"
    ) -> "_4644.MeasurementComponentParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.MeasurementComponentParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MEASUREMENT_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_measurement_component_load_case(
        self: "Self", design_entity_analysis: "_7791.MeasurementComponentLoadCase"
    ) -> "_4644.MeasurementComponentParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.MeasurementComponentParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MEASUREMENT_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_mountable_component(
        self: "Self", design_entity: "_2693.MountableComponent"
    ) -> "_4648.MountableComponentParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.MountableComponentParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MOUNTABLE_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_mountable_component_load_case(
        self: "Self", design_entity_analysis: "_7795.MountableComponentLoadCase"
    ) -> "_4648.MountableComponentParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.MountableComponentParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_MOUNTABLE_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_oil_seal(
        self: "Self", design_entity: "_2695.OilSeal"
    ) -> "_4649.OilSealParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.OilSealParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_OIL_SEAL],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_oil_seal_load_case(
        self: "Self", design_entity_analysis: "_7797.OilSealLoadCase"
    ) -> "_4649.OilSealParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.OilSealParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_OIL_SEAL_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_part(
        self: "Self", design_entity: "_2698.Part"
    ) -> "_4661.PartParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PartParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.Part)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_part_load_case(
        self: "Self", design_entity_analysis: "_7799.PartLoadCase"
    ) -> "_4661.PartParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PartParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PART_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_planet_carrier(
        self: "Self", design_entity: "_2700.PlanetCarrier"
    ) -> "_4667.PlanetCarrierParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetCarrierParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANET_CARRIER],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_planet_carrier_load_case(
        self: "Self", design_entity_analysis: "_7806.PlanetCarrierLoadCase"
    ) -> "_4667.PlanetCarrierParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetCarrierParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANET_CARRIER_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_point_load(
        self: "Self", design_entity: "_2702.PointLoad"
    ) -> "_4668.PointLoadParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PointLoadParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POINT_LOAD],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_point_load_load_case(
        self: "Self", design_entity_analysis: "_7809.PointLoadLoadCase"
    ) -> "_4668.PointLoadParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PointLoadParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POINT_LOAD_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_power_load(
        self: "Self", design_entity: "_2703.PowerLoad"
    ) -> "_4669.PowerLoadParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PowerLoadParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POWER_LOAD],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_power_load_load_case(
        self: "Self", design_entity_analysis: "_7810.PowerLoadLoadCase"
    ) -> "_4669.PowerLoadParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PowerLoadParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_POWER_LOAD_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_root_assembly(
        self: "Self", design_entity: "_2706.RootAssembly"
    ) -> "_4676.RootAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RootAssemblyParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROOT_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_root_assembly_load_case(
        self: "Self", design_entity_analysis: "_7819.RootAssemblyLoadCase"
    ) -> "_4676.RootAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.RootAssemblyParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_ROOT_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_specialised_assembly(
        self: "Self", design_entity: "_2708.SpecialisedAssembly"
    ) -> "_4680.SpecialisedAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpecialisedAssemblyParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPECIALISED_ASSEMBLY],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_specialised_assembly_load_case(
        self: "Self", design_entity_analysis: "_7823.SpecialisedAssemblyLoadCase"
    ) -> "_4680.SpecialisedAssemblyParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpecialisedAssemblyParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPECIALISED_ASSEMBLY_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_unbalanced_mass(
        self: "Self", design_entity: "_2709.UnbalancedMass"
    ) -> "_4703.UnbalancedMassParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.UnbalancedMassParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_UNBALANCED_MASS],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_unbalanced_mass_load_case(
        self: "Self", design_entity_analysis: "_7852.UnbalancedMassLoadCase"
    ) -> "_4703.UnbalancedMassParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.UnbalancedMassParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_UNBALANCED_MASS_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_virtual_component(
        self: "Self", design_entity: "_2711.VirtualComponent"
    ) -> "_4704.VirtualComponentParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_VIRTUAL_COMPONENT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_virtual_component_load_case(
        self: "Self", design_entity_analysis: "_7853.VirtualComponentLoadCase"
    ) -> "_4704.VirtualComponentParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_VIRTUAL_COMPONENT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft(
        self: "Self", design_entity: "_2714.Shaft"
    ) -> "_4678.ShaftParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_shaft_load_case(
        self: "Self", design_entity_analysis: "_7821.ShaftLoadCase"
    ) -> "_4678.ShaftParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SHAFT_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear(
        self: "Self", design_entity: "_2758.ConceptGear"
    ) -> "_4591.ConceptGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear_load_case(
        self: "Self", design_entity_analysis: "_7710.ConceptGearLoadCase"
    ) -> "_4591.ConceptGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear_set(
        self: "Self", design_entity: "_2759.ConceptGearSet"
    ) -> "_4592.ConceptGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_concept_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7712.ConceptGearSetLoadCase"
    ) -> "_4592.ConceptGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONCEPT_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear(
        self: "Self", design_entity: "_2765.FaceGear"
    ) -> "_4622.FaceGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear_load_case(
        self: "Self", design_entity_analysis: "_7753.FaceGearLoadCase"
    ) -> "_4622.FaceGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear_set(
        self: "Self", design_entity: "_2766.FaceGearSet"
    ) -> "_4623.FaceGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_face_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7755.FaceGearSetLoadCase"
    ) -> "_4623.FaceGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_FACE_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear(
        self: "Self", design_entity: "_2750.AGMAGleasonConicalGear"
    ) -> "_4566.AGMAGleasonConicalGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_load_case(
        self: "Self", design_entity_analysis: "_7682.AGMAGleasonConicalGearLoadCase"
    ) -> "_4566.AGMAGleasonConicalGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_set(
        self: "Self", design_entity: "_2751.AGMAGleasonConicalGearSet"
    ) -> "_4567.AGMAGleasonConicalGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7684.AGMAGleasonConicalGearSetLoadCase"
    ) -> "_4567.AGMAGleasonConicalGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear(
        self: "Self", design_entity: "_2752.BevelDifferentialGear"
    ) -> "_4573.BevelDifferentialGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear_load_case(
        self: "Self", design_entity_analysis: "_7691.BevelDifferentialGearLoadCase"
    ) -> "_4573.BevelDifferentialGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear_set(
        self: "Self", design_entity: "_2753.BevelDifferentialGearSet"
    ) -> "_4574.BevelDifferentialGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7693.BevelDifferentialGearSetLoadCase"
    ) -> "_4574.BevelDifferentialGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_planet_gear(
        self: "Self", design_entity: "_2754.BevelDifferentialPlanetGear"
    ) -> "_4575.BevelDifferentialPlanetGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialPlanetGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_planet_gear_load_case(
        self: "Self",
        design_entity_analysis: "_7694.BevelDifferentialPlanetGearLoadCase",
    ) -> "_4575.BevelDifferentialPlanetGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialPlanetGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_PLANET_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_sun_gear(
        self: "Self", design_entity: "_2755.BevelDifferentialSunGear"
    ) -> "_4576.BevelDifferentialSunGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialSunGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_SUN_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_differential_sun_gear_load_case(
        self: "Self", design_entity_analysis: "_7695.BevelDifferentialSunGearLoadCase"
    ) -> "_4576.BevelDifferentialSunGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialSunGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear(
        self: "Self", design_entity: "_2756.BevelGear"
    ) -> "_4578.BevelGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_7696.BevelGearLoadCase"
    ) -> "_4578.BevelGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear_set(
        self: "Self", design_entity: "_2757.BevelGearSet"
    ) -> "_4579.BevelGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7698.BevelGearSetLoadCase"
    ) -> "_4579.BevelGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear(
        self: "Self", design_entity: "_2760.ConicalGear"
    ) -> "_4594.ConicalGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear_load_case(
        self: "Self", design_entity_analysis: "_7713.ConicalGearLoadCase"
    ) -> "_4594.ConicalGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear_set(
        self: "Self", design_entity: "_2761.ConicalGearSet"
    ) -> "_4595.ConicalGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_conical_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7717.ConicalGearSetLoadCase"
    ) -> "_4595.ConicalGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CONICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear(
        self: "Self", design_entity: "_2762.CylindricalGear"
    ) -> "_4609.CylindricalGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear_load_case(
        self: "Self", design_entity_analysis: "_7730.CylindricalGearLoadCase"
    ) -> "_4609.CylindricalGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear_set(
        self: "Self", design_entity: "_2763.CylindricalGearSet"
    ) -> "_4610.CylindricalGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7734.CylindricalGearSetLoadCase"
    ) -> "_4610.CylindricalGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_planet_gear(
        self: "Self", design_entity: "_2764.CylindricalPlanetGear"
    ) -> "_4611.CylindricalPlanetGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalPlanetGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_PLANET_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_cylindrical_planet_gear_load_case(
        self: "Self", design_entity_analysis: "_7735.CylindricalPlanetGearLoadCase"
    ) -> "_4611.CylindricalPlanetGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalPlanetGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_CYLINDRICAL_PLANET_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear(
        self: "Self", design_entity: "_2767.Gear"
    ) -> "_4627.GearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.GearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear_load_case(
        self: "Self", design_entity_analysis: "_7759.GearLoadCase"
    ) -> "_4627.GearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.GearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear_set(
        self: "Self", design_entity: "_2769.GearSet"
    ) -> "_4628.GearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.GearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7764.GearSetLoadCase"
    ) -> "_4628.GearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.GearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear(
        self: "Self", design_entity: "_2771.HypoidGear"
    ) -> "_4631.HypoidGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear_load_case(
        self: "Self", design_entity_analysis: "_7774.HypoidGearLoadCase"
    ) -> "_4631.HypoidGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear_set(
        self: "Self", design_entity: "_2772.HypoidGearSet"
    ) -> "_4632.HypoidGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_hypoid_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7776.HypoidGearSetLoadCase"
    ) -> "_4632.HypoidGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_HYPOID_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear(
        self: "Self", design_entity: "_2773.KlingelnbergCycloPalloidConicalGear"
    ) -> "_4635.KlingelnbergCycloPalloidConicalGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "Self",
        design_entity_analysis: "_7781.KlingelnbergCycloPalloidConicalGearLoadCase",
    ) -> "_4635.KlingelnbergCycloPalloidConicalGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(
        self: "Self", design_entity: "_2774.KlingelnbergCycloPalloidConicalGearSet"
    ) -> "_4636.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "Self",
        design_entity_analysis: "_7783.KlingelnbergCycloPalloidConicalGearSetLoadCase",
    ) -> "_4636.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(
        self: "Self", design_entity: "_2775.KlingelnbergCycloPalloidHypoidGear"
    ) -> "_4638.KlingelnbergCycloPalloidHypoidGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "Self",
        design_entity_analysis: "_7784.KlingelnbergCycloPalloidHypoidGearLoadCase",
    ) -> "_4638.KlingelnbergCycloPalloidHypoidGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self", design_entity: "_2776.KlingelnbergCycloPalloidHypoidGearSet"
    ) -> "_4639.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "Self",
        design_entity_analysis: "_7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase",
    ) -> "_4639.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "Self", design_entity: "_2777.KlingelnbergCycloPalloidSpiralBevelGear"
    ) -> "_4641.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "Self",
        design_entity_analysis: "_7787.KlingelnbergCycloPalloidSpiralBevelGearLoadCase",
    ) -> "_4641.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2778.KlingelnbergCycloPalloidSpiralBevelGearSet"
    ) -> "_4642.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "Self",
        design_entity_analysis: "_7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase",
    ) -> "_4642.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_planetary_gear_set(
        self: "Self", design_entity: "_2779.PlanetaryGearSet"
    ) -> "_4666.PlanetaryGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_planetary_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7804.PlanetaryGearSetLoadCase"
    ) -> "_4666.PlanetaryGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_PLANETARY_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear(
        self: "Self", design_entity: "_2781.SpiralBevelGear"
    ) -> "_4682.SpiralBevelGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_7824.SpiralBevelGearLoadCase"
    ) -> "_4682.SpiralBevelGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2782.SpiralBevelGearSet"
    ) -> "_4683.SpiralBevelGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_spiral_bevel_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7826.SpiralBevelGearSetLoadCase"
    ) -> "_4683.SpiralBevelGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear(
        self: "Self", design_entity: "_2783.StraightBevelDiffGear"
    ) -> "_4688.StraightBevelDiffGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_load_case(
        self: "Self", design_entity_analysis: "_7830.StraightBevelDiffGearLoadCase"
    ) -> "_4688.StraightBevelDiffGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_set(
        self: "Self", design_entity: "_2784.StraightBevelDiffGearSet"
    ) -> "_4689.StraightBevelDiffGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearSetParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_SET],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_set_load_case(
        self: "Self", design_entity_analysis: "_7832.StraightBevelDiffGearSetLoadCase"
    ) -> "_4689.StraightBevelDiffGearSetParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearSetParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_DIFF_GEAR_SET_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear(
        self: "Self", design_entity: "_2785.StraightBevelGear"
    ) -> "_4691.StraightBevelGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearParametricStudyTool

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR],
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def results_for_straight_bevel_gear_load_case(
        self: "Self", design_entity_analysis: "_7833.StraightBevelGearLoadCase"
    ) -> "_4691.StraightBevelGearParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearParametricStudyTool

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ResultsFor",
            [_STRAIGHT_BEVEL_GEAR_LOAD_CASE],
            design_entity_analysis.wrapped if design_entity_analysis else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ParametricStudyTool
        """
        return _Cast_ParametricStudyTool(self)
