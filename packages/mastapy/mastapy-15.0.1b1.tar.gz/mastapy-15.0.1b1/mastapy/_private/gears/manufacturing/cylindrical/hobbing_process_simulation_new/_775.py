"""HobbingProcessSimulationInput"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _761,
    _788,
)

_HOBBING_PROCESS_SIMULATION_INPUT = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "HobbingProcessSimulationInput",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _779,
        _780,
    )

    Self = TypeVar("Self", bound="HobbingProcessSimulationInput")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HobbingProcessSimulationInput._Cast_HobbingProcessSimulationInput",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HobbingProcessSimulationInput",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HobbingProcessSimulationInput:
    """Special nested class for casting HobbingProcessSimulationInput to subclasses."""

    __parent__: "HobbingProcessSimulationInput"

    @property
    def process_simulation_input(self: "CastSelf") -> "_788.ProcessSimulationInput":
        return self.__parent__._cast(_788.ProcessSimulationInput)

    @property
    def hobbing_process_simulation_input(
        self: "CastSelf",
    ) -> "HobbingProcessSimulationInput":
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
class HobbingProcessSimulationInput(_788.ProcessSimulationInput):
    """HobbingProcessSimulationInput

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HOBBING_PROCESS_SIMULATION_INPUT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def process_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod":
        """EnumWithSelectedValue[mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.ActiveProcessMethod]"""
        temp = pythonnet_property_get(self.wrapped, "ProcessMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @process_method.setter
    @exception_bridge
    @enforce_parameter_types
    def process_method(self: "Self", value: "_761.ActiveProcessMethod") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ProcessMethod", value)

    @property
    @exception_bridge
    def hob_manufacture_error(self: "Self") -> "_779.HobManufactureError":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.HobManufactureError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HobManufactureError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def hob_resharpening_error(self: "Self") -> "_780.HobResharpeningError":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.HobResharpeningError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HobResharpeningError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_HobbingProcessSimulationInput":
        """Cast to another type.

        Returns:
            _Cast_HobbingProcessSimulationInput
        """
        return _Cast_HobbingProcessSimulationInput(self)
