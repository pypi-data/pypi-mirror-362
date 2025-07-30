"""BeltConnectionModalAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4912

_BELT_CONNECTION_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "BeltConnectionModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4877,
        _4883,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7689
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2940,
    )
    from mastapy._private.system_model.connections_and_sockets import _2489

    Self = TypeVar("Self", bound="BeltConnectionModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BeltConnectionModalAnalysis._Cast_BeltConnectionModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BeltConnectionModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BeltConnectionModalAnalysis:
    """Special nested class for casting BeltConnectionModalAnalysis to subclasses."""

    __parent__: "BeltConnectionModalAnalysis"

    @property
    def inter_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4912.InterMountableComponentConnectionModalAnalysis":
        return self.__parent__._cast(
            _4912.InterMountableComponentConnectionModalAnalysis
        )

    @property
    def connection_modal_analysis(self: "CastSelf") -> "_4877.ConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4877,
        )

        return self.__parent__._cast(_4877.ConnectionModalAnalysis)

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
    def cvt_belt_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4883.CVTBeltConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4883,
        )

        return self.__parent__._cast(_4883.CVTBeltConnectionModalAnalysis)

    @property
    def belt_connection_modal_analysis(
        self: "CastSelf",
    ) -> "BeltConnectionModalAnalysis":
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
class BeltConnectionModalAnalysis(_4912.InterMountableComponentConnectionModalAnalysis):
    """BeltConnectionModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BELT_CONNECTION_MODAL_ANALYSIS

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
    @exception_bridge
    def system_deflection_results(
        self: "Self",
    ) -> "_2940.BeltConnectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.BeltConnectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BeltConnectionModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BeltConnectionModalAnalysis
        """
        return _Cast_BeltConnectionModalAnalysis(self)
