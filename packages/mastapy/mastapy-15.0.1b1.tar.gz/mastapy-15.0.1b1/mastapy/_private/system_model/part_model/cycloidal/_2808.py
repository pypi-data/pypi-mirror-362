"""RingPins"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2693

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_RING_PINS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "RingPins"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.cycloidal import _1647, _1648
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2698

    Self = TypeVar("Self", bound="RingPins")
    CastSelf = TypeVar("CastSelf", bound="RingPins._Cast_RingPins")


__docformat__ = "restructuredtext en"
__all__ = ("RingPins",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingPins:
    """Special nested class for casting RingPins to subclasses."""

    __parent__: "RingPins"

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
        return self.__parent__._cast(_2693.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        from mastapy._private.system_model.part_model import _2670

        return self.__parent__._cast(_2670.Component)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def ring_pins(self: "CastSelf") -> "RingPins":
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
class RingPins(_2693.MountableComponent):
    """RingPins

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_PINS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @exception_bridge
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def ring_pins_material_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "RingPinsMaterialDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @ring_pins_material_database.setter
    @exception_bridge
    @enforce_parameter_types
    def ring_pins_material_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "RingPinsMaterialDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def ring_pins_design(self: "Self") -> "_1647.RingPinsDesign":
        """mastapy.cycloidal.RingPinsDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPinsDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ring_pins_material(self: "Self") -> "_1648.RingPinsMaterial":
        """mastapy.cycloidal.RingPinsMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPinsMaterial")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RingPins":
        """Cast to another type.

        Returns:
            _Cast_RingPins
        """
        return _Cast_RingPins(self)
