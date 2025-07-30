"""ThreeDVectorChartDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility_gui.charts import _2062

_THREE_D_VECTOR_CHART_DEFINITION = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Charts", "ThreeDVectorChartDefinition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1943

    Self = TypeVar("Self", bound="ThreeDVectorChartDefinition")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ThreeDVectorChartDefinition._Cast_ThreeDVectorChartDefinition",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThreeDVectorChartDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThreeDVectorChartDefinition:
    """Special nested class for casting ThreeDVectorChartDefinition to subclasses."""

    __parent__: "ThreeDVectorChartDefinition"

    @property
    def nd_chart_definition(self: "CastSelf") -> "_2062.NDChartDefinition":
        return self.__parent__._cast(_2062.NDChartDefinition)

    @property
    def chart_definition(self: "CastSelf") -> "_1943.ChartDefinition":
        from mastapy._private.utility.report import _1943

        return self.__parent__._cast(_1943.ChartDefinition)

    @property
    def three_d_vector_chart_definition(
        self: "CastSelf",
    ) -> "ThreeDVectorChartDefinition":
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
class ThreeDVectorChartDefinition(_2062.NDChartDefinition):
    """ThreeDVectorChartDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THREE_D_VECTOR_CHART_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ThreeDVectorChartDefinition":
        """Cast to another type.

        Returns:
            _Cast_ThreeDVectorChartDefinition
        """
        return _Cast_ThreeDVectorChartDefinition(self)
