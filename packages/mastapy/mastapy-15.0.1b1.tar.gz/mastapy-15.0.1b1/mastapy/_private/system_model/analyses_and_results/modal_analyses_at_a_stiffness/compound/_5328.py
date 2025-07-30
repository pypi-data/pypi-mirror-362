"""HypoidGearMeshCompoundModalAnalysisAtAStiffness"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5270,
)

_HYPOID_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "HypoidGearMeshCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5195,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5298,
        _5300,
        _5324,
        _5330,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2536

    Self = TypeVar("Self", bound="HypoidGearMeshCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HypoidGearMeshCompoundModalAnalysisAtAStiffness._Cast_HypoidGearMeshCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidGearMeshCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidGearMeshCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting HypoidGearMeshCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "HypoidGearMeshCompoundModalAnalysisAtAStiffness"

    @property
    def agma_gleason_conical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5270.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(
            _5270.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def conical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5298.ConicalGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5298,
        )

        return self.__parent__._cast(
            _5298.ConicalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5324.GearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5324,
        )

        return self.__parent__._cast(_5324.GearMeshCompoundModalAnalysisAtAStiffness)

    @property
    def inter_mountable_component_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5330.InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5330,
        )

        return self.__parent__._cast(
            _5330.InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5300.ConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5300,
        )

        return self.__parent__._cast(_5300.ConnectionCompoundModalAnalysisAtAStiffness)

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
    def hypoid_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "HypoidGearMeshCompoundModalAnalysisAtAStiffness":
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
class HypoidGearMeshCompoundModalAnalysisAtAStiffness(
    _5270.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness
):
    """HypoidGearMeshCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2536.HypoidGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh

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
    def connection_design(self: "Self") -> "_2536.HypoidGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh

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
    ) -> "List[_5195.HypoidGearMeshModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.HypoidGearMeshModalAnalysisAtAStiffness]

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
    ) -> "List[_5195.HypoidGearMeshModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.HypoidGearMeshModalAnalysisAtAStiffness]

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
    ) -> "_Cast_HypoidGearMeshCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_HypoidGearMeshCompoundModalAnalysisAtAStiffness
        """
        return _Cast_HypoidGearMeshCompoundModalAnalysisAtAStiffness(self)
