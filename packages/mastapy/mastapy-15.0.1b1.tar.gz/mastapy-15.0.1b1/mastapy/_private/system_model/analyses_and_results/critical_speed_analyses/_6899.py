"""CriticalSpeedAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7892

_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "CriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2891
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7877
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6901,
    )

    Self = TypeVar("Self", bound="CriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="CriticalSpeedAnalysis._Cast_CriticalSpeedAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CriticalSpeedAnalysis:
    """Special nested class for casting CriticalSpeedAnalysis to subclasses."""

    __parent__: "CriticalSpeedAnalysis"

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7892.StaticLoadAnalysisCase":
        return self.__parent__._cast(_7892.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7877.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7877,
        )

        return self.__parent__._cast(_7877.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2891.Context":
        from mastapy._private.system_model.analyses_and_results import _2891

        return self.__parent__._cast(_2891.Context)

    @property
    def critical_speed_analysis(self: "CastSelf") -> "CriticalSpeedAnalysis":
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
class CriticalSpeedAnalysis(_7892.StaticLoadAnalysisCase):
    """CriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def critical_speed_analysis_options(
        self: "Self",
    ) -> "_6901.CriticalSpeedAnalysisOptions":
        """mastapy.system_model.analyses_and_results.critical_speed_analyses.CriticalSpeedAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CriticalSpeedAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CriticalSpeedAnalysis
        """
        return _Cast_CriticalSpeedAnalysis(self)
