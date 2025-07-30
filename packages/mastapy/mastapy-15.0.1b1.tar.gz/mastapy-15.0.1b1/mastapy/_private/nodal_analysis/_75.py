"""LinearDampingConnectionProperties"""

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
from mastapy._private.nodal_analysis import _49

_LINEAR_DAMPING_CONNECTION_PROPERTIES = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "LinearDampingConnectionProperties"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LinearDampingConnectionProperties")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LinearDampingConnectionProperties._Cast_LinearDampingConnectionProperties",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LinearDampingConnectionProperties",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LinearDampingConnectionProperties:
    """Special nested class for casting LinearDampingConnectionProperties to subclasses."""

    __parent__: "LinearDampingConnectionProperties"

    @property
    def abstract_linear_connection_properties(
        self: "CastSelf",
    ) -> "_49.AbstractLinearConnectionProperties":
        return self.__parent__._cast(_49.AbstractLinearConnectionProperties)

    @property
    def linear_damping_connection_properties(
        self: "CastSelf",
    ) -> "LinearDampingConnectionProperties":
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
class LinearDampingConnectionProperties(_49.AbstractLinearConnectionProperties):
    """LinearDampingConnectionProperties

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LINEAR_DAMPING_CONNECTION_PROPERTIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_damping(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialDamping")

        if temp is None:
            return 0.0

        return temp

    @axial_damping.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_damping(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AxialDamping", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def radial_damping(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialDamping")

        if temp is None:
            return 0.0

        return temp

    @radial_damping.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_damping(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialDamping", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tilt_damping(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltDamping")

        if temp is None:
            return 0.0

        return temp

    @tilt_damping.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_damping(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltDamping", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def torsional_damping(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TorsionalDamping")

        if temp is None:
            return 0.0

        return temp

    @torsional_damping.setter
    @exception_bridge
    @enforce_parameter_types
    def torsional_damping(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TorsionalDamping", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LinearDampingConnectionProperties":
        """Cast to another type.

        Returns:
            _Cast_LinearDampingConnectionProperties
        """
        return _Cast_LinearDampingConnectionProperties(self)
