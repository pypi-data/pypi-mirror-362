"""ToothAndSlot"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1366

_TOOTH_AND_SLOT = python_net_import("SMT.MastaAPI.ElectricMachines", "ToothAndSlot")

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.electric_machines import _1443, _1444

    Self = TypeVar("Self", bound="ToothAndSlot")
    CastSelf = TypeVar("CastSelf", bound="ToothAndSlot._Cast_ToothAndSlot")


__docformat__ = "restructuredtext en"
__all__ = ("ToothAndSlot",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothAndSlot:
    """Special nested class for casting ToothAndSlot to subclasses."""

    __parent__: "ToothAndSlot"

    @property
    def abstract_tooth_and_slot(self: "CastSelf") -> "_1366.AbstractToothAndSlot":
        return self.__parent__._cast(_1366.AbstractToothAndSlot)

    @property
    def tooth_and_slot(self: "CastSelf") -> "ToothAndSlot":
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
class ToothAndSlot(_1366.AbstractToothAndSlot):
    """ToothAndSlot

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_AND_SLOT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def full_round_at_slot_bottom(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "FullRoundAtSlotBottom")

        if temp is None:
            return False

        return temp

    @full_round_at_slot_bottom.setter
    @exception_bridge
    @enforce_parameter_types
    def full_round_at_slot_bottom(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FullRoundAtSlotBottom",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def has_wedges(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasWedges")

        if temp is None:
            return False

        return temp

    @has_wedges.setter
    @exception_bridge
    @enforce_parameter_types
    def has_wedges(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasWedges", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def radius_of_curvature_at_slot_bottom(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadiusOfCurvatureAtSlotBottom")

        if temp is None:
            return 0.0

        return temp

    @radius_of_curvature_at_slot_bottom.setter
    @exception_bridge
    @enforce_parameter_types
    def radius_of_curvature_at_slot_bottom(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadiusOfCurvatureAtSlotBottom",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def slot_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SlotDepth")

        if temp is None:
            return 0.0

        return temp

    @slot_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def slot_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SlotDepth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def slot_opening_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SlotOpeningLength")

        if temp is None:
            return 0.0

        return temp

    @slot_opening_length.setter
    @exception_bridge
    @enforce_parameter_types
    def slot_opening_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SlotOpeningLength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def slot_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SlotWidth")

        if temp is None:
            return 0.0

        return temp

    @slot_width.setter
    @exception_bridge
    @enforce_parameter_types
    def slot_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SlotWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tooth_asymmetric_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToothAsymmetricLength")

        if temp is None:
            return 0.0

        return temp

    @tooth_asymmetric_length.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_asymmetric_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToothAsymmetricLength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tooth_taper_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToothTaperAngle")

        if temp is None:
            return 0.0

        return temp

    @tooth_taper_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_taper_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ToothTaperAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tooth_taper_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToothTaperDepth")

        if temp is None:
            return 0.0

        return temp

    @tooth_taper_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_taper_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ToothTaperDepth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tooth_taper_specification(self: "Self") -> "_1444.ToothTaperSpecification":
        """mastapy.electric_machines.ToothTaperSpecification"""
        temp = pythonnet_property_get(self.wrapped, "ToothTaperSpecification")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.ToothTaperSpecification"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1444", "ToothTaperSpecification"
        )(value)

    @tooth_taper_specification.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_taper_specification(
        self: "Self", value: "_1444.ToothTaperSpecification"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.ToothTaperSpecification"
        )
        pythonnet_property_set(self.wrapped, "ToothTaperSpecification", value)

    @property
    @exception_bridge
    def tooth_tip_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToothTipDepth")

        if temp is None:
            return 0.0

        return temp

    @tooth_tip_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_tip_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ToothTipDepth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tooth_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToothWidth")

        if temp is None:
            return 0.0

        return temp

    @tooth_width.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ToothWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tooth_width_at_slot_bottom(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToothWidthAtSlotBottom")

        if temp is None:
            return 0.0

        return temp

    @tooth_width_at_slot_bottom.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_width_at_slot_bottom(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToothWidthAtSlotBottom",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tooth_width_at_slot_top(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToothWidthAtSlotTop")

        if temp is None:
            return 0.0

        return temp

    @tooth_width_at_slot_top.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_width_at_slot_top(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToothWidthAtSlotTop",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tooth_slot_style(self: "Self") -> "_1443.ToothSlotStyle":
        """mastapy.electric_machines.ToothSlotStyle"""
        temp = pythonnet_property_get(self.wrapped, "ToothSlotStyle")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.ToothSlotStyle"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1443", "ToothSlotStyle"
        )(value)

    @tooth_slot_style.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_slot_style(self: "Self", value: "_1443.ToothSlotStyle") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.ToothSlotStyle"
        )
        pythonnet_property_set(self.wrapped, "ToothSlotStyle", value)

    @property
    @exception_bridge
    def wedge_thickness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "WedgeThickness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @wedge_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def wedge_thickness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "WedgeThickness", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ToothAndSlot":
        """Cast to another type.

        Returns:
            _Cast_ToothAndSlot
        """
        return _Cast_ToothAndSlot(self)
