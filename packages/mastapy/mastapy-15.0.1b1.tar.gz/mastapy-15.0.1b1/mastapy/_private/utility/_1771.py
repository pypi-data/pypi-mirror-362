"""AnalysisRunInformation"""

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

_ANALYSIS_RUN_INFORMATION = python_net_import(
    "SMT.MastaAPI.Utility", "AnalysisRunInformation"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AnalysisRunInformation")
    CastSelf = TypeVar(
        "CastSelf", bound="AnalysisRunInformation._Cast_AnalysisRunInformation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AnalysisRunInformation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AnalysisRunInformation:
    """Special nested class for casting AnalysisRunInformation to subclasses."""

    __parent__: "AnalysisRunInformation"

    @property
    def analysis_run_information(self: "CastSelf") -> "AnalysisRunInformation":
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
class AnalysisRunInformation(_0.APIBase):
    """AnalysisRunInformation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ANALYSIS_RUN_INFORMATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def masta_version_used(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MASTAVersionUsed")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def specifications_of_computer_used(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpecificationsOfComputerUsed")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def time_taken(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeTaken")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AnalysisRunInformation":
        """Cast to another type.

        Returns:
            _Cast_AnalysisRunInformation
        """
        return _Cast_AnalysisRunInformation(self)
