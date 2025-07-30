"""LegacyChartMathChartDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1943

_LEGACY_CHART_MATH_CHART_DEFINITION = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Charts", "LegacyChartMathChartDefinition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LegacyChartMathChartDefinition")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LegacyChartMathChartDefinition._Cast_LegacyChartMathChartDefinition",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LegacyChartMathChartDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LegacyChartMathChartDefinition:
    """Special nested class for casting LegacyChartMathChartDefinition to subclasses."""

    __parent__: "LegacyChartMathChartDefinition"

    @property
    def chart_definition(self: "CastSelf") -> "_1943.ChartDefinition":
        return self.__parent__._cast(_1943.ChartDefinition)

    @property
    def legacy_chart_math_chart_definition(
        self: "CastSelf",
    ) -> "LegacyChartMathChartDefinition":
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
class LegacyChartMathChartDefinition(_1943.ChartDefinition):
    """LegacyChartMathChartDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LEGACY_CHART_MATH_CHART_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LegacyChartMathChartDefinition":
        """Cast to another type.

        Returns:
            _Cast_LegacyChartMathChartDefinition
        """
        return _Cast_LegacyChartMathChartDefinition(self)
