"""ConstraintResult"""

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
)

_CONSTRAINT_RESULT = python_net_import(
    "SMT.MastaAPI.MathUtility.BayesianOptimization", "ConstraintResult"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConstraintResult")
    CastSelf = TypeVar("CastSelf", bound="ConstraintResult._Cast_ConstraintResult")


__docformat__ = "restructuredtext en"
__all__ = ("ConstraintResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConstraintResult:
    """Special nested class for casting ConstraintResult to subclasses."""

    __parent__: "ConstraintResult"

    @property
    def constraint_result(self: "CastSelf") -> "ConstraintResult":
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
class ConstraintResult(_0.APIBase):
    """ConstraintResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONSTRAINT_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def constraint_met(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConstraintMet")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def denormalized_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DenormalizedValue")

        if temp is None:
            return 0.0

        return temp

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
    def value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Value")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ConstraintResult":
        """Cast to another type.

        Returns:
            _Cast_ConstraintResult
        """
        return _Cast_ConstraintResult(self)
