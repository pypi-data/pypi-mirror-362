"""ToleranceCombination"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_TOLERANCE_COMBINATION = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "ToleranceCombination"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.tolerances import _2108

    Self = TypeVar("Self", bound="ToleranceCombination")
    CastSelf = TypeVar(
        "CastSelf", bound="ToleranceCombination._Cast_ToleranceCombination"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToleranceCombination",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToleranceCombination:
    """Special nested class for casting ToleranceCombination to subclasses."""

    __parent__: "ToleranceCombination"

    @property
    def tolerance_combination(self: "CastSelf") -> "ToleranceCombination":
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
class ToleranceCombination(_0.APIBase):
    """ToleranceCombination

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOLERANCE_COMBINATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fit(self: "Self") -> "_2108.FitType":
        """mastapy.bearings.tolerances.FitType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Fit")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.Tolerances.FitType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.tolerances._2108", "FitType"
        )(value)

    @property
    @exception_bridge
    def lower_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowerValue")

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
    def upper_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UpperValue")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ToleranceCombination":
        """Cast to another type.

        Returns:
            _Cast_ToleranceCombination
        """
        return _Cast_ToleranceCombination(self)
