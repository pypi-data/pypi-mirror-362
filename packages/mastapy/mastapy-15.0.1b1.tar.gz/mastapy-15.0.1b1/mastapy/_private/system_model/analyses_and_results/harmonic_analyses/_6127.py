"""TorqueConverterConnectionHarmonicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6007

_TORQUE_CONVERTER_CONNECTION_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "TorqueConverterConnectionHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6005,
        _6067,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7844
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3071,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2573

    Self = TypeVar("Self", bound="TorqueConverterConnectionHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorqueConverterConnectionHarmonicAnalysis._Cast_TorqueConverterConnectionHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterConnectionHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterConnectionHarmonicAnalysis:
    """Special nested class for casting TorqueConverterConnectionHarmonicAnalysis to subclasses."""

    __parent__: "TorqueConverterConnectionHarmonicAnalysis"

    @property
    def coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6007.CouplingConnectionHarmonicAnalysis":
        return self.__parent__._cast(_6007.CouplingConnectionHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6067.InterMountableComponentConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6067,
        )

        return self.__parent__._cast(
            _6067.InterMountableComponentConnectionHarmonicAnalysis
        )

    @property
    def connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6005.ConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6005,
        )

        return self.__parent__._cast(_6005.ConnectionHarmonicAnalysis)

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
    def torque_converter_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "TorqueConverterConnectionHarmonicAnalysis":
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
class TorqueConverterConnectionHarmonicAnalysis(
    _6007.CouplingConnectionHarmonicAnalysis
):
    """TorqueConverterConnectionHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER_CONNECTION_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2573.TorqueConverterConnection":
        """mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection

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
    def connection_load_case(self: "Self") -> "_7844.TorqueConverterConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase

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
    ) -> "_3071.TorqueConverterConnectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.TorqueConverterConnectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_TorqueConverterConnectionHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterConnectionHarmonicAnalysis
        """
        return _Cast_TorqueConverterConnectionHarmonicAnalysis(self)
