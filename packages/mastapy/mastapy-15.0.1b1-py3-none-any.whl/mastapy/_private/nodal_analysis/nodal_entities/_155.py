"""NodalEntity"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_NODAL_ENTITY = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "NodalEntity"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _130,
        _131,
        _132,
        _133,
        _134,
        _135,
        _136,
        _138,
        _139,
        _140,
        _141,
        _142,
        _143,
        _144,
        _145,
        _146,
        _147,
        _148,
        _149,
        _150,
        _151,
        _152,
        _153,
        _154,
        _156,
        _157,
        _158,
        _159,
        _160,
        _161,
        _162,
        _163,
        _164,
        _165,
        _166,
        _167,
        _168,
        _169,
        _170,
    )
    from mastapy._private.nodal_analysis.nodal_entities.external_force import (
        _171,
        _172,
        _173,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3046,
    )

    Self = TypeVar("Self", bound="NodalEntity")
    CastSelf = TypeVar("CastSelf", bound="NodalEntity._Cast_NodalEntity")


__docformat__ = "restructuredtext en"
__all__ = ("NodalEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalEntity:
    """Special nested class for casting NodalEntity to subclasses."""

    __parent__: "NodalEntity"

    @property
    def arbitrary_nodal_component(self: "CastSelf") -> "_130.ArbitraryNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _130

        return self.__parent__._cast(_130.ArbitraryNodalComponent)

    @property
    def arbitrary_nodal_component_base(
        self: "CastSelf",
    ) -> "_131.ArbitraryNodalComponentBase":
        from mastapy._private.nodal_analysis.nodal_entities import _131

        return self.__parent__._cast(_131.ArbitraryNodalComponentBase)

    @property
    def bar(self: "CastSelf") -> "_132.Bar":
        from mastapy._private.nodal_analysis.nodal_entities import _132

        return self.__parent__._cast(_132.Bar)

    @property
    def bar_base(self: "CastSelf") -> "_133.BarBase":
        from mastapy._private.nodal_analysis.nodal_entities import _133

        return self.__parent__._cast(_133.BarBase)

    @property
    def bar_elastic_mbd(self: "CastSelf") -> "_134.BarElasticMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _134

        return self.__parent__._cast(_134.BarElasticMBD)

    @property
    def bar_mbd(self: "CastSelf") -> "_135.BarMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _135

        return self.__parent__._cast(_135.BarMBD)

    @property
    def bar_rigid_mbd(self: "CastSelf") -> "_136.BarRigidMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _136

        return self.__parent__._cast(_136.BarRigidMBD)

    @property
    def bearing_axial_mounting_clearance(
        self: "CastSelf",
    ) -> "_138.BearingAxialMountingClearance":
        from mastapy._private.nodal_analysis.nodal_entities import _138

        return self.__parent__._cast(_138.BearingAxialMountingClearance)

    @property
    def cms_nodal_component(self: "CastSelf") -> "_139.CMSNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _139

        return self.__parent__._cast(_139.CMSNodalComponent)

    @property
    def component_nodal_composite(self: "CastSelf") -> "_140.ComponentNodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _140

        return self.__parent__._cast(_140.ComponentNodalComposite)

    @property
    def component_nodal_composite_base(
        self: "CastSelf",
    ) -> "_141.ComponentNodalCompositeBase":
        from mastapy._private.nodal_analysis.nodal_entities import _141

        return self.__parent__._cast(_141.ComponentNodalCompositeBase)

    @property
    def concentric_connection_nodal_component(
        self: "CastSelf",
    ) -> "_142.ConcentricConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _142

        return self.__parent__._cast(_142.ConcentricConnectionNodalComponent)

    @property
    def concentric_connection_nodal_component_base(
        self: "CastSelf",
    ) -> "_143.ConcentricConnectionNodalComponentBase":
        from mastapy._private.nodal_analysis.nodal_entities import _143

        return self.__parent__._cast(_143.ConcentricConnectionNodalComponentBase)

    @property
    def distributed_rigid_bar_coupling(
        self: "CastSelf",
    ) -> "_144.DistributedRigidBarCoupling":
        from mastapy._private.nodal_analysis.nodal_entities import _144

        return self.__parent__._cast(_144.DistributedRigidBarCoupling)

    @property
    def flow_junction_nodal_component(
        self: "CastSelf",
    ) -> "_145.FlowJunctionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _145

        return self.__parent__._cast(_145.FlowJunctionNodalComponent)

    @property
    def friction_nodal_component(self: "CastSelf") -> "_146.FrictionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _146

        return self.__parent__._cast(_146.FrictionNodalComponent)

    @property
    def gear_mesh_nodal_component(self: "CastSelf") -> "_147.GearMeshNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _147

        return self.__parent__._cast(_147.GearMeshNodalComponent)

    @property
    def gear_mesh_node_pair(self: "CastSelf") -> "_148.GearMeshNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _148

        return self.__parent__._cast(_148.GearMeshNodePair)

    @property
    def gear_mesh_point_on_flank_contact(
        self: "CastSelf",
    ) -> "_149.GearMeshPointOnFlankContact":
        from mastapy._private.nodal_analysis.nodal_entities import _149

        return self.__parent__._cast(_149.GearMeshPointOnFlankContact)

    @property
    def gear_mesh_single_flank_contact(
        self: "CastSelf",
    ) -> "_150.GearMeshSingleFlankContact":
        from mastapy._private.nodal_analysis.nodal_entities import _150

        return self.__parent__._cast(_150.GearMeshSingleFlankContact)

    @property
    def inertial_force_component(self: "CastSelf") -> "_151.InertialForceComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _151

        return self.__parent__._cast(_151.InertialForceComponent)

    @property
    def line_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_152.LineContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _152

        return self.__parent__._cast(_152.LineContactStiffnessEntity)

    @property
    def nodal_component(self: "CastSelf") -> "_153.NodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _153

        return self.__parent__._cast(_153.NodalComponent)

    @property
    def nodal_composite(self: "CastSelf") -> "_154.NodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _154

        return self.__parent__._cast(_154.NodalComposite)

    @property
    def null_nodal_entity(self: "CastSelf") -> "_156.NullNodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _156

        return self.__parent__._cast(_156.NullNodalEntity)

    @property
    def pid_control_nodal_component(
        self: "CastSelf",
    ) -> "_157.PIDControlNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _157

        return self.__parent__._cast(_157.PIDControlNodalComponent)

    @property
    def pressure_and_volumetric_flow_rate_nodal_component_v2(
        self: "CastSelf",
    ) -> "_158.PressureAndVolumetricFlowRateNodalComponentV2":
        from mastapy._private.nodal_analysis.nodal_entities import _158

        return self.__parent__._cast(_158.PressureAndVolumetricFlowRateNodalComponentV2)

    @property
    def pressure_constraint_nodal_component(
        self: "CastSelf",
    ) -> "_159.PressureConstraintNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _159

        return self.__parent__._cast(_159.PressureConstraintNodalComponent)

    @property
    def rigid_bar(self: "CastSelf") -> "_160.RigidBar":
        from mastapy._private.nodal_analysis.nodal_entities import _160

        return self.__parent__._cast(_160.RigidBar)

    @property
    def simple_bar(self: "CastSelf") -> "_161.SimpleBar":
        from mastapy._private.nodal_analysis.nodal_entities import _161

        return self.__parent__._cast(_161.SimpleBar)

    @property
    def spline_contact_nodal_component(
        self: "CastSelf",
    ) -> "_162.SplineContactNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _162

        return self.__parent__._cast(_162.SplineContactNodalComponent)

    @property
    def surface_to_surface_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_163.SurfaceToSurfaceContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _163

        return self.__parent__._cast(_163.SurfaceToSurfaceContactStiffnessEntity)

    @property
    def temperature_constraint(self: "CastSelf") -> "_164.TemperatureConstraint":
        from mastapy._private.nodal_analysis.nodal_entities import _164

        return self.__parent__._cast(_164.TemperatureConstraint)

    @property
    def thermal_connector_with_resistance_nodal_component(
        self: "CastSelf",
    ) -> "_165.ThermalConnectorWithResistanceNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _165

        return self.__parent__._cast(_165.ThermalConnectorWithResistanceNodalComponent)

    @property
    def thermal_nodal_component(self: "CastSelf") -> "_166.ThermalNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _166

        return self.__parent__._cast(_166.ThermalNodalComponent)

    @property
    def torsional_friction_node_pair(
        self: "CastSelf",
    ) -> "_167.TorsionalFrictionNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _167

        return self.__parent__._cast(_167.TorsionalFrictionNodePair)

    @property
    def torsional_friction_node_pair_base(
        self: "CastSelf",
    ) -> "_168.TorsionalFrictionNodePairBase":
        from mastapy._private.nodal_analysis.nodal_entities import _168

        return self.__parent__._cast(_168.TorsionalFrictionNodePairBase)

    @property
    def torsional_friction_node_pair_simple_locked_stiffness(
        self: "CastSelf",
    ) -> "_169.TorsionalFrictionNodePairSimpleLockedStiffness":
        from mastapy._private.nodal_analysis.nodal_entities import _169

        return self.__parent__._cast(
            _169.TorsionalFrictionNodePairSimpleLockedStiffness
        )

    @property
    def two_body_connection_nodal_component(
        self: "CastSelf",
    ) -> "_170.TwoBodyConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _170

        return self.__parent__._cast(_170.TwoBodyConnectionNodalComponent)

    @property
    def external_force_entity(self: "CastSelf") -> "_171.ExternalForceEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _171

        return self.__parent__._cast(_171.ExternalForceEntity)

    @property
    def external_force_line_contact_entity(
        self: "CastSelf",
    ) -> "_172.ExternalForceLineContactEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _172

        return self.__parent__._cast(_172.ExternalForceLineContactEntity)

    @property
    def external_force_single_point_entity(
        self: "CastSelf",
    ) -> "_173.ExternalForceSinglePointEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _173

        return self.__parent__._cast(_173.ExternalForceSinglePointEntity)

    @property
    def shaft_section_system_deflection(
        self: "CastSelf",
    ) -> "_3046.ShaftSectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3046,
        )

        return self.__parent__._cast(_3046.ShaftSectionSystemDeflection)

    @property
    def nodal_entity(self: "CastSelf") -> "NodalEntity":
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
class NodalEntity(_0.APIBase):
    """NodalEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_NodalEntity":
        """Cast to another type.

        Returns:
            _Cast_NodalEntity
        """
        return _Cast_NodalEntity(self)
