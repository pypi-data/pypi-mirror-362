"""CylindricalGearBasicRack"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1116

_CYLINDRICAL_GEAR_BASIC_RACK = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearBasicRack"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import (
        _1104,
        _1133,
        _1189,
        _1194,
    )

    Self = TypeVar("Self", bound="CylindricalGearBasicRack")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearBasicRack._Cast_CylindricalGearBasicRack"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearBasicRack",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearBasicRack:
    """Special nested class for casting CylindricalGearBasicRack to subclasses."""

    __parent__: "CylindricalGearBasicRack"

    @property
    def cylindrical_gear_abstract_rack(
        self: "CastSelf",
    ) -> "_1116.CylindricalGearAbstractRack":
        return self.__parent__._cast(_1116.CylindricalGearAbstractRack)

    @property
    def standard_rack(self: "CastSelf") -> "_1189.StandardRack":
        from mastapy._private.gears.gear_designs.cylindrical import _1189

        return self.__parent__._cast(_1189.StandardRack)

    @property
    def cylindrical_gear_basic_rack(self: "CastSelf") -> "CylindricalGearBasicRack":
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
class CylindricalGearBasicRack(_1116.CylindricalGearAbstractRack):
    """CylindricalGearBasicRack

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_BASIC_RACK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def basic_rack_clearance_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRackClearanceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rack_profile(self: "Self") -> "_1104.BasicRackProfiles":
        """mastapy.gears.gear_designs.cylindrical.BasicRackProfiles"""
        temp = pythonnet_property_get(self.wrapped, "BasicRackProfile")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.BasicRackProfiles"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1104", "BasicRackProfiles"
        )(value)

    @basic_rack_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def basic_rack_profile(self: "Self", value: "_1104.BasicRackProfiles") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.BasicRackProfiles"
        )
        pythonnet_property_set(self.wrapped, "BasicRackProfile", value)

    @property
    @exception_bridge
    def proportional_method_for_tip_clearance(
        self: "Self",
    ) -> "_1194.TipAlterationCoefficientMethod":
        """mastapy.gears.gear_designs.cylindrical.TipAlterationCoefficientMethod"""
        temp = pythonnet_property_get(self.wrapped, "ProportionalMethodForTipClearance")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.TipAlterationCoefficientMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1194",
            "TipAlterationCoefficientMethod",
        )(value)

    @proportional_method_for_tip_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def proportional_method_for_tip_clearance(
        self: "Self", value: "_1194.TipAlterationCoefficientMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.TipAlterationCoefficientMethod",
        )
        pythonnet_property_set(self.wrapped, "ProportionalMethodForTipClearance", value)

    @property
    @exception_bridge
    def tip_alteration_proportional_method_mesh(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(
            self.wrapped, "TipAlterationProportionalMethodMesh"
        )

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @tip_alteration_proportional_method_mesh.setter
    @exception_bridge
    @enforce_parameter_types
    def tip_alteration_proportional_method_mesh(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(
            self.wrapped, "TipAlterationProportionalMethodMesh", value
        )

    @property
    @exception_bridge
    def pinion_type_cutter_for_rating(
        self: "Self",
    ) -> "_1133.CylindricalGearPinionTypeCutter":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearPinionTypeCutter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionTypeCutterForRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearBasicRack":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearBasicRack
        """
        return _Cast_CylindricalGearBasicRack(self)
