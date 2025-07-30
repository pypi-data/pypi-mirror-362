"""FESectionResults"""

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

_FE_SECTION_RESULTS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis", "FESectionResults"
)

if TYPE_CHECKING:
    from typing import Any, Optional, Type, TypeVar

    Self = TypeVar("Self", bound="FESectionResults")
    CastSelf = TypeVar("CastSelf", bound="FESectionResults._Cast_FESectionResults")


__docformat__ = "restructuredtext en"
__all__ = ("FESectionResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESectionResults:
    """Special nested class for casting FESectionResults to subclasses."""

    __parent__: "FESectionResults"

    @property
    def fe_section_results(self: "CastSelf") -> "FESectionResults":
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
class FESectionResults(_0.APIBase):
    """FESectionResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SECTION_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def kinetic_energy_contribution(self: "Self") -> "Optional[float]":
        """Optional[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KineticEnergyContribution")

        if temp is None:
            return None

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
    def solid_part_id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SolidPartID")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def strain_energy_contribution(self: "Self") -> "Optional[float]":
        """Optional[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrainEnergyContribution")

        if temp is None:
            return None

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_FESectionResults":
        """Cast to another type.

        Returns:
            _Cast_FESectionResults
        """
        return _Cast_FESectionResults(self)
