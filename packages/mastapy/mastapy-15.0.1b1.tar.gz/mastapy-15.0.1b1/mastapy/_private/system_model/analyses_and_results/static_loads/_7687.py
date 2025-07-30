"""AssemblyLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7675

_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "AssemblyLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1347
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7677,
        _7688,
        _7690,
        _7693,
        _7699,
        _7700,
        _7701,
        _7703,
        _7709,
        _7712,
        _7724,
        _7726,
        _7728,
        _7734,
        _7755,
        _7756,
        _7757,
        _7761,
        _7776,
        _7786,
        _7789,
        _7790,
        _7791,
        _7794,
        _7797,
        _7799,
        _7802,
        _7806,
        _7809,
        _7810,
        _7814,
        _7815,
        _7816,
        _7819,
        _7820,
        _7821,
        _7826,
        _7829,
        _7832,
        _7835,
        _7839,
        _7845,
        _7852,
        _7856,
        _7859,
    )
    from mastapy._private.system_model.part_model import _2658

    Self = TypeVar("Self", bound="AssemblyLoadCase")
    CastSelf = TypeVar("CastSelf", bound="AssemblyLoadCase._Cast_AssemblyLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("AssemblyLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AssemblyLoadCase:
    """Special nested class for casting AssemblyLoadCase to subclasses."""

    __parent__: "AssemblyLoadCase"

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_7675.AbstractAssemblyLoadCase":
        return self.__parent__._cast(_7675.AbstractAssemblyLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7799,
        )

        return self.__parent__._cast(_7799.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def root_assembly_load_case(self: "CastSelf") -> "_7819.RootAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7819,
        )

        return self.__parent__._cast(_7819.RootAssemblyLoadCase)

    @property
    def assembly_load_case(self: "CastSelf") -> "AssemblyLoadCase":
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
class AssemblyLoadCase(_7675.AbstractAssemblyLoadCase):
    """AssemblyLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ASSEMBLY_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2658.Assembly":
        """mastapy.system_model.part_model.Assembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rating_for_all_gear_sets(self: "Self") -> "_1347.GearSetGroupDutyCycle":
        """mastapy.gears.analysis.GearSetGroupDutyCycle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingForAllGearSets")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bearings(self: "Self") -> "List[_7688.BearingLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bearings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def belt_drives(self: "Self") -> "List[_7690.BeltDriveLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeltDrives")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def bevel_differential_gear_sets(
        self: "Self",
    ) -> "List[_7693.BevelDifferentialGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelDifferentialGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def bolted_joints(self: "Self") -> "List[_7699.BoltedJointLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltedJoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def bolts(self: "Self") -> "List[_7700.BoltLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bolts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cv_ts(self: "Self") -> "List[_7724.CVTLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CVTs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def clutch_connections(self: "Self") -> "List[_7701.ClutchConnectionLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClutchConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def clutches(self: "Self") -> "List[_7703.ClutchLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Clutches")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def concept_couplings(self: "Self") -> "List[_7709.ConceptCouplingLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptCouplings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def concept_gear_sets(self: "Self") -> "List[_7712.ConceptGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cycloidal_assemblies(self: "Self") -> "List[_7726.CycloidalAssemblyLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CycloidalAssemblyLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cycloidal_discs(self: "Self") -> "List[_7728.CycloidalDiscLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalDiscs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_gear_sets(self: "Self") -> "List[_7734.CylindricalGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def fe_parts(self: "Self") -> "List[_7756.FEPartLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEParts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def face_gear_sets(self: "Self") -> "List[_7755.FaceGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def flexible_pin_assemblies(
        self: "Self",
    ) -> "List[_7757.FlexiblePinAssemblyLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlexiblePinAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_meshes(self: "Self") -> "List[_7761.GearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def hypoid_gear_sets(self: "Self") -> "List[_7776.HypoidGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(
        self: "Self",
    ) -> "List[_7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearSets"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(
        self: "Self",
    ) -> "List[_7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidSpiralBevelGearSets"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def mass_discs(self: "Self") -> "List[_7790.MassDiscLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassDiscs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def measurement_components(
        self: "Self",
    ) -> "List[_7791.MeasurementComponentLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeasurementComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def microphones(self: "Self") -> "List[_7794.MicrophoneLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.MicrophoneLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Microphones")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def oil_seals(self: "Self") -> "List[_7797.OilSealLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilSeals")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def part_to_part_shear_couplings(
        self: "Self",
    ) -> "List[_7802.PartToPartShearCouplingLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartToPartShearCouplings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def planet_carriers(self: "Self") -> "List[_7806.PlanetCarrierLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetCarriers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def point_loads(self: "Self") -> "List[_7809.PointLoadLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def power_loads(self: "Self") -> "List[_7810.PowerLoadLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def ring_pins(self: "Self") -> "List[_7814.RingPinsLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.RingPinsLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPins")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def ring_pins_to_cycloidal_disc_connections(
        self: "Self",
    ) -> "List[_7815.RingPinsToDiscConnectionLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.RingPinsToDiscConnectionLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RingPinsToCycloidalDiscConnections"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def rolling_ring_assemblies(
        self: "Self",
    ) -> "List[_7816.RollingRingAssemblyLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingRingAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shaft_hub_connections(self: "Self") -> "List[_7820.ShaftHubConnectionLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftHubConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shafts(self: "Self") -> "List[_7821.ShaftLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shafts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shafts_and_housings(
        self: "Self",
    ) -> "List[_7677.AbstractShaftOrHousingLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftsAndHousings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def spiral_bevel_gear_sets(
        self: "Self",
    ) -> "List[_7826.SpiralBevelGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def spring_dampers(self: "Self") -> "List[_7829.SpringDamperLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpringDampers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def straight_bevel_diff_gear_sets(
        self: "Self",
    ) -> "List[_7832.StraightBevelDiffGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def straight_bevel_gear_sets(
        self: "Self",
    ) -> "List[_7835.StraightBevelGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def synchronisers(self: "Self") -> "List[_7839.SynchroniserLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Synchronisers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def torque_converters(self: "Self") -> "List[_7845.TorqueConverterLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueConverters")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def unbalanced_masses(self: "Self") -> "List[_7852.UnbalancedMassLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UnbalancedMasses")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def worm_gear_sets(self: "Self") -> "List[_7856.WormGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def zerol_bevel_gear_sets(self: "Self") -> "List[_7859.ZerolBevelGearSetLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AssemblyLoadCase":
        """Cast to another type.

        Returns:
            _Cast_AssemblyLoadCase
        """
        return _Cast_AssemblyLoadCase(self)
