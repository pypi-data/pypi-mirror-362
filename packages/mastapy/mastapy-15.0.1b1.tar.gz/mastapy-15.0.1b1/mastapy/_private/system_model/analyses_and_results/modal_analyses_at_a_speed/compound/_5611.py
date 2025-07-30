"""PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5566,
)

_PART_TO_PART_SHEAR_COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
        "PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5479,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5563,
        _5593,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2569

    Self = TypeVar(
        "Self", bound="PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed._Cast_PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed:
    """Special nested class for casting PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed"

    @property
    def coupling_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5566.CouplingConnectionCompoundModalAnalysisAtASpeed":
        return self.__parent__._cast(
            _5566.CouplingConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def inter_mountable_component_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5593.InterMountableComponentConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5593,
        )

        return self.__parent__._cast(
            _5593.InterMountableComponentConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5563.ConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5563,
        )

        return self.__parent__._cast(_5563.ConnectionCompoundModalAnalysisAtASpeed)

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
    def part_to_part_shear_coupling_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed":
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
class PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed(
    _5566.CouplingConnectionCompoundModalAnalysisAtASpeed
):
    """PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _PART_TO_PART_SHEAR_COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2569.PartToPartShearCouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection

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
    def connection_design(self: "Self") -> "_2569.PartToPartShearCouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection

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
    ) -> "List[_5479.PartToPartShearCouplingConnectionModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.PartToPartShearCouplingConnectionModalAnalysisAtASpeed]

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
    ) -> "List[_5479.PartToPartShearCouplingConnectionModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.PartToPartShearCouplingConnectionModalAnalysisAtASpeed]

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
    ) -> "_Cast_PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed
        """
        return _Cast_PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed(
            self
        )
