"""MethodOutcomeWithResult"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.utility import _1782

_METHOD_OUTCOME_WITH_RESULT = python_net_import(
    "SMT.MastaAPI.Utility", "MethodOutcomeWithResult"
)

if TYPE_CHECKING:
    from typing import Any, Type

    Self = TypeVar("Self", bound="MethodOutcomeWithResult")
    CastSelf = TypeVar(
        "CastSelf", bound="MethodOutcomeWithResult._Cast_MethodOutcomeWithResult"
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("MethodOutcomeWithResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MethodOutcomeWithResult:
    """Special nested class for casting MethodOutcomeWithResult to subclasses."""

    __parent__: "MethodOutcomeWithResult"

    @property
    def method_outcome(self: "CastSelf") -> "_1782.MethodOutcome":
        return self.__parent__._cast(_1782.MethodOutcome)

    @property
    def method_outcome_with_result(self: "CastSelf") -> "MethodOutcomeWithResult":
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
class MethodOutcomeWithResult(_1782.MethodOutcome, Generic[T]):
    """MethodOutcomeWithResult

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _METHOD_OUTCOME_WITH_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def result(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Result")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MethodOutcomeWithResult":
        """Cast to another type.

        Returns:
            _Cast_MethodOutcomeWithResult
        """
        return _Cast_MethodOutcomeWithResult(self)
