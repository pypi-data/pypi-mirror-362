"""TransferPathAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_TRANSFER_PATH_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.TransferPathAnalyses",
    "TransferPathAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
        _6141,
    )

    Self = TypeVar("Self", bound="TransferPathAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="TransferPathAnalysis._Cast_TransferPathAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TransferPathAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TransferPathAnalysis:
    """Special nested class for casting TransferPathAnalysis to subclasses."""

    __parent__: "TransferPathAnalysis"

    @property
    def transfer_path_analysis(self: "CastSelf") -> "TransferPathAnalysis":
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
class TransferPathAnalysis(_0.APIBase):
    """TransferPathAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRANSFER_PATH_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def modal_analysis_of_tpa_submodel(
        self: "Self",
    ) -> "_6141.ModalAnalysisForTransferPathAnalysis":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses.ModalAnalysisForTransferPathAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalAnalysisOfTPASubmodel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_TransferPathAnalysis":
        """Cast to another type.

        Returns:
            _Cast_TransferPathAnalysis
        """
        return _Cast_TransferPathAnalysis(self)
