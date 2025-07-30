"""ConicalGearMeshCompoundModalAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _5060,
)

_CONICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "ConicalGearMeshCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4874
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _5006,
        _5013,
        _5018,
        _5036,
        _5064,
        _5066,
        _5068,
        _5071,
        _5074,
        _5103,
        _5109,
        _5112,
        _5130,
    )

    Self = TypeVar("Self", bound="ConicalGearMeshCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMeshCompoundModalAnalysis._Cast_ConicalGearMeshCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshCompoundModalAnalysis:
    """Special nested class for casting ConicalGearMeshCompoundModalAnalysis to subclasses."""

    __parent__: "ConicalGearMeshCompoundModalAnalysis"

    @property
    def gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5060.GearMeshCompoundModalAnalysis":
        return self.__parent__._cast(_5060.GearMeshCompoundModalAnalysis)

    @property
    def inter_mountable_component_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5066.InterMountableComponentConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5066,
        )

        return self.__parent__._cast(
            _5066.InterMountableComponentConnectionCompoundModalAnalysis
        )

    @property
    def connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5036.ConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5036,
        )

        return self.__parent__._cast(_5036.ConnectionCompoundModalAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5006.AGMAGleasonConicalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5006,
        )

        return self.__parent__._cast(
            _5006.AGMAGleasonConicalGearMeshCompoundModalAnalysis
        )

    @property
    def bevel_differential_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5013.BevelDifferentialGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5013,
        )

        return self.__parent__._cast(
            _5013.BevelDifferentialGearMeshCompoundModalAnalysis
        )

    @property
    def bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5018.BevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5018,
        )

        return self.__parent__._cast(_5018.BevelGearMeshCompoundModalAnalysis)

    @property
    def hypoid_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5064.HypoidGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5064,
        )

        return self.__parent__._cast(_5064.HypoidGearMeshCompoundModalAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5068.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5068,
        )

        return self.__parent__._cast(
            _5068.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5071.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5071,
        )

        return self.__parent__._cast(
            _5071.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5074.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5074,
        )

        return self.__parent__._cast(
            _5074.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5103.SpiralBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5103,
        )

        return self.__parent__._cast(_5103.SpiralBevelGearMeshCompoundModalAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5109.StraightBevelDiffGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5109,
        )

        return self.__parent__._cast(
            _5109.StraightBevelDiffGearMeshCompoundModalAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5112.StraightBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5112,
        )

        return self.__parent__._cast(_5112.StraightBevelGearMeshCompoundModalAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5130.ZerolBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5130,
        )

        return self.__parent__._cast(_5130.ZerolBevelGearMeshCompoundModalAnalysis)

    @property
    def conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "ConicalGearMeshCompoundModalAnalysis":
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
class ConicalGearMeshCompoundModalAnalysis(_5060.GearMeshCompoundModalAnalysis):
    """ConicalGearMeshCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def planetaries(self: "Self") -> "List[ConicalGearMeshCompoundModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConicalGearMeshCompoundModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

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
    ) -> "List[_4874.ConicalGearMeshModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearMeshModalAnalysis]

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
    ) -> "List[_4874.ConicalGearMeshModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearMeshModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ConicalGearMeshCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshCompoundModalAnalysis
        """
        return _Cast_ConicalGearMeshCompoundModalAnalysis(self)
