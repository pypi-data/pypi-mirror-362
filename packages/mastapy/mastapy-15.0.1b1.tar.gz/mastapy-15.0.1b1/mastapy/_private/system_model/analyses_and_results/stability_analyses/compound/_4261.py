"""SpringDamperConnectionCompoundStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4194,
)

_SPRING_DAMPER_CONNECTION_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "SpringDamperConnectionCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4126,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4191,
        _4221,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2571

    Self = TypeVar("Self", bound="SpringDamperConnectionCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpringDamperConnectionCompoundStabilityAnalysis._Cast_SpringDamperConnectionCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamperConnectionCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpringDamperConnectionCompoundStabilityAnalysis:
    """Special nested class for casting SpringDamperConnectionCompoundStabilityAnalysis to subclasses."""

    __parent__: "SpringDamperConnectionCompoundStabilityAnalysis"

    @property
    def coupling_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4194.CouplingConnectionCompoundStabilityAnalysis":
        return self.__parent__._cast(_4194.CouplingConnectionCompoundStabilityAnalysis)

    @property
    def inter_mountable_component_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4221.InterMountableComponentConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4221,
        )

        return self.__parent__._cast(
            _4221.InterMountableComponentConnectionCompoundStabilityAnalysis
        )

    @property
    def connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4191.ConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4191,
        )

        return self.__parent__._cast(_4191.ConnectionCompoundStabilityAnalysis)

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
    def spring_damper_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "SpringDamperConnectionCompoundStabilityAnalysis":
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
class SpringDamperConnectionCompoundStabilityAnalysis(
    _4194.CouplingConnectionCompoundStabilityAnalysis
):
    """SpringDamperConnectionCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPRING_DAMPER_CONNECTION_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2571.SpringDamperConnection":
        """mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection

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
    def connection_design(self: "Self") -> "_2571.SpringDamperConnection":
        """mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection

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
    ) -> "List[_4126.SpringDamperConnectionStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.SpringDamperConnectionStabilityAnalysis]

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
    ) -> "List[_4126.SpringDamperConnectionStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.SpringDamperConnectionStabilityAnalysis]

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
    ) -> "_Cast_SpringDamperConnectionCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SpringDamperConnectionCompoundStabilityAnalysis
        """
        return _Cast_SpringDamperConnectionCompoundStabilityAnalysis(self)
