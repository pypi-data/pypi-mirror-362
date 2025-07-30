"""TorqueConverterConnectionCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6760,
)

_TORQUE_CONVERTER_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "TorqueConverterConnectionCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6710,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6757,
        _6787,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2573

    Self = TypeVar("Self", bound="TorqueConverterConnectionCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorqueConverterConnectionCompoundDynamicAnalysis._Cast_TorqueConverterConnectionCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterConnectionCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterConnectionCompoundDynamicAnalysis:
    """Special nested class for casting TorqueConverterConnectionCompoundDynamicAnalysis to subclasses."""

    __parent__: "TorqueConverterConnectionCompoundDynamicAnalysis"

    @property
    def coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6760.CouplingConnectionCompoundDynamicAnalysis":
        return self.__parent__._cast(_6760.CouplingConnectionCompoundDynamicAnalysis)

    @property
    def inter_mountable_component_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6787.InterMountableComponentConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6787,
        )

        return self.__parent__._cast(
            _6787.InterMountableComponentConnectionCompoundDynamicAnalysis
        )

    @property
    def connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6757.ConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6757,
        )

        return self.__parent__._cast(_6757.ConnectionCompoundDynamicAnalysis)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7881.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7881,
        )

        return self.__parent__._cast(_7881.ConnectionCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7885.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7885,
        )

        return self.__parent__._cast(_7885.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def torque_converter_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "TorqueConverterConnectionCompoundDynamicAnalysis":
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
class TorqueConverterConnectionCompoundDynamicAnalysis(
    _6760.CouplingConnectionCompoundDynamicAnalysis
):
    """TorqueConverterConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2573.TorqueConverterConnection":
        """mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6710.TorqueConverterConnectionDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterConnectionDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6710.TorqueConverterConnectionDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterConnectionDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_TorqueConverterConnectionCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterConnectionCompoundDynamicAnalysis
        """
        return _Cast_TorqueConverterConnectionCompoundDynamicAnalysis(self)
