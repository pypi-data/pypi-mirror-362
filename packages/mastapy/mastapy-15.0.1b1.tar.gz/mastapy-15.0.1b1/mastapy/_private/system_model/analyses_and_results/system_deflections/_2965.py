"""ConicalGearMeshSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.system_deflections import _3000

_CONICAL_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "ConicalGearMeshSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1270, _1275, _1280
    from mastapy._private.gears.ltca.conical import _973
    from mastapy._private.gears.rating.conical import _630
    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7882,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4325
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2930,
        _2942,
        _2947,
        _2967,
        _2968,
        _3004,
        _3008,
        _3009,
        _3012,
        _3015,
        _3050,
        _3056,
        _3059,
        _3082,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2528

    Self = TypeVar("Self", bound="ConicalGearMeshSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMeshSystemDeflection._Cast_ConicalGearMeshSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshSystemDeflection:
    """Special nested class for casting ConicalGearMeshSystemDeflection to subclasses."""

    __parent__: "ConicalGearMeshSystemDeflection"

    @property
    def gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3000.GearMeshSystemDeflection":
        return self.__parent__._cast(_3000.GearMeshSystemDeflection)

    @property
    def inter_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3008.InterMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3008,
        )

        return self.__parent__._cast(
            _3008.InterMountableComponentConnectionSystemDeflection
        )

    @property
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2968.ConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2968,
        )

        return self.__parent__._cast(_2968.ConnectionSystemDeflection)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7882.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7882,
        )

        return self.__parent__._cast(_7882.ConnectionFEAnalysis)

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
    def agma_gleason_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2930.AGMAGleasonConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2930,
        )

        return self.__parent__._cast(_2930.AGMAGleasonConicalGearMeshSystemDeflection)

    @property
    def bevel_differential_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2942.BevelDifferentialGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2942,
        )

        return self.__parent__._cast(_2942.BevelDifferentialGearMeshSystemDeflection)

    @property
    def bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2947.BevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2947,
        )

        return self.__parent__._cast(_2947.BevelGearMeshSystemDeflection)

    @property
    def hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3004.HypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3004,
        )

        return self.__parent__._cast(_3004.HypoidGearMeshSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3009.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3009,
        )

        return self.__parent__._cast(
            _3009.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3012.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3012,
        )

        return self.__parent__._cast(
            _3012.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3015.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3015,
        )

        return self.__parent__._cast(
            _3015.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3050.SpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3050,
        )

        return self.__parent__._cast(_3050.SpiralBevelGearMeshSystemDeflection)

    @property
    def straight_bevel_diff_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3056.StraightBevelDiffGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3056,
        )

        return self.__parent__._cast(_3056.StraightBevelDiffGearMeshSystemDeflection)

    @property
    def straight_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3059.StraightBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3059,
        )

        return self.__parent__._cast(_3059.StraightBevelGearMeshSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3082.ZerolBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3082,
        )

        return self.__parent__._cast(_3082.ZerolBevelGearMeshSystemDeflection)

    @property
    def conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "ConicalGearMeshSystemDeflection":
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
class ConicalGearMeshSystemDeflection(_3000.GearMeshSystemDeflection):
    """ConicalGearMeshSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_misalignment_in_surface_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngularMisalignmentInSurfaceOfAction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def delta_e(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DeltaE")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def delta_sigma(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DeltaSigma")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def delta_xp(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DeltaXP")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def delta_xw(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DeltaXW")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def include_mesh_node_misalignments_in_default_report(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "IncludeMeshNodeMisalignmentsInDefaultReport"
        )

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def linear_misalignment_in_surface_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LinearMisalignmentInSurfaceOfAction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_in_line_of_action_from_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadInLineOfActionFromLTCA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def loaded_flank(self: "Self") -> "_1270.ActiveConicalFlank":
        """mastapy.gears.gear_designs.conical.ActiveConicalFlank

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.ActiveConicalFlank"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1270", "ActiveConicalFlank"
        )(value)

    @property
    @exception_bridge
    def pinion_angular_misalignment_in_surface_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionAngularMisalignmentInSurfaceOfAction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_torque_for_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionTorqueForLTCA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_on_gear_a_due_to_force_in_line_of_action_at_mesh_node(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TorqueOnGearADueToForceInLineOfActionAtMeshNode"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_on_gear_a_due_to_moment_at_mesh_node(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TorqueOnGearADueToMomentAtMeshNode"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_on_gear_b_due_to_force_in_line_of_action_at_mesh_node(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TorqueOnGearBDueToForceInLineOfActionAtMeshNode"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_on_gear_b_due_to_moment_at_mesh_node(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TorqueOnGearBDueToMomentAtMeshNode"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angular_misalignment_in_surface_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelAngularMisalignmentInSurfaceOfAction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2528.ConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh

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
    def gear_a(self: "Self") -> "_2967.ConicalGearSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_b(self: "Self") -> "_2967.ConicalGearSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ltca_results(self: "Self") -> "_973.ConicalMeshLoadDistributionAnalysis":
        """mastapy.gears.ltca.conical.ConicalMeshLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LTCAResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_design(self: "Self") -> "_1275.ConicalGearMeshDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_node_misalignments_pinion(
        self: "Self",
    ) -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshNodeMisalignmentsPinion")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_node_misalignments_total(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshNodeMisalignmentsTotal")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_node_misalignments_wheel(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshNodeMisalignmentsWheel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_pinion(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsPinion")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_total(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsTotal")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_wheel(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsWheel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_pinion(
        self: "Self",
    ) -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodePinion",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_total(
        self: "Self",
    ) -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeTotal",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_wheel(
        self: "Self",
    ) -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeWheel",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rating(self: "Self") -> "_630.ConicalGearMeshRating":
        """mastapy.gears.rating.conical.ConicalGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def planetaries(self: "Self") -> "List[ConicalGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConicalGearMeshSystemDeflection]

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
    def power_flow_results(self: "Self") -> "_4325.ConicalGearMeshPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.ConicalGearMeshPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearMeshSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshSystemDeflection
        """
        return _Cast_ConicalGearMeshSystemDeflection(self)
