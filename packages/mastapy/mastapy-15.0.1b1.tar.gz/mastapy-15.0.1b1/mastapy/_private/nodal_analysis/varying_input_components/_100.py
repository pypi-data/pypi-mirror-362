"""AngleInputComponent"""

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

_ANGLE_INPUT_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.VaryingInputComponents", "AngleInputComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AngleInputComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="AngleInputComponent._Cast_AngleInputComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AngleInputComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AngleInputComponent:
    """Special nested class for casting AngleInputComponent to subclasses."""

    __parent__: "AngleInputComponent"

    @property
    def abstract_varying_input_component(
        self: "CastSelf",
    ) -> "_99.AbstractVaryingInputComponent":
        return self.__parent__._cast(_99.AbstractVaryingInputComponent)

    @property
    def angle_input_component(self: "CastSelf") -> "AngleInputComponent":
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
class AngleInputComponent(_99.AbstractVaryingInputComponent):
    """AngleInputComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ANGLE_INPUT_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Angle")

        if temp is None:
            return 0.0

        return temp

    @angle.setter
    @exception_bridge
    @enforce_parameter_types
    def angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Angle", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AngleInputComponent":
        """Cast to another type.

        Returns:
            _Cast_AngleInputComponent
        """
        return _Cast_AngleInputComponent(self)
