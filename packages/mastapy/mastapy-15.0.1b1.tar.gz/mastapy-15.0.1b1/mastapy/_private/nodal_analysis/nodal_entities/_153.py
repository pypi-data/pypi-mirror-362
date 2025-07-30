"""NodalComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _155

_NODAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "NodalComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _130,
        _131,
        _132,
        _133,
        _138,
        _139,
        _144,
        _145,
        _146,
        _148,
        _151,
        _152,
        _157,
        _158,
        _159,
        _160,
        _163,
        _164,
        _165,
        _166,
    )
    from mastapy._private.nodal_analysis.nodal_entities.external_force import (
        _171,
        _172,
        _173,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3046,
    )

    Self = TypeVar("Self", bound="NodalComponent")
    CastSelf = TypeVar("CastSelf", bound="NodalComponent._Cast_NodalComponent")


__docformat__ = "restructuredtext en"
__all__ = ("NodalComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalComponent:
    """Special nested class for casting NodalComponent to subclasses."""

    __parent__: "NodalComponent"

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        return self.__parent__._cast(_155.NodalEntity)

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
    def gear_mesh_node_pair(self: "CastSelf") -> "_148.GearMeshNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _148

        return self.__parent__._cast(_148.GearMeshNodePair)

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
    def nodal_component(self: "CastSelf") -> "NodalComponent":
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
class NodalComponent(_155.NodalEntity):
    """NodalComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NodalComponent":
        """Cast to another type.

        Returns:
            _Cast_NodalComponent
        """
        return _Cast_NodalComponent(self)
