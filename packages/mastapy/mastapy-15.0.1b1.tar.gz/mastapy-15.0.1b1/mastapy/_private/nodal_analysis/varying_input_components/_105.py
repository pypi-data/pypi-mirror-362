"""VelocityInputComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.varying_input_components import _99

_VELOCITY_INPUT_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.VaryingInputComponents", "VelocityInputComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="VelocityInputComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="VelocityInputComponent._Cast_VelocityInputComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("VelocityInputComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VelocityInputComponent:
    """Special nested class for casting VelocityInputComponent to subclasses."""

    __parent__: "VelocityInputComponent"

    @property
    def abstract_varying_input_component(
        self: "CastSelf",
    ) -> "_99.AbstractVaryingInputComponent":
        return self.__parent__._cast(_99.AbstractVaryingInputComponent)

    @property
    def velocity_input_component(self: "CastSelf") -> "VelocityInputComponent":
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
class VelocityInputComponent(_99.AbstractVaryingInputComponent):
    """VelocityInputComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VELOCITY_INPUT_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Velocity")

        if temp is None:
            return 0.0

        return temp

    @velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Velocity", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_VelocityInputComponent":
        """Cast to another type.

        Returns:
            _Cast_VelocityInputComponent
        """
        return _Cast_VelocityInputComponent(self)
