"""SimpleChartDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1943

_SIMPLE_CHART_DEFINITION = python_net_import(
    "SMT.MastaAPI.Utility.Report", "SimpleChartDefinition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SimpleChartDefinition")
    CastSelf = TypeVar(
        "CastSelf", bound="SimpleChartDefinition._Cast_SimpleChartDefinition"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SimpleChartDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SimpleChartDefinition:
    """Special nested class for casting SimpleChartDefinition to subclasses."""

    __parent__: "SimpleChartDefinition"

    @property
    def chart_definition(self: "CastSelf") -> "_1943.ChartDefinition":
        return self.__parent__._cast(_1943.ChartDefinition)

    @property
    def simple_chart_definition(self: "CastSelf") -> "SimpleChartDefinition":
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
class SimpleChartDefinition(_1943.ChartDefinition):
    """SimpleChartDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SIMPLE_CHART_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SimpleChartDefinition":
        """Cast to another type.

        Returns:
            _Cast_SimpleChartDefinition
        """
        return _Cast_SimpleChartDefinition(self)
