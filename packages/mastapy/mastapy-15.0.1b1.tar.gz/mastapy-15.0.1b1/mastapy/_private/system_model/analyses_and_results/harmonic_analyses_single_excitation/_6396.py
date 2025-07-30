"""ModalAnalysisForHarmonicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4926

_MODAL_ANALYSIS_FOR_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "ModalAnalysisForHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2891
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7877,
        _7892,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6058,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
        _6141,
    )

    Self = TypeVar("Self", bound="ModalAnalysisForHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ModalAnalysisForHarmonicAnalysis._Cast_ModalAnalysisForHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModalAnalysisForHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModalAnalysisForHarmonicAnalysis:
    """Special nested class for casting ModalAnalysisForHarmonicAnalysis to subclasses."""

    __parent__: "ModalAnalysisForHarmonicAnalysis"

    @property
    def modal_analysis(self: "CastSelf") -> "_4926.ModalAnalysis":
        return self.__parent__._cast(_4926.ModalAnalysis)

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
    def modal_analysis_for_transfer_path_analysis(
        self: "CastSelf",
    ) -> "_6141.ModalAnalysisForTransferPathAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
            _6141,
        )

        return self.__parent__._cast(_6141.ModalAnalysisForTransferPathAnalysis)

    @property
    def modal_analysis_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "ModalAnalysisForHarmonicAnalysis":
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
class ModalAnalysisForHarmonicAnalysis(_4926.ModalAnalysis):
    """ModalAnalysisForHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODAL_ANALYSIS_FOR_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def frequency_for_truncation_correction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyForTruncationCorrection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def harmonic_analysis_settings(self: "Self") -> "_6058.HarmonicAnalysisOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ModalAnalysisForHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ModalAnalysisForHarmonicAnalysis
        """
        return _Cast_ModalAnalysisForHarmonicAnalysis(self)
