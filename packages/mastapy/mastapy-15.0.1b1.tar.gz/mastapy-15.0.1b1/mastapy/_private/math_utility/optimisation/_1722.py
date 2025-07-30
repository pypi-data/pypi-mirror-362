"""AbstractOptimisable"""

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

_ABSTRACT_OPTIMISABLE = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "AbstractOptimisable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.optimisation import _1725

    Self = TypeVar("Self", bound="AbstractOptimisable")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractOptimisable._Cast_AbstractOptimisable"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractOptimisable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractOptimisable:
    """Special nested class for casting AbstractOptimisable to subclasses."""

    __parent__: "AbstractOptimisable"

    @property
    def optimisable(self: "CastSelf") -> "_1725.Optimisable":
        from mastapy._private.math_utility.optimisation import _1725

        return self.__parent__._cast(_1725.Optimisable)

    @property
    def abstract_optimisable(self: "CastSelf") -> "AbstractOptimisable":
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
class AbstractOptimisable(_0.APIBase):
    """AbstractOptimisable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_OPTIMISABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def parameter_1(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Parameter1")

        if temp is None:
            return 0.0

        return temp

    @parameter_1.setter
    @exception_bridge
    @enforce_parameter_types
    def parameter_1(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Parameter1", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def parameter_2(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Parameter2")

        if temp is None:
            return 0.0

        return temp

    @parameter_2.setter
    @exception_bridge
    @enforce_parameter_types
    def parameter_2(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Parameter2", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractOptimisable":
        """Cast to another type.

        Returns:
            _Cast_AbstractOptimisable
        """
        return _Cast_AbstractOptimisable(self)
