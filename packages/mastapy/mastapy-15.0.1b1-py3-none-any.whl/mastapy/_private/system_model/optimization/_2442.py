"""MeasuredAndFactorViewModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_MEASURED_AND_FACTOR_VIEW_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization", "MeasuredAndFactorViewModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MeasuredAndFactorViewModel")
    CastSelf = TypeVar(
        "CastSelf", bound="MeasuredAndFactorViewModel._Cast_MeasuredAndFactorViewModel"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeasuredAndFactorViewModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeasuredAndFactorViewModel:
    """Special nested class for casting MeasuredAndFactorViewModel to subclasses."""

    __parent__: "MeasuredAndFactorViewModel"

    @property
    def measured_and_factor_view_model(
        self: "CastSelf",
    ) -> "MeasuredAndFactorViewModel":
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
class MeasuredAndFactorViewModel(_0.APIBase):
    """MeasuredAndFactorViewModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MEASURED_AND_FACTOR_VIEW_MODEL

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
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def per_normal_module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PerNormalModule")

        if temp is None:
            return 0.0

        return temp

    @per_normal_module.setter
    @exception_bridge
    @enforce_parameter_types
    def per_normal_module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PerNormalModule", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MeasuredAndFactorViewModel":
        """Cast to another type.

        Returns:
            _Cast_MeasuredAndFactorViewModel
        """
        return _Cast_MeasuredAndFactorViewModel(self)
