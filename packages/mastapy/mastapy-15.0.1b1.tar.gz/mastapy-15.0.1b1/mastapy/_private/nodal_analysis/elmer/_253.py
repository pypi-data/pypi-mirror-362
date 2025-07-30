"""ElmerResultsFromMechanicalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.elmer import _251

_ELMER_RESULTS_FROM_MECHANICAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.Elmer", "ElmerResultsFromMechanicalAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElmerResultsFromMechanicalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElmerResultsFromMechanicalAnalysis._Cast_ElmerResultsFromMechanicalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElmerResultsFromMechanicalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElmerResultsFromMechanicalAnalysis:
    """Special nested class for casting ElmerResultsFromMechanicalAnalysis to subclasses."""

    __parent__: "ElmerResultsFromMechanicalAnalysis"

    @property
    def elmer_results(self: "CastSelf") -> "_251.ElmerResults":
        return self.__parent__._cast(_251.ElmerResults)

    @property
    def elmer_results_from_mechanical_analysis(
        self: "CastSelf",
    ) -> "ElmerResultsFromMechanicalAnalysis":
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
class ElmerResultsFromMechanicalAnalysis(_251.ElmerResults):
    """ElmerResultsFromMechanicalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELMER_RESULTS_FROM_MECHANICAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElmerResultsFromMechanicalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ElmerResultsFromMechanicalAnalysis
        """
        return _Cast_ElmerResultsFromMechanicalAnalysis(self)
