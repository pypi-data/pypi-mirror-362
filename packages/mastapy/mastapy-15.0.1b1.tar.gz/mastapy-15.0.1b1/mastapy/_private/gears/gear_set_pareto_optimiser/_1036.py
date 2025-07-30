"""ParetoOptimiserChartInformation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_set_pareto_optimiser import _1007, _1014
from mastapy._private.gears.rating import _445

_PARETO_OPTIMISER_CHART_INFORMATION = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "ParetoOptimiserChartInformation"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ParetoOptimiserChartInformation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParetoOptimiserChartInformation._Cast_ParetoOptimiserChartInformation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParetoOptimiserChartInformation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParetoOptimiserChartInformation:
    """Special nested class for casting ParetoOptimiserChartInformation to subclasses."""

    __parent__: "ParetoOptimiserChartInformation"

    @property
    def chart_info_base(self: "CastSelf") -> "_1007.ChartInfoBase":
        return self.__parent__._cast(_1007.ChartInfoBase)

    @property
    def pareto_optimiser_chart_information(
        self: "CastSelf",
    ) -> "ParetoOptimiserChartInformation":
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
class ParetoOptimiserChartInformation(
    _1007.ChartInfoBase[_445.AbstractGearSetRating, _1014.GearSetOptimiserCandidate]
):
    """ParetoOptimiserChartInformation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARETO_OPTIMISER_CHART_INFORMATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ParetoOptimiserChartInformation":
        """Cast to another type.

        Returns:
            _Cast_ParetoOptimiserChartInformation
        """
        return _Cast_ParetoOptimiserChartInformation(self)
