"""ShaftOrHousingSelection"""

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

_SHAFT_OR_HOUSING_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.TransferPathAnalyses",
    "ShaftOrHousingSelection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShaftOrHousingSelection")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftOrHousingSelection._Cast_ShaftOrHousingSelection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftOrHousingSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftOrHousingSelection:
    """Special nested class for casting ShaftOrHousingSelection to subclasses."""

    __parent__: "ShaftOrHousingSelection"

    @property
    def shaft_or_housing_selection(self: "CastSelf") -> "ShaftOrHousingSelection":
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
class ShaftOrHousingSelection(_0.APIBase):
    """ShaftOrHousingSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_OR_HOUSING_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def include(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Include")

        if temp is None:
            return False

        return temp

    @include.setter
    @exception_bridge
    @enforce_parameter_types
    def include(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Include", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftOrHousingSelection":
        """Cast to another type.

        Returns:
            _Cast_ShaftOrHousingSelection
        """
        return _Cast_ShaftOrHousingSelection(self)
