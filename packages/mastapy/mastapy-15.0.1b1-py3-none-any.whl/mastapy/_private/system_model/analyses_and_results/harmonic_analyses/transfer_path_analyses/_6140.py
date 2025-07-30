"""DynamicModelForTransferPathAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6023

_DYNAMIC_MODEL_FOR_TRANSFER_PATH_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.TransferPathAnalyses",
    "DynamicModelForTransferPathAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2891
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7877,
        _7886,
        _7892,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6641,
    )

    Self = TypeVar("Self", bound="DynamicModelForTransferPathAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DynamicModelForTransferPathAnalysis._Cast_DynamicModelForTransferPathAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicModelForTransferPathAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicModelForTransferPathAnalysis:
    """Special nested class for casting DynamicModelForTransferPathAnalysis to subclasses."""

    __parent__: "DynamicModelForTransferPathAnalysis"

    @property
    def dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6023.DynamicModelForHarmonicAnalysis":
        return self.__parent__._cast(_6023.DynamicModelForHarmonicAnalysis)

    @property
    def dynamic_analysis(self: "CastSelf") -> "_6641.DynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6641,
        )

        return self.__parent__._cast(_6641.DynamicAnalysis)

    @property
    def fe_analysis(self: "CastSelf") -> "_7886.FEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7886,
        )

        return self.__parent__._cast(_7886.FEAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7892.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7892,
        )

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
    def dynamic_model_for_transfer_path_analysis(
        self: "CastSelf",
    ) -> "DynamicModelForTransferPathAnalysis":
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
class DynamicModelForTransferPathAnalysis(_6023.DynamicModelForHarmonicAnalysis):
    """DynamicModelForTransferPathAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_MODEL_FOR_TRANSFER_PATH_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicModelForTransferPathAnalysis":
        """Cast to another type.

        Returns:
            _Cast_DynamicModelForTransferPathAnalysis
        """
        return _Cast_DynamicModelForTransferPathAnalysis(self)
