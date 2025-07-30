"""ShaftSectionDamageResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_SHAFT_SECTION_DAMAGE_RESULTS = python_net_import(
    "SMT.MastaAPI.Shafts", "ShaftSectionDamageResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.shafts import _40

    Self = TypeVar("Self", bound="ShaftSectionDamageResults")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftSectionDamageResults._Cast_ShaftSectionDamageResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSectionDamageResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSectionDamageResults:
    """Special nested class for casting ShaftSectionDamageResults to subclasses."""

    __parent__: "ShaftSectionDamageResults"

    @property
    def shaft_section_damage_results(self: "CastSelf") -> "ShaftSectionDamageResults":
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
class ShaftSectionDamageResults(_0.APIBase):
    """ShaftSectionDamageResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SECTION_DAMAGE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def left_end(self: "Self") -> "_40.ShaftSectionEndDamageResults":
        """mastapy.shafts.ShaftSectionEndDamageResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftEnd")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_end(self: "Self") -> "_40.ShaftSectionEndDamageResults":
        """mastapy.shafts.ShaftSectionEndDamageResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightEnd")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSectionDamageResults":
        """Cast to another type.

        Returns:
            _Cast_ShaftSectionDamageResults
        """
        return _Cast_ShaftSectionDamageResults(self)
