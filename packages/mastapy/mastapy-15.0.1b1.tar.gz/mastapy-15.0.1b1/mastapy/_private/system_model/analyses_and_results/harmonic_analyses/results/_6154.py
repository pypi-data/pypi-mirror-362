"""HarmonicSelection"""

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

_HARMONIC_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results",
    "HarmonicSelection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HarmonicSelection")
    CastSelf = TypeVar("CastSelf", bound="HarmonicSelection._Cast_HarmonicSelection")


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicSelection:
    """Special nested class for casting HarmonicSelection to subclasses."""

    __parent__: "HarmonicSelection"

    @property
    def harmonic_selection(self: "CastSelf") -> "HarmonicSelection":
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
class HarmonicSelection(_0.APIBase):
    """HarmonicSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def harmonic(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Harmonic")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def included(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Included")

        if temp is None:
            return False

        return temp

    @included.setter
    @exception_bridge
    @enforce_parameter_types
    def included(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Included", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def is_included_in_excitations(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsIncludedInExcitations")

        if temp is None:
            return False

        return temp

    @is_included_in_excitations.setter
    @exception_bridge
    @enforce_parameter_types
    def is_included_in_excitations(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsIncludedInExcitations",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def order(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Order")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicSelection":
        """Cast to another type.

        Returns:
            _Cast_HarmonicSelection
        """
        return _Cast_HarmonicSelection(self)
