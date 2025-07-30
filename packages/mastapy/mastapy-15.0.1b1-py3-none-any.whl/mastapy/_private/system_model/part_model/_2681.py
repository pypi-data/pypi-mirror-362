"""FlexiblePinAssembly"""

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
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2708

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_FLEXIBLE_PIN_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "FlexiblePinAssembly"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2659, _2698
    from mastapy._private.system_model.part_model.gears import _2762

    Self = TypeVar("Self", bound="FlexiblePinAssembly")
    CastSelf = TypeVar(
        "CastSelf", bound="FlexiblePinAssembly._Cast_FlexiblePinAssembly"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FlexiblePinAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlexiblePinAssembly:
    """Special nested class for casting FlexiblePinAssembly to subclasses."""

    __parent__: "FlexiblePinAssembly"

    @property
    def specialised_assembly(self: "CastSelf") -> "_2708.SpecialisedAssembly":
        return self.__parent__._cast(_2708.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2659

        return self.__parent__._cast(_2659.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "FlexiblePinAssembly":
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
class FlexiblePinAssembly(_2708.SpecialisedAssembly):
    """FlexiblePinAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLEXIBLE_PIN_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def length_to_diameter_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthToDiameterRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "Material", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @material.setter
    @exception_bridge
    @enforce_parameter_types
    def material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "Material",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def maximum_pin_diameter_from_planet_bore(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPinDiameterFromPlanetBore")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_fatigue_safety_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumFatigueSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @minimum_fatigue_safety_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_fatigue_safety_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumFatigueSafetyFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pin_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinDiameter")

        if temp is None:
            return 0.0

        return temp

    @pin_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def pin_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PinDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def pin_position_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinPositionTolerance")

        if temp is None:
            return 0.0

        return temp

    @pin_position_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def pin_position_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinPositionTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pitch_iso_quality_grade(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_int":
        """ListWithSelectedItem[int]"""
        temp = pythonnet_property_get(self.wrapped, "PitchISOQualityGrade")

        if temp is None:
            return 0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_int",
        )(temp)

    @pitch_iso_quality_grade.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_iso_quality_grade(self: "Self", value: "int") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "PitchISOQualityGrade", value)

    @property
    @exception_bridge
    def planet_gear_bore_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetGearBoreDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def spindle_outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpindleOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_pin_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalPinLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def unsupported_pin_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UnsupportedPinLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def planet_gear(self: "Self") -> "_2762.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FlexiblePinAssembly":
        """Cast to another type.

        Returns:
            _Cast_FlexiblePinAssembly
        """
        return _Cast_FlexiblePinAssembly(self)
