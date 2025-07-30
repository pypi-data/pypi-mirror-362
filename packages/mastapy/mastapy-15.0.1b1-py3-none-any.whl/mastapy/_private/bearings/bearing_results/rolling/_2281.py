"""SMTRibStressResults"""

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

_SMT_RIB_STRESS_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "SMTRibStressResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SMTRibStressResults")
    CastSelf = TypeVar(
        "CastSelf", bound="SMTRibStressResults._Cast_SMTRibStressResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SMTRibStressResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SMTRibStressResults:
    """Special nested class for casting SMTRibStressResults to subclasses."""

    __parent__: "SMTRibStressResults"

    @property
    def smt_rib_stress_results(self: "CastSelf") -> "SMTRibStressResults":
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
class SMTRibStressResults(_0.APIBase):
    """SMTRibStressResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SMT_RIB_STRESS_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_rib_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumRibLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SMTRibStressResults":
        """Cast to another type.

        Returns:
            _Cast_SMTRibStressResults
        """
        return _Cast_SMTRibStressResults(self)
