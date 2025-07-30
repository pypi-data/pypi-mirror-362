"""BeltConnectionModalAnalysisAtAStiffness"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _5198,
)

_BELT_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
    "BeltConnectionModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5167,
        _5172,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7689
    from mastapy._private.system_model.connections_and_sockets import _2489

    Self = TypeVar("Self", bound="BeltConnectionModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BeltConnectionModalAnalysisAtAStiffness._Cast_BeltConnectionModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BeltConnectionModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BeltConnectionModalAnalysisAtAStiffness:
    """Special nested class for casting BeltConnectionModalAnalysisAtAStiffness to subclasses."""

    __parent__: "BeltConnectionModalAnalysisAtAStiffness"

    @property
    def inter_mountable_component_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5198.InterMountableComponentConnectionModalAnalysisAtAStiffness":
        return self.__parent__._cast(
            _5198.InterMountableComponentConnectionModalAnalysisAtAStiffness
        )

    @property
    def connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5167.ConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5167,
        )

        return self.__parent__._cast(_5167.ConnectionModalAnalysisAtAStiffness)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7883.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7883,
        )

        return self.__parent__._cast(_7883.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7880.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2890.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.ConnectionAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def cvt_belt_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5172.CVTBeltConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5172,
        )

        return self.__parent__._cast(_5172.CVTBeltConnectionModalAnalysisAtAStiffness)

    @property
    def belt_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "BeltConnectionModalAnalysisAtAStiffness":
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
class BeltConnectionModalAnalysisAtAStiffness(
    _5198.InterMountableComponentConnectionModalAnalysisAtAStiffness
):
    """BeltConnectionModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BELT_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2489.BeltConnection":
        """mastapy.system_model.connections_and_sockets.BeltConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_load_case(self: "Self") -> "_7689.BeltConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BeltConnectionModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_BeltConnectionModalAnalysisAtAStiffness
        """
        return _Cast_BeltConnectionModalAnalysisAtAStiffness(self)
