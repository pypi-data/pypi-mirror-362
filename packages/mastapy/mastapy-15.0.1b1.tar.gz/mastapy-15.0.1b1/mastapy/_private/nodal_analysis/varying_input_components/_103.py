"""NonDimensionalInputComponent"""

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

_NON_DIMENSIONAL_INPUT_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.VaryingInputComponents", "NonDimensionalInputComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NonDimensionalInputComponent")
    CastSelf = TypeVar(
        "CastSelf",
        bound="NonDimensionalInputComponent._Cast_NonDimensionalInputComponent",
    )


__docformat__ = "restructuredtext en"
__all__ = ("NonDimensionalInputComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NonDimensionalInputComponent:
    """Special nested class for casting NonDimensionalInputComponent to subclasses."""

    __parent__: "NonDimensionalInputComponent"

    @property
    def abstract_varying_input_component(
        self: "CastSelf",
    ) -> "_99.AbstractVaryingInputComponent":
        return self.__parent__._cast(_99.AbstractVaryingInputComponent)

    @property
    def non_dimensional_input_component(
        self: "CastSelf",
    ) -> "NonDimensionalInputComponent":
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
class NonDimensionalInputComponent(_99.AbstractVaryingInputComponent):
    """NonDimensionalInputComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NON_DIMENSIONAL_INPUT_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def non_dimensional_quantity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalQuantity")

        if temp is None:
            return 0.0

        return temp

    @non_dimensional_quantity.setter
    @exception_bridge
    @enforce_parameter_types
    def non_dimensional_quantity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NonDimensionalQuantity",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_NonDimensionalInputComponent":
        """Cast to another type.

        Returns:
            _Cast_NonDimensionalInputComponent
        """
        return _Cast_NonDimensionalInputComponent(self)
