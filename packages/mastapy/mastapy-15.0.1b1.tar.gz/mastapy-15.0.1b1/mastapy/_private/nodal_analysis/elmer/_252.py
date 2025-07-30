"""ElmerResultsFromElectromagneticAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.elmer import _251

_ELMER_RESULTS_FROM_ELECTROMAGNETIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.Elmer", "ElmerResultsFromElectromagneticAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElmerResultsFromElectromagneticAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElmerResultsFromElectromagneticAnalysis._Cast_ElmerResultsFromElectromagneticAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElmerResultsFromElectromagneticAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElmerResultsFromElectromagneticAnalysis:
    """Special nested class for casting ElmerResultsFromElectromagneticAnalysis to subclasses."""

    __parent__: "ElmerResultsFromElectromagneticAnalysis"

    @property
    def elmer_results(self: "CastSelf") -> "_251.ElmerResults":
        return self.__parent__._cast(_251.ElmerResults)

    @property
    def elmer_results_from_electromagnetic_analysis(
        self: "CastSelf",
    ) -> "ElmerResultsFromElectromagneticAnalysis":
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
class ElmerResultsFromElectromagneticAnalysis(_251.ElmerResults):
    """ElmerResultsFromElectromagneticAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELMER_RESULTS_FROM_ELECTROMAGNETIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElmerResultsFromElectromagneticAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ElmerResultsFromElectromagneticAnalysis
        """
        return _Cast_ElmerResultsFromElectromagneticAnalysis(self)
