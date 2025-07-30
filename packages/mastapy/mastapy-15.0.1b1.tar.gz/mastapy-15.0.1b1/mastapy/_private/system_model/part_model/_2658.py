"""Assembly"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_generic,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.bevel import _1299
from mastapy._private.system_model.part_model import _2659

_ARRAY = python_net_import("System", "Array")
_STRING = python_net_import("System", "String")
_DOUBLE = python_net_import("System", "Double")
_INT_32 = python_net_import("System", "Int32")
_ROLLING_BEARING_TYPE = python_net_import("SMT.MastaAPI.Bearings", "RollingBearingType")
_BELT_CREATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.CreationOptions", "BeltCreationOptions"
)
_CYCLOIDAL_ASSEMBLY_CREATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.CreationOptions",
    "CycloidalAssemblyCreationOptions",
)
_CYLINDRICAL_GEAR_LINEAR_TRAIN_CREATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.CreationOptions",
    "CylindricalGearLinearTrainCreationOptions",
)
_PLANET_CARRIER_CREATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.CreationOptions", "PlanetCarrierCreationOptions"
)
_SHAFT_CREATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.CreationOptions", "ShaftCreationOptions"
)
_CYLINDRICAL_GEAR_PAIR_CREATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.CreationOptions",
    "CylindricalGearPairCreationOptions",
)
_SPIRAL_BEVEL_GEAR_SET_CREATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.CreationOptions",
    "SpiralBevelGearSetCreationOptions",
)
_HAND = python_net_import("SMT.MastaAPI.Gears", "Hand")
_AGMA_GLEASON_CONICAL_GEAR_GEOMETRY_METHODS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "AGMAGleasonConicalGearGeometryMethods"
)
_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Assembly")

if TYPE_CHECKING:
    from typing import Any, List, Optional, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings import _2072, _2099
    from mastapy._private.gears import _423
    from mastapy._private.gears.gear_designs.creation_options import _1265, _1266, _1269
    from mastapy._private.nodal_analysis import _82
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import (
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
        _2694,
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
    from mastapy._private.system_model.part_model.creation_options import (
        _2809,
        _2810,
        _2811,
        _2813,
        _2814,
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

    T_get_part_named = TypeVar("T_get_part_named", bound="_2698.Part")
    T_all_parts = TypeVar("T_all_parts", bound="_2698.Part")
    Self = TypeVar("Self", bound="Assembly")
    CastSelf = TypeVar("CastSelf", bound="Assembly._Cast_Assembly")


__docformat__ = "restructuredtext en"
__all__ = ("Assembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Assembly:
    """Special nested class for casting Assembly to subclasses."""

    __parent__: "Assembly"

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        return self.__parent__._cast(_2659.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def root_assembly(self: "CastSelf") -> "_2706.RootAssembly":
        return self.__parent__._cast(_2706.RootAssembly)

    @property
    def assembly(self: "CastSelf") -> "Assembly":
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
class Assembly(_2659.AbstractAssembly):
    """Assembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ASSEMBLY

    class PartType(Enum):
        """PartType is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _ASSEMBLY.PartType

        ASSEMBLY = 0
        BEARING = 1
        SHAFT = 2
        OIL_SEAL = 3
        POWER_LOAD = 4
        POINT_LOAD = 5
        DATUM = 6
        MEASUREMENT_POINT = 7
        MASS_DISC = 8
        UNBALANCED_MASS = 9
        STRAIGHT_BEVEL_DIFFERENTIAL_GEAR_SET = 10
        SPIRAL_BEVEL_DIFFERENTIAL_GEAR_SET = 11
        ZEROL_BEVEL_DIFFERENTIAL_GEAR_SET = 12
        CYLINDRICAL_GEAR_PAIR = 13
        CYLINDRICAL_GEAR_SET = 14
        CYLINDRICAL_PLANETARY_GEAR_SET = 15
        SPIRAL_BEVEL_GEAR_SET = 16
        KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = 17
        KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = 18
        STRAIGHT_BEVEL_GEAR_SET = 19
        HYPOID_GEAR_SET = 20
        WORM_GEAR_SET = 21
        ZEROL_BEVEL_GEAR_SET = 22
        CLUTCH = 23
        SHAFT_HUB_CONNECTION = 24
        SYNCHRONISER = 25
        ROLLING_RING = 26
        BELT_DRIVE = 27
        CONCEPT_COUPLING = 28
        CVT = 29
        SPRING_DAMPER = 30
        TORQUE_CONVERTER = 31
        BOLTED_JOINT = 32
        CYCLOIDAL_ASSEMBLY = 33

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    PartType.__setattr__ = __enum_setattr
    PartType.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialContactRatioRatingForNVH")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_width_of_widest_cylindrical_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidthOfWidestCylindricalGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def largest_number_of_teeth(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LargestNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def mass_of_bearings(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassOfBearings")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mass_of_fe_part_housings(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassOfFEPartHousings")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mass_of_fe_part_shafts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassOfFEPartShafts")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mass_of_gears(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassOfGears")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mass_of_other_parts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassOfOtherParts")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mass_of_shafts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassOfShafts")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_tip_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumTipThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def smallest_number_of_teeth(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallestNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def transverse_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseContactRatioRatingForNVH"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_and_axial_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseAndAxialContactRatioRatingForNVH"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def oil_level_specification(self: "Self") -> "_2694.OilLevelSpecification":
        """mastapy.system_model.part_model.OilLevelSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilLevelSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bearings(self: "Self") -> "List[_2664.Bearing]":
        """List[mastapy.system_model.part_model.Bearing]

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
    def bolted_joints(self: "Self") -> "List[_2668.BoltedJoint]":
        """List[mastapy.system_model.part_model.BoltedJoint]

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
    def component_details(self: "Self") -> "List[_2670.Component]":
        """List[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def components_with_unknown_scalar_mass(self: "Self") -> "List[_2670.Component]":
        """List[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentsWithUnknownScalarMass")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def conical_gear_sets(self: "Self") -> "List[_2761.ConicalGearSet]":
        """List[mastapy.system_model.part_model.gears.ConicalGearSet]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_gear_sets(self: "Self") -> "List[_2763.CylindricalGearSet]":
        """List[mastapy.system_model.part_model.gears.CylindricalGearSet]

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
    def fe_parts(self: "Self") -> "List[_2680.FEPart]":
        """List[mastapy.system_model.part_model.FEPart]

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
    def face_gear_sets(self: "Self") -> "List[_2766.FaceGearSet]":
        """List[mastapy.system_model.part_model.gears.FaceGearSet]

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
    def gear_sets(self: "Self") -> "List[_2769.GearSet]":
        """List[mastapy.system_model.part_model.gears.GearSet]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def hypoid_gear_sets(self: "Self") -> "List[_2772.HypoidGearSet]":
        """List[mastapy.system_model.part_model.gears.HypoidGearSet]

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
    def klingelnberg_cyclo_palloid_gear_sets(
        self: "Self",
    ) -> "List[_2774.KlingelnbergCycloPalloidConicalGearSet]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KlingelnbergCycloPalloidGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def microphone_arrays(self: "Self") -> "List[_2692.MicrophoneArray]":
        """List[mastapy.system_model.part_model.MicrophoneArray]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicrophoneArrays")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def microphones(self: "Self") -> "List[_2691.Microphone]":
        """List[mastapy.system_model.part_model.Microphone]

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
    def oil_seals(self: "Self") -> "List[_2695.OilSeal]":
        """List[mastapy.system_model.part_model.OilSeal]

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
    def point_loads(self: "Self") -> "List[_2702.PointLoad]":
        """List[mastapy.system_model.part_model.PointLoad]

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
    def power_loads(self: "Self") -> "List[_2703.PowerLoad]":
        """List[mastapy.system_model.part_model.PowerLoad]

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
    def shaft_hub_connections(self: "Self") -> "List[_2840.ShaftHubConnection]":
        """List[mastapy.system_model.part_model.couplings.ShaftHubConnection]

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
    def shafts(self: "Self") -> "List[_2714.Shaft]":
        """List[mastapy.system_model.part_model.shaft_model.Shaft]

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
    def spiral_bevel_gear_sets(self: "Self") -> "List[_2782.SpiralBevelGearSet]":
        """List[mastapy.system_model.part_model.gears.SpiralBevelGearSet]

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
    def straight_bevel_gear_sets(self: "Self") -> "List[_2786.StraightBevelGearSet]":
        """List[mastapy.system_model.part_model.gears.StraightBevelGearSet]

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
    def worm_gear_sets(self: "Self") -> "List[_2790.WormGearSet]":
        """List[mastapy.system_model.part_model.gears.WormGearSet]

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

    @exception_bridge
    @enforce_parameter_types
    def get_part_named(self: "Self", name: "str") -> "_2698.Part":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_assembly(self: "Self", name: "str") -> "Assembly":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Assembly")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_abstract_assembly(
        self: "Self", name: "str"
    ) -> "_2659.AbstractAssembly":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "AbstractAssembly"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_abstract_shaft(
        self: "Self", name: "str"
    ) -> "_2660.AbstractShaft":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaft"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_abstract_shaft_or_housing(
        self: "Self", name: "str"
    ) -> "_2661.AbstractShaftOrHousing":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaftOrHousing"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_bearing(self: "Self", name: "str") -> "_2664.Bearing":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bearing")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_bolt(self: "Self", name: "str") -> "_2667.Bolt":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bolt")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_bolted_joint(
        self: "Self", name: "str"
    ) -> "_2668.BoltedJoint":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "BoltedJoint"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_component(
        self: "Self", name: "str"
    ) -> "_2670.Component":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_connector(
        self: "Self", name: "str"
    ) -> "_2673.Connector":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Connector")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_datum(self: "Self", name: "str") -> "_2674.Datum":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Datum")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_external_cad_model(
        self: "Self", name: "str"
    ) -> "_2679.ExternalCADModel":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "ExternalCADModel"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_fe_part(self: "Self", name: "str") -> "_2680.FEPart":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "FEPart")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_flexible_pin_assembly(
        self: "Self", name: "str"
    ) -> "_2681.FlexiblePinAssembly":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "FlexiblePinAssembly"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_guide_dxf_model(
        self: "Self", name: "str"
    ) -> "_2682.GuideDxfModel":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "GuideDxfModel"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_mass_disc(self: "Self", name: "str") -> "_2689.MassDisc":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "MassDisc")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_measurement_component(
        self: "Self", name: "str"
    ) -> "_2690.MeasurementComponent":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "MeasurementComponent"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_microphone(
        self: "Self", name: "str"
    ) -> "_2691.Microphone":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "Microphone"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_microphone_array(
        self: "Self", name: "str"
    ) -> "_2692.MicrophoneArray":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "MicrophoneArray"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_mountable_component(
        self: "Self", name: "str"
    ) -> "_2693.MountableComponent":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_oil_seal(self: "Self", name: "str") -> "_2695.OilSeal":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "OilSeal")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_part(self: "Self", name: "str") -> "_2698.Part":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_planet_carrier(
        self: "Self", name: "str"
    ) -> "_2700.PlanetCarrier":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "PlanetCarrier"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_point_load(
        self: "Self", name: "str"
    ) -> "_2702.PointLoad":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PointLoad")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_power_load(
        self: "Self", name: "str"
    ) -> "_2703.PowerLoad":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PowerLoad")
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_root_assembly(
        self: "Self", name: "str"
    ) -> "_2706.RootAssembly":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "RootAssembly"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_specialised_assembly(
        self: "Self", name: "str"
    ) -> "_2708.SpecialisedAssembly":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_unbalanced_mass(
        self: "Self", name: "str"
    ) -> "_2709.UnbalancedMass":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "UnbalancedMass"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_virtual_component(
        self: "Self", name: "str"
    ) -> "_2711.VirtualComponent":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_shaft(self: "Self", name: "str") -> "_2714.Shaft":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.ShaftModel", "Shaft"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_agma_gleason_conical_gear(
        self: "Self", name: "str"
    ) -> "_2750.AGMAGleasonConicalGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_agma_gleason_conical_gear_set(
        self: "Self", name: "str"
    ) -> "_2751.AGMAGleasonConicalGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_bevel_differential_gear(
        self: "Self", name: "str"
    ) -> "_2752.BevelDifferentialGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_bevel_differential_gear_set(
        self: "Self", name: "str"
    ) -> "_2753.BevelDifferentialGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_bevel_differential_planet_gear(
        self: "Self", name: "str"
    ) -> "_2754.BevelDifferentialPlanetGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialPlanetGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_bevel_differential_sun_gear(
        self: "Self", name: "str"
    ) -> "_2755.BevelDifferentialSunGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialSunGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_bevel_gear(
        self: "Self", name: "str"
    ) -> "_2756.BevelGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_bevel_gear_set(
        self: "Self", name: "str"
    ) -> "_2757.BevelGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_concept_gear(
        self: "Self", name: "str"
    ) -> "_2758.ConceptGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_concept_gear_set(
        self: "Self", name: "str"
    ) -> "_2759.ConceptGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_conical_gear(
        self: "Self", name: "str"
    ) -> "_2760.ConicalGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_conical_gear_set(
        self: "Self", name: "str"
    ) -> "_2761.ConicalGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_cylindrical_gear(
        self: "Self", name: "str"
    ) -> "_2762.CylindricalGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_cylindrical_gear_set(
        self: "Self", name: "str"
    ) -> "_2763.CylindricalGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_cylindrical_planet_gear(
        self: "Self", name: "str"
    ) -> "_2764.CylindricalPlanetGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalPlanetGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_face_gear(self: "Self", name: "str") -> "_2765.FaceGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_face_gear_set(
        self: "Self", name: "str"
    ) -> "_2766.FaceGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_gear(self: "Self", name: "str") -> "_2767.Gear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_gear_set(self: "Self", name: "str") -> "_2769.GearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_hypoid_gear(
        self: "Self", name: "str"
    ) -> "_2771.HypoidGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_hypoid_gear_set(
        self: "Self", name: "str"
    ) -> "_2772.HypoidGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_klingelnberg_cyclo_palloid_conical_gear(
        self: "Self", name: "str"
    ) -> "_2773.KlingelnbergCycloPalloidConicalGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidConicalGear",
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_klingelnberg_cyclo_palloid_conical_gear_set(
        self: "Self", name: "str"
    ) -> "_2774.KlingelnbergCycloPalloidConicalGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidConicalGearSet",
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_klingelnberg_cyclo_palloid_hypoid_gear(
        self: "Self", name: "str"
    ) -> "_2775.KlingelnbergCycloPalloidHypoidGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidHypoidGear",
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self", name: "str"
    ) -> "_2776.KlingelnbergCycloPalloidHypoidGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidHypoidGearSet",
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "Self", name: "str"
    ) -> "_2777.KlingelnbergCycloPalloidSpiralBevelGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidSpiralBevelGear",
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "Self", name: "str"
    ) -> "_2778.KlingelnbergCycloPalloidSpiralBevelGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidSpiralBevelGearSet",
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_planetary_gear_set(
        self: "Self", name: "str"
    ) -> "_2779.PlanetaryGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "PlanetaryGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_spiral_bevel_gear(
        self: "Self", name: "str"
    ) -> "_2781.SpiralBevelGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_spiral_bevel_gear_set(
        self: "Self", name: "str"
    ) -> "_2782.SpiralBevelGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_straight_bevel_diff_gear(
        self: "Self", name: "str"
    ) -> "_2783.StraightBevelDiffGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_straight_bevel_diff_gear_set(
        self: "Self", name: "str"
    ) -> "_2784.StraightBevelDiffGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_straight_bevel_gear(
        self: "Self", name: "str"
    ) -> "_2785.StraightBevelGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_straight_bevel_gear_set(
        self: "Self", name: "str"
    ) -> "_2786.StraightBevelGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_straight_bevel_planet_gear(
        self: "Self", name: "str"
    ) -> "_2787.StraightBevelPlanetGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelPlanetGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_straight_bevel_sun_gear(
        self: "Self", name: "str"
    ) -> "_2788.StraightBevelSunGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelSunGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_worm_gear(self: "Self", name: "str") -> "_2789.WormGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_worm_gear_set(
        self: "Self", name: "str"
    ) -> "_2790.WormGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_zerol_bevel_gear(
        self: "Self", name: "str"
    ) -> "_2791.ZerolBevelGear":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGear"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_zerol_bevel_gear_set(
        self: "Self", name: "str"
    ) -> "_2792.ZerolBevelGearSet":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGearSet"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_cycloidal_assembly(
        self: "Self", name: "str"
    ) -> "_2806.CycloidalAssembly":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalAssembly"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_cycloidal_disc(
        self: "Self", name: "str"
    ) -> "_2807.CycloidalDisc":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalDisc"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_ring_pins(self: "Self", name: "str") -> "_2808.RingPins":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "RingPins"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_belt_drive(
        self: "Self", name: "str"
    ) -> "_2815.BeltDrive":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDrive"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_clutch(self: "Self", name: "str") -> "_2817.Clutch":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Clutch"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_clutch_half(
        self: "Self", name: "str"
    ) -> "_2818.ClutchHalf":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ClutchHalf"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_concept_coupling(
        self: "Self", name: "str"
    ) -> "_2820.ConceptCoupling":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCoupling"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_concept_coupling_half(
        self: "Self", name: "str"
    ) -> "_2821.ConceptCouplingHalf":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCouplingHalf"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_coupling(self: "Self", name: "str") -> "_2823.Coupling":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Coupling"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_coupling_half(
        self: "Self", name: "str"
    ) -> "_2824.CouplingHalf":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_cvt(self: "Self", name: "str") -> "_2826.CVT":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVT"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_cvt_pulley(
        self: "Self", name: "str"
    ) -> "_2827.CVTPulley":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVTPulley"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_part_to_part_shear_coupling(
        self: "Self", name: "str"
    ) -> "_2828.PartToPartShearCoupling":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_part_to_part_shear_coupling_half(
        self: "Self", name: "str"
    ) -> "_2829.PartToPartShearCouplingHalf":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings",
            "PartToPartShearCouplingHalf",
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_pulley(self: "Self", name: "str") -> "_2831.Pulley":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Pulley"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_rolling_ring(
        self: "Self", name: "str"
    ) -> "_2838.RollingRing":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRing"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_rolling_ring_assembly(
        self: "Self", name: "str"
    ) -> "_2839.RollingRingAssembly":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRingAssembly"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_shaft_hub_connection(
        self: "Self", name: "str"
    ) -> "_2840.ShaftHubConnection":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ShaftHubConnection"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_spring_damper(
        self: "Self", name: "str"
    ) -> "_2846.SpringDamper":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_spring_damper_half(
        self: "Self", name: "str"
    ) -> "_2847.SpringDamperHalf":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamperHalf"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_synchroniser(
        self: "Self", name: "str"
    ) -> "_2848.Synchroniser":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Synchroniser"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_synchroniser_half(
        self: "Self", name: "str"
    ) -> "_2850.SynchroniserHalf":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserHalf"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_synchroniser_part(
        self: "Self", name: "str"
    ) -> "_2851.SynchroniserPart":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserPart"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_synchroniser_sleeve(
        self: "Self", name: "str"
    ) -> "_2852.SynchroniserSleeve":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserSleeve"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_torque_converter(
        self: "Self", name: "str"
    ) -> "_2853.TorqueConverter":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverter"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_torque_converter_pump(
        self: "Self", name: "str"
    ) -> "_2854.TorqueConverterPump":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterPump"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_part_named_of_type_torque_converter_turbine(
        self: "Self", name: "str"
    ) -> "_2856.TorqueConverterTurbine":
        """T_get_part_named

        Args:
            name (str)
        """
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterTurbine"
        )
        name = str(name)
        method_result = pythonnet_method_call_generic(
            self.wrapped, "GetPartNamed", cast_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_part(
        self: "Self", part_type: "Assembly.PartType", name: "str"
    ) -> "_2698.Part":
        """mastapy.system_model.part_model.Part

        Args:
            part_type (mastapy.system_model.part_model.Assembly.PartType)
            name (str)
        """
        part_type = conversion.mp_to_pn_enum(
            part_type, "SMT.MastaAPI.SystemModel.PartModel.Assembly+PartType"
        )
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddPart", part_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def all_parts(self: "Self") -> "List[_2698.Part]":
        """List[mastapy.system_model.part_model.Part]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_assembly(self: "Self") -> "List[Assembly]":
        """List[mastapy.system_model.part_model.Assembly]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Assembly")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_abstract_assembly(
        self: "Self",
    ) -> "List[_2659.AbstractAssembly]":
        """List[mastapy.system_model.part_model.AbstractAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "AbstractAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_abstract_shaft(self: "Self") -> "List[_2660.AbstractShaft]":
        """List[mastapy.system_model.part_model.AbstractShaft]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaft"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_abstract_shaft_or_housing(
        self: "Self",
    ) -> "List[_2661.AbstractShaftOrHousing]":
        """List[mastapy.system_model.part_model.AbstractShaftOrHousing]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaftOrHousing"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bearing(self: "Self") -> "List[_2664.Bearing]":
        """List[mastapy.system_model.part_model.Bearing]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bearing")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bolt(self: "Self") -> "List[_2667.Bolt]":
        """List[mastapy.system_model.part_model.Bolt]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bolt")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bolted_joint(self: "Self") -> "List[_2668.BoltedJoint]":
        """List[mastapy.system_model.part_model.BoltedJoint]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "BoltedJoint"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_component(self: "Self") -> "List[_2670.Component]":
        """List[mastapy.system_model.part_model.Component]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_connector(self: "Self") -> "List[_2673.Connector]":
        """List[mastapy.system_model.part_model.Connector]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Connector")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_datum(self: "Self") -> "List[_2674.Datum]":
        """List[mastapy.system_model.part_model.Datum]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Datum")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_external_cad_model(
        self: "Self",
    ) -> "List[_2679.ExternalCADModel]":
        """List[mastapy.system_model.part_model.ExternalCADModel]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "ExternalCADModel"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_fe_part(self: "Self") -> "List[_2680.FEPart]":
        """List[mastapy.system_model.part_model.FEPart]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "FEPart")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_flexible_pin_assembly(
        self: "Self",
    ) -> "List[_2681.FlexiblePinAssembly]":
        """List[mastapy.system_model.part_model.FlexiblePinAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "FlexiblePinAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_guide_dxf_model(self: "Self") -> "List[_2682.GuideDxfModel]":
        """List[mastapy.system_model.part_model.GuideDxfModel]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "GuideDxfModel"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_mass_disc(self: "Self") -> "List[_2689.MassDisc]":
        """List[mastapy.system_model.part_model.MassDisc]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "MassDisc")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_measurement_component(
        self: "Self",
    ) -> "List[_2690.MeasurementComponent]":
        """List[mastapy.system_model.part_model.MeasurementComponent]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "MeasurementComponent"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_microphone(self: "Self") -> "List[_2691.Microphone]":
        """List[mastapy.system_model.part_model.Microphone]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "Microphone"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_microphone_array(
        self: "Self",
    ) -> "List[_2692.MicrophoneArray]":
        """List[mastapy.system_model.part_model.MicrophoneArray]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "MicrophoneArray"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_mountable_component(
        self: "Self",
    ) -> "List[_2693.MountableComponent]":
        """List[mastapy.system_model.part_model.MountableComponent]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_oil_seal(self: "Self") -> "List[_2695.OilSeal]":
        """List[mastapy.system_model.part_model.OilSeal]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "OilSeal")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_part(self: "Self") -> "List[_2698.Part]":
        """List[mastapy.system_model.part_model.Part]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_planet_carrier(self: "Self") -> "List[_2700.PlanetCarrier]":
        """List[mastapy.system_model.part_model.PlanetCarrier]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "PlanetCarrier"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_point_load(self: "Self") -> "List[_2702.PointLoad]":
        """List[mastapy.system_model.part_model.PointLoad]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PointLoad")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_power_load(self: "Self") -> "List[_2703.PowerLoad]":
        """List[mastapy.system_model.part_model.PowerLoad]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PowerLoad")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_root_assembly(self: "Self") -> "List[_2706.RootAssembly]":
        """List[mastapy.system_model.part_model.RootAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "RootAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_specialised_assembly(
        self: "Self",
    ) -> "List[_2708.SpecialisedAssembly]":
        """List[mastapy.system_model.part_model.SpecialisedAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_unbalanced_mass(self: "Self") -> "List[_2709.UnbalancedMass]":
        """List[mastapy.system_model.part_model.UnbalancedMass]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "UnbalancedMass"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_virtual_component(
        self: "Self",
    ) -> "List[_2711.VirtualComponent]":
        """List[mastapy.system_model.part_model.VirtualComponent]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_shaft(self: "Self") -> "List[_2714.Shaft]":
        """List[mastapy.system_model.part_model.shaft_model.Shaft]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.ShaftModel", "Shaft"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_agma_gleason_conical_gear(
        self: "Self",
    ) -> "List[_2750.AGMAGleasonConicalGear]":
        """List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_agma_gleason_conical_gear_set(
        self: "Self",
    ) -> "List[_2751.AGMAGleasonConicalGearSet]":
        """List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_differential_gear(
        self: "Self",
    ) -> "List[_2752.BevelDifferentialGear]":
        """List[mastapy.system_model.part_model.gears.BevelDifferentialGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_differential_gear_set(
        self: "Self",
    ) -> "List[_2753.BevelDifferentialGearSet]":
        """List[mastapy.system_model.part_model.gears.BevelDifferentialGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_differential_planet_gear(
        self: "Self",
    ) -> "List[_2754.BevelDifferentialPlanetGear]":
        """List[mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialPlanetGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_differential_sun_gear(
        self: "Self",
    ) -> "List[_2755.BevelDifferentialSunGear]":
        """List[mastapy.system_model.part_model.gears.BevelDifferentialSunGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialSunGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_gear(self: "Self") -> "List[_2756.BevelGear]":
        """List[mastapy.system_model.part_model.gears.BevelGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_gear_set(self: "Self") -> "List[_2757.BevelGearSet]":
        """List[mastapy.system_model.part_model.gears.BevelGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_concept_gear(self: "Self") -> "List[_2758.ConceptGear]":
        """List[mastapy.system_model.part_model.gears.ConceptGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_concept_gear_set(
        self: "Self",
    ) -> "List[_2759.ConceptGearSet]":
        """List[mastapy.system_model.part_model.gears.ConceptGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_conical_gear(self: "Self") -> "List[_2760.ConicalGear]":
        """List[mastapy.system_model.part_model.gears.ConicalGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_conical_gear_set(
        self: "Self",
    ) -> "List[_2761.ConicalGearSet]":
        """List[mastapy.system_model.part_model.gears.ConicalGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cylindrical_gear(
        self: "Self",
    ) -> "List[_2762.CylindricalGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cylindrical_gear_set(
        self: "Self",
    ) -> "List[_2763.CylindricalGearSet]":
        """List[mastapy.system_model.part_model.gears.CylindricalGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cylindrical_planet_gear(
        self: "Self",
    ) -> "List[_2764.CylindricalPlanetGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalPlanetGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalPlanetGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_face_gear(self: "Self") -> "List[_2765.FaceGear]":
        """List[mastapy.system_model.part_model.gears.FaceGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_face_gear_set(self: "Self") -> "List[_2766.FaceGearSet]":
        """List[mastapy.system_model.part_model.gears.FaceGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_gear(self: "Self") -> "List[_2767.Gear]":
        """List[mastapy.system_model.part_model.gears.Gear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_gear_set(self: "Self") -> "List[_2769.GearSet]":
        """List[mastapy.system_model.part_model.gears.GearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_hypoid_gear(self: "Self") -> "List[_2771.HypoidGear]":
        """List[mastapy.system_model.part_model.gears.HypoidGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_hypoid_gear_set(self: "Self") -> "List[_2772.HypoidGearSet]":
        """List[mastapy.system_model.part_model.gears.HypoidGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear(
        self: "Self",
    ) -> "List[_2773.KlingelnbergCycloPalloidConicalGear]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidConicalGear",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear_set(
        self: "Self",
    ) -> "List[_2774.KlingelnbergCycloPalloidConicalGearSet]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidConicalGearSet",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear(
        self: "Self",
    ) -> "List[_2775.KlingelnbergCycloPalloidHypoidGear]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidHypoidGear",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self",
    ) -> "List[_2776.KlingelnbergCycloPalloidHypoidGearSet]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidHypoidGearSet",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "Self",
    ) -> "List[_2777.KlingelnbergCycloPalloidSpiralBevelGear]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidSpiralBevelGear",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "Self",
    ) -> "List[_2778.KlingelnbergCycloPalloidSpiralBevelGearSet]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidSpiralBevelGearSet",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_planetary_gear_set(
        self: "Self",
    ) -> "List[_2779.PlanetaryGearSet]":
        """List[mastapy.system_model.part_model.gears.PlanetaryGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "PlanetaryGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_spiral_bevel_gear(
        self: "Self",
    ) -> "List[_2781.SpiralBevelGear]":
        """List[mastapy.system_model.part_model.gears.SpiralBevelGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_spiral_bevel_gear_set(
        self: "Self",
    ) -> "List[_2782.SpiralBevelGearSet]":
        """List[mastapy.system_model.part_model.gears.SpiralBevelGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_diff_gear(
        self: "Self",
    ) -> "List[_2783.StraightBevelDiffGear]":
        """List[mastapy.system_model.part_model.gears.StraightBevelDiffGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_diff_gear_set(
        self: "Self",
    ) -> "List[_2784.StraightBevelDiffGearSet]":
        """List[mastapy.system_model.part_model.gears.StraightBevelDiffGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_gear(
        self: "Self",
    ) -> "List[_2785.StraightBevelGear]":
        """List[mastapy.system_model.part_model.gears.StraightBevelGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_gear_set(
        self: "Self",
    ) -> "List[_2786.StraightBevelGearSet]":
        """List[mastapy.system_model.part_model.gears.StraightBevelGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_planet_gear(
        self: "Self",
    ) -> "List[_2787.StraightBevelPlanetGear]":
        """List[mastapy.system_model.part_model.gears.StraightBevelPlanetGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelPlanetGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_sun_gear(
        self: "Self",
    ) -> "List[_2788.StraightBevelSunGear]":
        """List[mastapy.system_model.part_model.gears.StraightBevelSunGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelSunGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_worm_gear(self: "Self") -> "List[_2789.WormGear]":
        """List[mastapy.system_model.part_model.gears.WormGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_worm_gear_set(self: "Self") -> "List[_2790.WormGearSet]":
        """List[mastapy.system_model.part_model.gears.WormGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_zerol_bevel_gear(
        self: "Self",
    ) -> "List[_2791.ZerolBevelGear]":
        """List[mastapy.system_model.part_model.gears.ZerolBevelGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_zerol_bevel_gear_set(
        self: "Self",
    ) -> "List[_2792.ZerolBevelGearSet]":
        """List[mastapy.system_model.part_model.gears.ZerolBevelGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cycloidal_assembly(
        self: "Self",
    ) -> "List[_2806.CycloidalAssembly]":
        """List[mastapy.system_model.part_model.cycloidal.CycloidalAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cycloidal_disc(self: "Self") -> "List[_2807.CycloidalDisc]":
        """List[mastapy.system_model.part_model.cycloidal.CycloidalDisc]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalDisc"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_ring_pins(self: "Self") -> "List[_2808.RingPins]":
        """List[mastapy.system_model.part_model.cycloidal.RingPins]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "RingPins"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_belt_drive(self: "Self") -> "List[_2815.BeltDrive]":
        """List[mastapy.system_model.part_model.couplings.BeltDrive]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDrive"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_clutch(self: "Self") -> "List[_2817.Clutch]":
        """List[mastapy.system_model.part_model.couplings.Clutch]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Clutch"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_clutch_half(self: "Self") -> "List[_2818.ClutchHalf]":
        """List[mastapy.system_model.part_model.couplings.ClutchHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ClutchHalf"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_concept_coupling(
        self: "Self",
    ) -> "List[_2820.ConceptCoupling]":
        """List[mastapy.system_model.part_model.couplings.ConceptCoupling]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCoupling"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_concept_coupling_half(
        self: "Self",
    ) -> "List[_2821.ConceptCouplingHalf]":
        """List[mastapy.system_model.part_model.couplings.ConceptCouplingHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCouplingHalf"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_coupling(self: "Self") -> "List[_2823.Coupling]":
        """List[mastapy.system_model.part_model.couplings.Coupling]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Coupling"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_coupling_half(self: "Self") -> "List[_2824.CouplingHalf]":
        """List[mastapy.system_model.part_model.couplings.CouplingHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cvt(self: "Self") -> "List[_2826.CVT]":
        """List[mastapy.system_model.part_model.couplings.CVT]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVT"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cvt_pulley(self: "Self") -> "List[_2827.CVTPulley]":
        """List[mastapy.system_model.part_model.couplings.CVTPulley]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVTPulley"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_part_to_part_shear_coupling(
        self: "Self",
    ) -> "List[_2828.PartToPartShearCoupling]":
        """List[mastapy.system_model.part_model.couplings.PartToPartShearCoupling]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_part_to_part_shear_coupling_half(
        self: "Self",
    ) -> "List[_2829.PartToPartShearCouplingHalf]":
        """List[mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings",
            "PartToPartShearCouplingHalf",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_pulley(self: "Self") -> "List[_2831.Pulley]":
        """List[mastapy.system_model.part_model.couplings.Pulley]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Pulley"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_rolling_ring(self: "Self") -> "List[_2838.RollingRing]":
        """List[mastapy.system_model.part_model.couplings.RollingRing]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRing"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_rolling_ring_assembly(
        self: "Self",
    ) -> "List[_2839.RollingRingAssembly]":
        """List[mastapy.system_model.part_model.couplings.RollingRingAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRingAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_shaft_hub_connection(
        self: "Self",
    ) -> "List[_2840.ShaftHubConnection]":
        """List[mastapy.system_model.part_model.couplings.ShaftHubConnection]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ShaftHubConnection"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_spring_damper(self: "Self") -> "List[_2846.SpringDamper]":
        """List[mastapy.system_model.part_model.couplings.SpringDamper]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_spring_damper_half(
        self: "Self",
    ) -> "List[_2847.SpringDamperHalf]":
        """List[mastapy.system_model.part_model.couplings.SpringDamperHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamperHalf"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_synchroniser(self: "Self") -> "List[_2848.Synchroniser]":
        """List[mastapy.system_model.part_model.couplings.Synchroniser]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Synchroniser"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_synchroniser_half(
        self: "Self",
    ) -> "List[_2850.SynchroniserHalf]":
        """List[mastapy.system_model.part_model.couplings.SynchroniserHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserHalf"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_synchroniser_part(
        self: "Self",
    ) -> "List[_2851.SynchroniserPart]":
        """List[mastapy.system_model.part_model.couplings.SynchroniserPart]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserPart"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_synchroniser_sleeve(
        self: "Self",
    ) -> "List[_2852.SynchroniserSleeve]":
        """List[mastapy.system_model.part_model.couplings.SynchroniserSleeve]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserSleeve"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_torque_converter(
        self: "Self",
    ) -> "List[_2853.TorqueConverter]":
        """List[mastapy.system_model.part_model.couplings.TorqueConverter]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverter"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_torque_converter_pump(
        self: "Self",
    ) -> "List[_2854.TorqueConverterPump]":
        """List[mastapy.system_model.part_model.couplings.TorqueConverterPump]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterPump"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_torque_converter_turbine(
        self: "Self",
    ) -> "List[_2856.TorqueConverterTurbine]":
        """List[mastapy.system_model.part_model.couplings.TorqueConverterTurbine]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterTurbine"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    @enforce_parameter_types
    def add_assembly(self: "Self", name: "str" = "Assembly") -> "Assembly":
        """mastapy.system_model.part_model.Assembly

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddAssembly", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_axial_clearance_bearing(
        self: "Self", name: "str", contact_diameter: "float"
    ) -> "_2664.Bearing":
        """mastapy.system_model.part_model.Bearing

        Args:
            name (str)
            contact_diameter (float)
        """
        name = str(name)
        contact_diameter = float(contact_diameter)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddAxialClearanceBearing",
            name if name else "",
            contact_diameter if contact_diameter else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_bearing(self: "Self", name: "str") -> "_2664.Bearing":
        """mastapy.system_model.part_model.Bearing

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call_overload(
            self.wrapped, "AddBearing", [_STRING], name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_bearing_with_name_and_rolling_bearing_type(
        self: "Self", name: "str", type_: "_2099.RollingBearingType"
    ) -> "_2664.Bearing":
        """mastapy.system_model.part_model.Bearing

        Args:
            name (str)
            type_ (mastapy.bearings.RollingBearingType)
        """
        name = str(name)
        type_ = conversion.mp_to_pn_enum(
            type_, "SMT.MastaAPI.Bearings.RollingBearingType"
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddBearing",
            [_STRING, _ROLLING_BEARING_TYPE],
            name if name else "",
            type_,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_bearing_with_name_rolling_bearing_type_and_designation(
        self: "Self", name: "str", type_: "_2099.RollingBearingType", designation: "str"
    ) -> "_2664.Bearing":
        """mastapy.system_model.part_model.Bearing

        Args:
            name (str)
            type_ (mastapy.bearings.RollingBearingType)
            designation (str)
        """
        name = str(name)
        type_ = conversion.mp_to_pn_enum(
            type_, "SMT.MastaAPI.Bearings.RollingBearingType"
        )
        designation = str(designation)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddBearing",
            [_STRING, _ROLLING_BEARING_TYPE, _STRING],
            name if name else "",
            type_,
            designation if designation else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_belt_drive_with_options(
        self: "Self",
        belt_creation_options: Optional["_2809.BeltCreationOptions"] = None,
    ) -> "_2815.BeltDrive":
        """mastapy.system_model.part_model.couplings.BeltDrive

        Args:
            belt_creation_options (mastapy.system_model.part_model.creation_options.BeltCreationOptions, optional)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddBeltDrive",
            [_BELT_CREATION_OPTIONS],
            belt_creation_options.wrapped if belt_creation_options else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_belt_drive(
        self: "Self",
        centre_distance: "float" = 0.1,
        pulley_a_diameter: "float" = 0.08,
        pulley_b_diameter: "float" = 0.08,
        name: "str" = "Belt Drive",
    ) -> "_2815.BeltDrive":
        """mastapy.system_model.part_model.couplings.BeltDrive

        Args:
            centre_distance (float, optional)
            pulley_a_diameter (float, optional)
            pulley_b_diameter (float, optional)
            name (str, optional)
        """
        centre_distance = float(centre_distance)
        pulley_a_diameter = float(pulley_a_diameter)
        pulley_b_diameter = float(pulley_b_diameter)
        name = str(name)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddBeltDrive",
            [_DOUBLE, _DOUBLE, _DOUBLE, _STRING],
            centre_distance if centre_distance else 0.0,
            pulley_a_diameter if pulley_a_diameter else 0.0,
            pulley_b_diameter if pulley_b_diameter else 0.0,
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_bolted_joint(
        self: "Self", name: "str" = "Bolted Joint"
    ) -> "_2668.BoltedJoint":
        """mastapy.system_model.part_model.BoltedJoint

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddBoltedJoint", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_cvt(self: "Self", name: "str" = "CVT") -> "_2826.CVT":
        """mastapy.system_model.part_model.couplings.CVT

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddCVT", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_clutch(self: "Self", name: "str" = "Clutch") -> "_2817.Clutch":
        """mastapy.system_model.part_model.couplings.Clutch

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddClutch", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_concept_coupling(
        self: "Self", name: "str" = "Concept Coupling"
    ) -> "_2820.ConceptCoupling":
        """mastapy.system_model.part_model.couplings.ConceptCoupling

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddConceptCoupling", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_cycloidal_assembly_with_options(
        self: "Self",
        cycloidal_assembly_creation_options: Optional[
            "_2810.CycloidalAssemblyCreationOptions"
        ] = None,
    ) -> "_2806.CycloidalAssembly":
        """mastapy.system_model.part_model.cycloidal.CycloidalAssembly

        Args:
            cycloidal_assembly_creation_options (mastapy.system_model.part_model.creation_options.CycloidalAssemblyCreationOptions, optional)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddCycloidalAssembly",
            [_CYCLOIDAL_ASSEMBLY_CREATION_OPTIONS],
            cycloidal_assembly_creation_options.wrapped
            if cycloidal_assembly_creation_options
            else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_cycloidal_assembly(
        self: "Self",
        number_of_discs: "int" = 1,
        number_of_pins: "int" = 10,
        name: "str" = "Cycloidal Assembly",
    ) -> "_2806.CycloidalAssembly":
        """mastapy.system_model.part_model.cycloidal.CycloidalAssembly

        Args:
            number_of_discs (int, optional)
            number_of_pins (int, optional)
            name (str, optional)
        """
        number_of_discs = int(number_of_discs)
        number_of_pins = int(number_of_pins)
        name = str(name)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddCycloidalAssembly",
            [_INT_32, _INT_32, _STRING],
            number_of_discs if number_of_discs else 0,
            number_of_pins if number_of_pins else 0,
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_cylindrical_gear_pair_with_options(
        self: "Self",
        cylindrical_gear_pair_creation_options: Optional[
            "_1265.CylindricalGearPairCreationOptions"
        ] = None,
    ) -> "_2763.CylindricalGearSet":
        """mastapy.system_model.part_model.gears.CylindricalGearSet

        Args:
            cylindrical_gear_pair_creation_options (mastapy.gears.gear_designs.creation_options.CylindricalGearPairCreationOptions, optional)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddCylindricalGearPair",
            [_CYLINDRICAL_GEAR_PAIR_CREATION_OPTIONS],
            cylindrical_gear_pair_creation_options.wrapped
            if cylindrical_gear_pair_creation_options
            else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_cylindrical_gear_pair(
        self: "Self", centre_distance: "float"
    ) -> "_2763.CylindricalGearSet":
        """mastapy.system_model.part_model.gears.CylindricalGearSet

        Args:
            centre_distance (float)
        """
        centre_distance = float(centre_distance)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddCylindricalGearPair",
            [_DOUBLE],
            centre_distance if centre_distance else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_cylindrical_gear_set_with_options(
        self: "Self",
        cylindrical_gear_linear_train_creation_options: Optional[
            "_2811.CylindricalGearLinearTrainCreationOptions"
        ] = None,
    ) -> "_2763.CylindricalGearSet":
        """mastapy.system_model.part_model.gears.CylindricalGearSet

        Args:
            cylindrical_gear_linear_train_creation_options (mastapy.system_model.part_model.creation_options.CylindricalGearLinearTrainCreationOptions, optional)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddCylindricalGearSet",
            [_CYLINDRICAL_GEAR_LINEAR_TRAIN_CREATION_OPTIONS],
            cylindrical_gear_linear_train_creation_options.wrapped
            if cylindrical_gear_linear_train_creation_options
            else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_cylindrical_gear_set_extended(
        self: "Self",
        name: "str",
        normal_pressure_angle: "float",
        helix_angle: "float",
        normal_module: "float",
        pinion_hand: "_423.Hand",
        centre_distances: "List[float]",
    ) -> "_2763.CylindricalGearSet":
        """mastapy.system_model.part_model.gears.CylindricalGearSet

        Args:
            name (str)
            normal_pressure_angle (float)
            helix_angle (float)
            normal_module (float)
            pinion_hand (mastapy.gears.Hand)
            centre_distances (List[float])
        """
        name = str(name)
        normal_pressure_angle = float(normal_pressure_angle)
        helix_angle = float(helix_angle)
        normal_module = float(normal_module)
        pinion_hand = conversion.mp_to_pn_enum(pinion_hand, "SMT.MastaAPI.Gears.Hand")
        centre_distances = conversion.mp_to_pn_array_float(centre_distances)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddCylindricalGearSet",
            [_STRING, _DOUBLE, _DOUBLE, _DOUBLE, _HAND, _ARRAY[_DOUBLE]],
            name if name else "",
            normal_pressure_angle if normal_pressure_angle else 0.0,
            helix_angle if helix_angle else 0.0,
            normal_module if normal_module else 0.0,
            pinion_hand,
            centre_distances,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_cylindrical_gear_set(
        self: "Self", name: "str", centre_distances: "List[float]"
    ) -> "_2763.CylindricalGearSet":
        """mastapy.system_model.part_model.gears.CylindricalGearSet

        Args:
            name (str)
            centre_distances (List[float])
        """
        name = str(name)
        centre_distances = conversion.mp_to_pn_array_float(centre_distances)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddCylindricalGearSet",
            [_STRING, _ARRAY[_DOUBLE]],
            name if name else "",
            centre_distances,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_datum(self: "Self", name: "str" = "Datum") -> "_2674.Datum":
        """mastapy.system_model.part_model.Datum

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddDatum", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_fe_part(self: "Self", name: "str" = "FE Part") -> "_2680.FEPart":
        """mastapy.system_model.part_model.FEPart

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddFEPart", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_face_gear_set(
        self: "Self", name: "str" = "Face Gear Set"
    ) -> "_2766.FaceGearSet":
        """mastapy.system_model.part_model.gears.FaceGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddFaceGearSet", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_hypoid_gear_set(
        self: "Self", name: "str" = "Hypoid Gear Set"
    ) -> "_2772.HypoidGearSet":
        """mastapy.system_model.part_model.gears.HypoidGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call_overload(
            self.wrapped, "AddHypoidGearSet", [_STRING], name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_hypoid_gear_set_detailed(
        self: "Self",
        name: "str" = "Hypoid Gear Set",
        pinion_number_of_teeth: "int" = 7,
        wheel_number_of_teeth: "int" = 41,
        outer_transverse_module: "float" = 0.0109756,
        wheel_face_width: "float" = 0.072,
        offset: "float" = 0.045,
        average_pressure_angle: "float" = 0.3926991,
        design_method: "_1299.AGMAGleasonConicalGearGeometryMethods" = _1299.AGMAGleasonConicalGearGeometryMethods.GLEASON,
    ) -> "_2772.HypoidGearSet":
        """mastapy.system_model.part_model.gears.HypoidGearSet

        Args:
            name (str, optional)
            pinion_number_of_teeth (int, optional)
            wheel_number_of_teeth (int, optional)
            outer_transverse_module (float, optional)
            wheel_face_width (float, optional)
            offset (float, optional)
            average_pressure_angle (float, optional)
            design_method (mastapy.gears.gear_designs.bevel.AGMAGleasonConicalGearGeometryMethods, optional)
        """
        name = str(name)
        pinion_number_of_teeth = int(pinion_number_of_teeth)
        wheel_number_of_teeth = int(wheel_number_of_teeth)
        outer_transverse_module = float(outer_transverse_module)
        wheel_face_width = float(wheel_face_width)
        offset = float(offset)
        average_pressure_angle = float(average_pressure_angle)
        design_method = conversion.mp_to_pn_enum(
            design_method,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.AGMAGleasonConicalGearGeometryMethods",
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddHypoidGearSet",
            [
                _STRING,
                _INT_32,
                _INT_32,
                _DOUBLE,
                _DOUBLE,
                _DOUBLE,
                _DOUBLE,
                _AGMA_GLEASON_CONICAL_GEAR_GEOMETRY_METHODS,
            ],
            name if name else "",
            pinion_number_of_teeth if pinion_number_of_teeth else 0,
            wheel_number_of_teeth if wheel_number_of_teeth else 0,
            outer_transverse_module if outer_transverse_module else 0.0,
            wheel_face_width if wheel_face_width else 0.0,
            offset if offset else 0.0,
            average_pressure_angle if average_pressure_angle else 0.0,
            design_method,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self", name: "str" = "Klingelnberg Cyclo Palloid Hypoid Gear Set"
    ) -> "_2776.KlingelnbergCycloPalloidHypoidGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddKlingelnbergCycloPalloidHypoidGearSet",
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "Self", name: "str" = "Klingelnberg Cyclo Palloid Spiral Bevel Gear Set"
    ) -> "_2778.KlingelnbergCycloPalloidSpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddKlingelnbergCycloPalloidSpiralBevelGearSet",
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_linear_bearing(
        self: "Self", name: "str", width: "float"
    ) -> "_2664.Bearing":
        """mastapy.system_model.part_model.Bearing

        Args:
            name (str)
            width (float)
        """
        name = str(name)
        width = float(width)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddLinearBearing",
            name if name else "",
            width if width else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_mass_disc(self: "Self", name: "str" = "Mass Disc") -> "_2689.MassDisc":
        """mastapy.system_model.part_model.MassDisc

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddMassDisc", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_measurement_component(
        self: "Self", name: "str" = "Measurement Component"
    ) -> "_2690.MeasurementComponent":
        """mastapy.system_model.part_model.MeasurementComponent

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddMeasurementComponent", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_microphone_array(
        self: "Self", name: "str" = "Microphone Array"
    ) -> "_2692.MicrophoneArray":
        """mastapy.system_model.part_model.MicrophoneArray

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddMicrophoneArray", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_oil_seal(self: "Self", name: "str" = "Oil Seal") -> "_2695.OilSeal":
        """mastapy.system_model.part_model.OilSeal

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddOilSeal", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_planet_carrier_with_options(
        self: "Self",
        planet_carrier_creation_options: Optional[
            "_2813.PlanetCarrierCreationOptions"
        ] = None,
    ) -> "_2700.PlanetCarrier":
        """mastapy.system_model.part_model.PlanetCarrier

        Args:
            planet_carrier_creation_options (mastapy.system_model.part_model.creation_options.PlanetCarrierCreationOptions, optional)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddPlanetCarrier",
            [_PLANET_CARRIER_CREATION_OPTIONS],
            planet_carrier_creation_options.wrapped
            if planet_carrier_creation_options
            else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_planet_carrier(
        self: "Self", number_of_planets: "int" = 3, diameter: "float" = 0.05
    ) -> "_2700.PlanetCarrier":
        """mastapy.system_model.part_model.PlanetCarrier

        Args:
            number_of_planets (int, optional)
            diameter (float, optional)
        """
        number_of_planets = int(number_of_planets)
        diameter = float(diameter)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddPlanetCarrier",
            [_INT_32, _DOUBLE],
            number_of_planets if number_of_planets else 0,
            diameter if diameter else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_planetary_gear_set(
        self: "Self", name: "str" = "Planetary Gear Set"
    ) -> "_2779.PlanetaryGearSet":
        """mastapy.system_model.part_model.gears.PlanetaryGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddPlanetaryGearSet", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_point_load(self: "Self", name: "str" = "Point Load") -> "_2702.PointLoad":
        """mastapy.system_model.part_model.PointLoad

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddPointLoad", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_power_load(self: "Self", name: "str" = "Power Load") -> "_2703.PowerLoad":
        """mastapy.system_model.part_model.PowerLoad

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddPowerLoad", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_rolling_bearing_from_catalogue(
        self: "Self", catalogue: "_2072.BearingCatalog", designation: "str", name: "str"
    ) -> "_2664.Bearing":
        """mastapy.system_model.part_model.Bearing

        Args:
            catalogue (mastapy.bearings.BearingCatalog)
            designation (str)
            name (str)
        """
        catalogue = conversion.mp_to_pn_enum(
            catalogue, "SMT.MastaAPI.Bearings.BearingCatalog"
        )
        designation = str(designation)
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddRollingBearingFromCatalogue",
            catalogue,
            designation if designation else "",
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_rolling_ring(
        self: "Self", name: "str" = "Rolling Ring"
    ) -> "_2838.RollingRing":
        """mastapy.system_model.part_model.couplings.RollingRing

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddRollingRing", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_shaft_with_options(
        self: "Self", shaft_creation_options: "_2814.ShaftCreationOptions"
    ) -> "_2714.Shaft":
        """mastapy.system_model.part_model.shaft_model.Shaft

        Args:
            shaft_creation_options (mastapy.system_model.part_model.creation_options.ShaftCreationOptions)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddShaft",
            [_SHAFT_CREATION_OPTIONS],
            shaft_creation_options.wrapped if shaft_creation_options else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_shaft(
        self: "Self",
        length: "float" = 0.1,
        outer_diameter: "float" = 0.025,
        bore: "float" = 0.0,
        name: "str" = "Shaft",
    ) -> "_2714.Shaft":
        """mastapy.system_model.part_model.shaft_model.Shaft

        Args:
            length (float, optional)
            outer_diameter (float, optional)
            bore (float, optional)
            name (str, optional)
        """
        length = float(length)
        outer_diameter = float(outer_diameter)
        bore = float(bore)
        name = str(name)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddShaft",
            [_DOUBLE, _DOUBLE, _DOUBLE, _STRING],
            length if length else 0.0,
            outer_diameter if outer_diameter else 0.0,
            bore if bore else 0.0,
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_spiral_bevel_differential_gear_set(
        self: "Self", name: "str" = "Spiral Bevel Differential Gear Set"
    ) -> "_2753.BevelDifferentialGearSet":
        """mastapy.system_model.part_model.gears.BevelDifferentialGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddSpiralBevelDifferentialGearSet", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_spiral_bevel_gear_set_with_options(
        self: "Self",
        spiral_bevel_gear_set_creation_options: Optional[
            "_1269.SpiralBevelGearSetCreationOptions"
        ] = None,
    ) -> "_2782.SpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.SpiralBevelGearSet

        Args:
            spiral_bevel_gear_set_creation_options (mastapy.gears.gear_designs.creation_options.SpiralBevelGearSetCreationOptions, optional)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddSpiralBevelGearSet",
            [_SPIRAL_BEVEL_GEAR_SET_CREATION_OPTIONS],
            spiral_bevel_gear_set_creation_options.wrapped
            if spiral_bevel_gear_set_creation_options
            else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_spiral_bevel_gear_set(
        self: "Self", name: "str" = "Spiral Bevel Gear Set"
    ) -> "_2782.SpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.SpiralBevelGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call_overload(
            self.wrapped, "AddSpiralBevelGearSet", [_STRING], name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_spiral_bevel_gear_set_detailed(
        self: "Self",
        name: "str" = "Spiral Bevel Gear Set",
        outer_transverse_module: "float" = 0.00635,
        pressure_angle: "float" = 0.02,
        mean_spiral_angle: "float" = 0.523599,
        wheel_number_of_teeth: "int" = 43,
        pinion_number_of_teeth: "int" = 14,
        wheel_face_width: "float" = 0.02,
        pinion_face_width: "float" = 0.02,
        pinion_face_width_offset: "float" = 0.0,
        shaft_angle: "float" = 1.5708,
    ) -> "_2782.SpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.SpiralBevelGearSet

        Args:
            name (str, optional)
            outer_transverse_module (float, optional)
            pressure_angle (float, optional)
            mean_spiral_angle (float, optional)
            wheel_number_of_teeth (int, optional)
            pinion_number_of_teeth (int, optional)
            wheel_face_width (float, optional)
            pinion_face_width (float, optional)
            pinion_face_width_offset (float, optional)
            shaft_angle (float, optional)
        """
        name = str(name)
        outer_transverse_module = float(outer_transverse_module)
        pressure_angle = float(pressure_angle)
        mean_spiral_angle = float(mean_spiral_angle)
        wheel_number_of_teeth = int(wheel_number_of_teeth)
        pinion_number_of_teeth = int(pinion_number_of_teeth)
        wheel_face_width = float(wheel_face_width)
        pinion_face_width = float(pinion_face_width)
        pinion_face_width_offset = float(pinion_face_width_offset)
        shaft_angle = float(shaft_angle)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "AddSpiralBevelGearSet",
            [
                _STRING,
                _DOUBLE,
                _DOUBLE,
                _DOUBLE,
                _INT_32,
                _INT_32,
                _DOUBLE,
                _DOUBLE,
                _DOUBLE,
                _DOUBLE,
            ],
            name if name else "",
            outer_transverse_module if outer_transverse_module else 0.0,
            pressure_angle if pressure_angle else 0.0,
            mean_spiral_angle if mean_spiral_angle else 0.0,
            wheel_number_of_teeth if wheel_number_of_teeth else 0,
            pinion_number_of_teeth if pinion_number_of_teeth else 0,
            wheel_face_width if wheel_face_width else 0.0,
            pinion_face_width if pinion_face_width else 0.0,
            pinion_face_width_offset if pinion_face_width_offset else 0.0,
            shaft_angle if shaft_angle else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_spring_damper(
        self: "Self", name: "str" = "Spring Damper"
    ) -> "_2846.SpringDamper":
        """mastapy.system_model.part_model.couplings.SpringDamper

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddSpringDamper", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_straight_bevel_differential_gear_set(
        self: "Self", name: "str" = "Straight Bevel Differential Gear Set"
    ) -> "_2784.StraightBevelDiffGearSet":
        """mastapy.system_model.part_model.gears.StraightBevelDiffGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddStraightBevelDifferentialGearSet", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_straight_bevel_gear_set(
        self: "Self", name: "str" = "Straight Bevel Gear Set"
    ) -> "_2786.StraightBevelGearSet":
        """mastapy.system_model.part_model.gears.StraightBevelGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddStraightBevelGearSet", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_synchroniser(
        self: "Self", name: "str" = "Synchroniser"
    ) -> "_2848.Synchroniser":
        """mastapy.system_model.part_model.couplings.Synchroniser

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddSynchroniser", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_torque_converter(
        self: "Self", name: "str" = "Torque Converter"
    ) -> "_2853.TorqueConverter":
        """mastapy.system_model.part_model.couplings.TorqueConverter

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddTorqueConverter", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_unbalanced_mass(
        self: "Self", name: "str" = "Unbalanced Mass"
    ) -> "_2709.UnbalancedMass":
        """mastapy.system_model.part_model.UnbalancedMass

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddUnbalancedMass", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_worm_gear_set(
        self: "Self", name: "str" = "Worm Gear Set"
    ) -> "_2790.WormGearSet":
        """mastapy.system_model.part_model.gears.WormGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddWormGearSet", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_zerol_bevel_differential_gear_set(
        self: "Self", name: "str" = "Zerol Bevel Differential Gear Set"
    ) -> "_2753.BevelDifferentialGearSet":
        """mastapy.system_model.part_model.gears.BevelDifferentialGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddZerolBevelDifferentialGearSet", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_zerol_bevel_gear_set(
        self: "Self", name: "str" = "Zerol Bevel Gear Set"
    ) -> "_2792.ZerolBevelGearSet":
        """mastapy.system_model.part_model.gears.ZerolBevelGearSet

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddZerolBevelGearSet", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_differential(
        self: "Self", settings: "_1266.DifferentialAssemblyCreationOptions"
    ) -> "Assembly":
        """mastapy.system_model.part_model.Assembly

        Args:
            settings (mastapy.gears.gear_designs.creation_options.DifferentialAssemblyCreationOptions)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "AddDifferential", settings.wrapped if settings else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_shaft_hub_connection(
        self: "Self", name: "str"
    ) -> "_2840.ShaftHubConnection":
        """mastapy.system_model.part_model.couplings.ShaftHubConnection

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddShaftHubConnection", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def import_fe_mesh_from_file(
        self: "Self", file_name: "PathLike", stiffness_matrix: "_82.NodalMatrix"
    ) -> "_2680.FEPart":
        """mastapy.system_model.part_model.FEPart

        Args:
            file_name (PathLike)
            stiffness_matrix (mastapy.nodal_analysis.NodalMatrix)
        """
        file_name = str(file_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "ImportFEMeshFromFile",
            file_name,
            stiffness_matrix.wrapped if stiffness_matrix else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Assembly":
        """Cast to another type.

        Returns:
            _Cast_Assembly
        """
        return _Cast_Assembly(self)
