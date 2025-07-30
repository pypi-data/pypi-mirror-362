"""GearMeshCompoundModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5330,
)

_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "GearMeshCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5191,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5270,
        _5277,
        _5282,
        _5295,
        _5298,
        _5300,
        _5313,
        _5319,
        _5328,
        _5332,
        _5335,
        _5338,
        _5367,
        _5373,
        _5376,
        _5391,
        _5394,
    )

    Self = TypeVar("Self", bound="GearMeshCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshCompoundModalAnalysisAtAStiffness._Cast_GearMeshCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting GearMeshCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "GearMeshCompoundModalAnalysisAtAStiffness"

    @property
    def inter_mountable_component_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5330.InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness":
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
    def agma_gleason_conical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5270.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5270,
        )

        return self.__parent__._cast(
            _5270.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5277.BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5277,
        )

        return self.__parent__._cast(
            _5277.BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5282.BevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5282,
        )

        return self.__parent__._cast(
            _5282.BevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def concept_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5295.ConceptGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5295,
        )

        return self.__parent__._cast(
            _5295.ConceptGearMeshCompoundModalAnalysisAtAStiffness
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
    def cylindrical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5313.CylindricalGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5313,
        )

        return self.__parent__._cast(
            _5313.CylindricalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def face_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5319.FaceGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5319,
        )

        return self.__parent__._cast(
            _5319.FaceGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def hypoid_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5328.HypoidGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5328,
        )

        return self.__parent__._cast(
            _5328.HypoidGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> (
        "_5332.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5332,
        )

        return self.__parent__._cast(
            _5332.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> (
        "_5335.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtAStiffness"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5335,
        )

        return self.__parent__._cast(
            _5335.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5338.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5338,
        )

        return self.__parent__._cast(
            _5338.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def spiral_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5367.SpiralBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5367,
        )

        return self.__parent__._cast(
            _5367.SpiralBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5373.StraightBevelDiffGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5373,
        )

        return self.__parent__._cast(
            _5373.StraightBevelDiffGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5376.StraightBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5376,
        )

        return self.__parent__._cast(
            _5376.StraightBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def worm_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5391.WormGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5391,
        )

        return self.__parent__._cast(
            _5391.WormGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def zerol_bevel_gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5394.ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5394,
        )

        return self.__parent__._cast(
            _5394.ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness
        )

    @property
    def gear_mesh_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "GearMeshCompoundModalAnalysisAtAStiffness":
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
class GearMeshCompoundModalAnalysisAtAStiffness(
    _5330.InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness
):
    """GearMeshCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5191.GearMeshModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.GearMeshModalAnalysisAtAStiffness]

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
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5191.GearMeshModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.GearMeshModalAnalysisAtAStiffness]

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
    def cast_to(self: "Self") -> "_Cast_GearMeshCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_GearMeshCompoundModalAnalysisAtAStiffness
        """
        return _Cast_GearMeshCompoundModalAnalysisAtAStiffness(self)
