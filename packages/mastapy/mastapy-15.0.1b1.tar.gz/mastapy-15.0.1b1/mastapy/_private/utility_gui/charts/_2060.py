"""MatrixVisualisationDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility_gui.charts import _2070

_MATRIX_VISUALISATION_DEFINITION = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Charts", "MatrixVisualisationDefinition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1943
    from mastapy._private.utility_gui.charts import _2062

    Self = TypeVar("Self", bound="MatrixVisualisationDefinition")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MatrixVisualisationDefinition._Cast_MatrixVisualisationDefinition",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MatrixVisualisationDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MatrixVisualisationDefinition:
    """Special nested class for casting MatrixVisualisationDefinition to subclasses."""

    __parent__: "MatrixVisualisationDefinition"

    @property
    def two_d_chart_definition(self: "CastSelf") -> "_2070.TwoDChartDefinition":
        return self.__parent__._cast(_2070.TwoDChartDefinition)

    @property
    def nd_chart_definition(self: "CastSelf") -> "_2062.NDChartDefinition":
        from mastapy._private.utility_gui.charts import _2062

        return self.__parent__._cast(_2062.NDChartDefinition)

    @property
    def chart_definition(self: "CastSelf") -> "_1943.ChartDefinition":
        from mastapy._private.utility.report import _1943

        return self.__parent__._cast(_1943.ChartDefinition)

    @property
    def matrix_visualisation_definition(
        self: "CastSelf",
    ) -> "MatrixVisualisationDefinition":
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
class MatrixVisualisationDefinition(_2070.TwoDChartDefinition):
    """MatrixVisualisationDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MATRIX_VISUALISATION_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MatrixVisualisationDefinition":
        """Cast to another type.

        Returns:
            _Cast_MatrixVisualisationDefinition
        """
        return _Cast_MatrixVisualisationDefinition(self)
