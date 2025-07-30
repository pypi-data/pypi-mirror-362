"""MethodOutcome"""

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

_METHOD_OUTCOME = python_net_import("SMT.MastaAPI.Utility", "MethodOutcome")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility import _1783

    Self = TypeVar("Self", bound="MethodOutcome")
    CastSelf = TypeVar("CastSelf", bound="MethodOutcome._Cast_MethodOutcome")


__docformat__ = "restructuredtext en"
__all__ = ("MethodOutcome",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MethodOutcome:
    """Special nested class for casting MethodOutcome to subclasses."""

    __parent__: "MethodOutcome"

    @property
    def method_outcome_with_result(self: "CastSelf") -> "_1783.MethodOutcomeWithResult":
        from mastapy._private.utility import _1783

        return self.__parent__._cast(_1783.MethodOutcomeWithResult)

    @property
    def method_outcome(self: "CastSelf") -> "MethodOutcome":
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
class MethodOutcome(_0.APIBase):
    """MethodOutcome

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _METHOD_OUTCOME

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def failure_message(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FailureMessage")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def successful(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Successful")

        if temp is None:
            return False

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_MethodOutcome":
        """Cast to another type.

        Returns:
            _Cast_MethodOutcome
        """
        return _Cast_MethodOutcome(self)
