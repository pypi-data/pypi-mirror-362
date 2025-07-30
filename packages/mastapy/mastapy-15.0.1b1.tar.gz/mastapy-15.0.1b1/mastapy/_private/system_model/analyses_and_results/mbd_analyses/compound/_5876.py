"""GearMeshCompoundMultibodyDynamicsAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
    _5882,
)

_GEAR_MESH_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "GearMeshCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5721
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5822,
        _5829,
        _5834,
        _5847,
        _5850,
        _5852,
        _5865,
        _5871,
        _5880,
        _5884,
        _5887,
        _5890,
        _5919,
        _5925,
        _5928,
        _5943,
        _5946,
    )

    Self = TypeVar("Self", bound="GearMeshCompoundMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshCompoundMultibodyDynamicsAnalysis._Cast_GearMeshCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting GearMeshCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "GearMeshCompoundMultibodyDynamicsAnalysis"

    @property
    def inter_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5882.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5882.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5852.ConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5852,
        )

        return self.__parent__._cast(_5852.ConnectionCompoundMultibodyDynamicsAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5822.AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5822,
        )

        return self.__parent__._cast(
            _5822.AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5829.BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5829,
        )

        return self.__parent__._cast(
            _5829.BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5834.BevelGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5834,
        )

        return self.__parent__._cast(
            _5834.BevelGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def concept_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5847.ConceptGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5847,
        )

        return self.__parent__._cast(
            _5847.ConceptGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def conical_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5850.ConicalGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5850,
        )

        return self.__parent__._cast(
            _5850.ConicalGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def cylindrical_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5865.CylindricalGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5865,
        )

        return self.__parent__._cast(
            _5865.CylindricalGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def face_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5871.FaceGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5871,
        )

        return self.__parent__._cast(
            _5871.FaceGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def hypoid_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5880.HypoidGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5880,
        )

        return self.__parent__._cast(
            _5880.HypoidGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> (
        "_5884.KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5884,
        )

        return self.__parent__._cast(
            _5884.KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> (
        "_5887.KlingelnbergCycloPalloidHypoidGearMeshCompoundMultibodyDynamicsAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5887,
        )

        return self.__parent__._cast(
            _5887.KlingelnbergCycloPalloidHypoidGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5890.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5890,
        )

        return self.__parent__._cast(
            _5890.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5919.SpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5919,
        )

        return self.__parent__._cast(
            _5919.SpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5925.StraightBevelDiffGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5925,
        )

        return self.__parent__._cast(
            _5925.StraightBevelDiffGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5928.StraightBevelGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5928,
        )

        return self.__parent__._cast(
            _5928.StraightBevelGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def worm_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5943.WormGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5943,
        )

        return self.__parent__._cast(
            _5943.WormGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def zerol_bevel_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5946.ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5946,
        )

        return self.__parent__._cast(
            _5946.ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "GearMeshCompoundMultibodyDynamicsAnalysis":
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
class GearMeshCompoundMultibodyDynamicsAnalysis(
    _5882.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
):
    """GearMeshCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

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
    ) -> "List[_5721.GearMeshMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.GearMeshMultibodyDynamicsAnalysis]

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
    ) -> "List[_5721.GearMeshMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.GearMeshMultibodyDynamicsAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_GearMeshCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearMeshCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_GearMeshCompoundMultibodyDynamicsAnalysis(self)
