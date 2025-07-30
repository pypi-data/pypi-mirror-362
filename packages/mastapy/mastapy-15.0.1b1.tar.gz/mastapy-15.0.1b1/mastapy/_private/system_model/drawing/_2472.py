"""ModalAnalysisViewable"""

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
from mastapy._private.system_model.drawing import _2469

_MODAL_ANALYSIS_VIEWABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "ModalAnalysisViewable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6642,
    )
    from mastapy._private.system_model.drawing import _2474

    Self = TypeVar("Self", bound="ModalAnalysisViewable")
    CastSelf = TypeVar(
        "CastSelf", bound="ModalAnalysisViewable._Cast_ModalAnalysisViewable"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModalAnalysisViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModalAnalysisViewable:
    """Special nested class for casting ModalAnalysisViewable to subclasses."""

    __parent__: "ModalAnalysisViewable"

    @property
    def dynamic_analysis_viewable(self: "CastSelf") -> "_2469.DynamicAnalysisViewable":
        return self.__parent__._cast(_2469.DynamicAnalysisViewable)

    @property
    def part_analysis_case_with_contour_viewable(
        self: "CastSelf",
    ) -> "_2474.PartAnalysisCaseWithContourViewable":
        from mastapy._private.system_model.drawing import _2474

        return self.__parent__._cast(_2474.PartAnalysisCaseWithContourViewable)

    @property
    def modal_analysis_viewable(self: "CastSelf") -> "ModalAnalysisViewable":
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
class ModalAnalysisViewable(_2469.DynamicAnalysisViewable):
    """ModalAnalysisViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODAL_ANALYSIS_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def dynamic_analysis_draw_style(self: "Self") -> "_6642.DynamicAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.dynamic_analyses.DynamicAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ModalAnalysisViewable":
        """Cast to another type.

        Returns:
            _Cast_ModalAnalysisViewable
        """
        return _Cast_ModalAnalysisViewable(self)
