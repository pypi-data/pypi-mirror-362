"""GearMeshDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _1052

_GEAR_MESH_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns", "GearMeshDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1051
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1314
    from mastapy._private.gears.gear_designs.bevel import _1301
    from mastapy._private.gears.gear_designs.concept import _1297
    from mastapy._private.gears.gear_designs.conical import _1275
    from mastapy._private.gears.gear_designs.cylindrical import _1128
    from mastapy._private.gears.gear_designs.face import _1095
    from mastapy._private.gears.gear_designs.hypoid import _1090
    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1086
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1082
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1078
    from mastapy._private.gears.gear_designs.spiral_bevel import _1074
    from mastapy._private.gears.gear_designs.straight_bevel import _1066
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _1070
    from mastapy._private.gears.gear_designs.worm import _1062
    from mastapy._private.gears.gear_designs.zerol_bevel import _1057

    Self = TypeVar("Self", bound="GearMeshDesign")
    CastSelf = TypeVar("CastSelf", bound="GearMeshDesign._Cast_GearMeshDesign")


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshDesign:
    """Special nested class for casting GearMeshDesign to subclasses."""

    __parent__: "GearMeshDesign"

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def zerol_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1057.ZerolBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1057

        return self.__parent__._cast(_1057.ZerolBevelGearMeshDesign)

    @property
    def worm_gear_mesh_design(self: "CastSelf") -> "_1062.WormGearMeshDesign":
        from mastapy._private.gears.gear_designs.worm import _1062

        return self.__parent__._cast(_1062.WormGearMeshDesign)

    @property
    def straight_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1066.StraightBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1066

        return self.__parent__._cast(_1066.StraightBevelGearMeshDesign)

    @property
    def straight_bevel_diff_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1070.StraightBevelDiffGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1070

        return self.__parent__._cast(_1070.StraightBevelDiffGearMeshDesign)

    @property
    def spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1074.SpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1074

        return self.__parent__._cast(_1074.SpiralBevelGearMeshDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1078.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1078

        return self.__parent__._cast(
            _1078.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1082.KlingelnbergCycloPalloidHypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1082

        return self.__parent__._cast(_1082.KlingelnbergCycloPalloidHypoidGearMeshDesign)

    @property
    def klingelnberg_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1086.KlingelnbergConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1086

        return self.__parent__._cast(_1086.KlingelnbergConicalGearMeshDesign)

    @property
    def hypoid_gear_mesh_design(self: "CastSelf") -> "_1090.HypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1090

        return self.__parent__._cast(_1090.HypoidGearMeshDesign)

    @property
    def face_gear_mesh_design(self: "CastSelf") -> "_1095.FaceGearMeshDesign":
        from mastapy._private.gears.gear_designs.face import _1095

        return self.__parent__._cast(_1095.FaceGearMeshDesign)

    @property
    def cylindrical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1128.CylindricalGearMeshDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1128

        return self.__parent__._cast(_1128.CylindricalGearMeshDesign)

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "_1275.ConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.conical import _1275

        return self.__parent__._cast(_1275.ConicalGearMeshDesign)

    @property
    def concept_gear_mesh_design(self: "CastSelf") -> "_1297.ConceptGearMeshDesign":
        from mastapy._private.gears.gear_designs.concept import _1297

        return self.__parent__._cast(_1297.ConceptGearMeshDesign)

    @property
    def bevel_gear_mesh_design(self: "CastSelf") -> "_1301.BevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.bevel import _1301

        return self.__parent__._cast(_1301.BevelGearMeshDesign)

    @property
    def agma_gleason_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1314.AGMAGleasonConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1314

        return self.__parent__._cast(_1314.AGMAGleasonConicalGearMeshDesign)

    @property
    def gear_mesh_design(self: "CastSelf") -> "GearMeshDesign":
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
class GearMeshDesign(_1052.GearDesignComponent):
    """GearMeshDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_DESIGN

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
    def has_hunting_ratio(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasHuntingRatio")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def highest_common_factor_of_teeth_numbers(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HighestCommonFactorOfTeethNumbers")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def speed_ratio_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedRatioAToB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_ratio_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueRatioAToB")

        if temp is None:
            return 0.0

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
    def gear_a(self: "Self") -> "_1051.GearDesign":
        """mastapy.gears.gear_designs.GearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_b(self: "Self") -> "_1051.GearDesign":
        """mastapy.gears.gear_designs.GearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshDesign":
        """Cast to another type.

        Returns:
            _Cast_GearMeshDesign
        """
        return _Cast_GearMeshDesign(self)
