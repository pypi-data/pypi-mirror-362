"""GearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _1052

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_GEAR_SET_DESIGN = python_net_import("SMT.MastaAPI.Gears.GearDesigns", "GearSetDesign")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _417
    from mastapy._private.gears.fe_model import _1320
    from mastapy._private.gears.gear_designs import _1051
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1315
    from mastapy._private.gears.gear_designs.bevel import _1302
    from mastapy._private.gears.gear_designs.concept import _1298
    from mastapy._private.gears.gear_designs.conical import _1276
    from mastapy._private.gears.gear_designs.cylindrical import _1138, _1151
    from mastapy._private.gears.gear_designs.face import _1099
    from mastapy._private.gears.gear_designs.hypoid import _1091
    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1087
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1083
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1079
    from mastapy._private.gears.gear_designs.spiral_bevel import _1075
    from mastapy._private.gears.gear_designs.straight_bevel import _1067
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _1071
    from mastapy._private.gears.gear_designs.worm import _1063
    from mastapy._private.gears.gear_designs.zerol_bevel import _1058

    Self = TypeVar("Self", bound="GearSetDesign")
    CastSelf = TypeVar("CastSelf", bound="GearSetDesign._Cast_GearSetDesign")


__docformat__ = "restructuredtext en"
__all__ = ("GearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetDesign:
    """Special nested class for casting GearSetDesign to subclasses."""

    __parent__: "GearSetDesign"

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def zerol_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1058.ZerolBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1058

        return self.__parent__._cast(_1058.ZerolBevelGearSetDesign)

    @property
    def worm_gear_set_design(self: "CastSelf") -> "_1063.WormGearSetDesign":
        from mastapy._private.gears.gear_designs.worm import _1063

        return self.__parent__._cast(_1063.WormGearSetDesign)

    @property
    def straight_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1067.StraightBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1067

        return self.__parent__._cast(_1067.StraightBevelGearSetDesign)

    @property
    def straight_bevel_diff_gear_set_design(
        self: "CastSelf",
    ) -> "_1071.StraightBevelDiffGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1071

        return self.__parent__._cast(_1071.StraightBevelDiffGearSetDesign)

    @property
    def spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1075.SpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1075

        return self.__parent__._cast(_1075.SpiralBevelGearSetDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1079.KlingelnbergCycloPalloidSpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1079

        return self.__parent__._cast(
            _1079.KlingelnbergCycloPalloidSpiralBevelGearSetDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_design(
        self: "CastSelf",
    ) -> "_1083.KlingelnbergCycloPalloidHypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1083

        return self.__parent__._cast(_1083.KlingelnbergCycloPalloidHypoidGearSetDesign)

    @property
    def klingelnberg_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1087.KlingelnbergConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1087

        return self.__parent__._cast(_1087.KlingelnbergConicalGearSetDesign)

    @property
    def hypoid_gear_set_design(self: "CastSelf") -> "_1091.HypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1091

        return self.__parent__._cast(_1091.HypoidGearSetDesign)

    @property
    def face_gear_set_design(self: "CastSelf") -> "_1099.FaceGearSetDesign":
        from mastapy._private.gears.gear_designs.face import _1099

        return self.__parent__._cast(_1099.FaceGearSetDesign)

    @property
    def cylindrical_gear_set_design(
        self: "CastSelf",
    ) -> "_1138.CylindricalGearSetDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1138

        return self.__parent__._cast(_1138.CylindricalGearSetDesign)

    @property
    def cylindrical_planetary_gear_set_design(
        self: "CastSelf",
    ) -> "_1151.CylindricalPlanetaryGearSetDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1151

        return self.__parent__._cast(_1151.CylindricalPlanetaryGearSetDesign)

    @property
    def conical_gear_set_design(self: "CastSelf") -> "_1276.ConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.conical import _1276

        return self.__parent__._cast(_1276.ConicalGearSetDesign)

    @property
    def concept_gear_set_design(self: "CastSelf") -> "_1298.ConceptGearSetDesign":
        from mastapy._private.gears.gear_designs.concept import _1298

        return self.__parent__._cast(_1298.ConceptGearSetDesign)

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "_1302.BevelGearSetDesign":
        from mastapy._private.gears.gear_designs.bevel import _1302

        return self.__parent__._cast(_1302.BevelGearSetDesign)

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1315.AGMAGleasonConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1315

        return self.__parent__._cast(_1315.AGMAGleasonConicalGearSetDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "GearSetDesign":
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
class GearSetDesign(_1052.GearDesignComponent):
    """GearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_DESIGN

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
    def fe_model(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "FEModel", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @fe_model.setter
    @exception_bridge
    @enforce_parameter_types
    def fe_model(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "FEModel",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def gear_set_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def has_errors_or_warnings(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasErrorsOrWarnings")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def largest_mesh_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LargestMeshRatio")

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
    def long_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LongName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name_including_tooth_numbers(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NameIncludingToothNumbers")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def required_safety_factor_for_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RequiredSafetyFactorForBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def required_safety_factor_for_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RequiredSafetyFactorForContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def required_safety_factor_for_static_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForStaticBending"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def required_safety_factor_for_static_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForStaticContact"
        )

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
    def use_script_to_provide_mesh_efficiency(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseScriptToProvideMeshEfficiency")

        if temp is None:
            return False

        return temp

    @use_script_to_provide_mesh_efficiency.setter
    @exception_bridge
    @enforce_parameter_types
    def use_script_to_provide_mesh_efficiency(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseScriptToProvideMeshEfficiency",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def active_ltcafe_model(self: "Self") -> "_1320.GearSetFEModel":
        """mastapy.gears.fe_model.GearSetFEModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveLTCAFEModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def tifffe_model(self: "Self") -> "_1320.GearSetFEModel":
        """mastapy.gears.fe_model.GearSetFEModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TIFFFEModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def transmission_properties_gears(self: "Self") -> "_417.GearSetDesignGroup":
        """mastapy.gears.GearSetDesignGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmissionPropertiesGears")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gears(self: "Self") -> "List[_1051.GearDesign]":
        """List[mastapy.gears.gear_designs.GearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def ltcafe_models(self: "Self") -> "List[_1320.GearSetFEModel]":
        """List[mastapy.gears.fe_model.GearSetFEModel]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LTCAFEModels")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def create_new_tifffe_model(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateNewTIFFFEModel")

    @exception_bridge
    def create_new_fe_model(self: "Self") -> "_1320.GearSetFEModel":
        """mastapy.gears.fe_model.GearSetFEModel"""
        method_result = pythonnet_method_call(self.wrapped, "CreateNewFEModel")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def copy(self: "Self", include_fe: "bool" = False) -> "GearSetDesign":
        """mastapy.gears.gear_designs.GearSetDesign

        Args:
            include_fe (bool, optional)
        """
        include_fe = bool(include_fe)
        method_result = pythonnet_method_call(
            self.wrapped, "Copy", include_fe if include_fe else False
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_GearSetDesign
        """
        return _Cast_GearSetDesign(self)
