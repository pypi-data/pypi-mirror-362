"""ModalAnalysisBarModelFEExportOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4927

_MODAL_ANALYSIS_BAR_MODEL_FE_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "ModalAnalysisBarModelFEExportOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ModalAnalysisBarModelFEExportOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ModalAnalysisBarModelFEExportOptions._Cast_ModalAnalysisBarModelFEExportOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModalAnalysisBarModelFEExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModalAnalysisBarModelFEExportOptions:
    """Special nested class for casting ModalAnalysisBarModelFEExportOptions to subclasses."""

    __parent__: "ModalAnalysisBarModelFEExportOptions"

    @property
    def modal_analysis_bar_model_base_fe_export_options(
        self: "CastSelf",
    ) -> "_4927.ModalAnalysisBarModelBaseFEExportOptions":
        return self.__parent__._cast(_4927.ModalAnalysisBarModelBaseFEExportOptions)

    @property
    def modal_analysis_bar_model_fe_export_options(
        self: "CastSelf",
    ) -> "ModalAnalysisBarModelFEExportOptions":
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
class ModalAnalysisBarModelFEExportOptions(
    _4927.ModalAnalysisBarModelBaseFEExportOptions
):
    """ModalAnalysisBarModelFEExportOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODAL_ANALYSIS_BAR_MODEL_FE_EXPORT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ModalAnalysisBarModelFEExportOptions":
        """Cast to another type.

        Returns:
            _Cast_ModalAnalysisBarModelFEExportOptions
        """
        return _Cast_ModalAnalysisBarModelFEExportOptions(self)
