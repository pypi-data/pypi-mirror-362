"""AbstractPeriodicExcitationDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ABSTRACT_PERIODIC_EXCITATION_DETAIL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "AbstractPeriodicExcitationDetail",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import _1564
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6024,
        _6025,
        _6026,
        _6027,
        _6028,
        _6029,
        _6030,
        _6031,
        _6032,
        _6033,
        _6034,
        _6035,
        _6045,
        _6047,
        _6048,
        _6050,
        _6088,
        _6105,
        _6131,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
        _6149,
    )

    Self = TypeVar("Self", bound="AbstractPeriodicExcitationDetail")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractPeriodicExcitationDetail._Cast_AbstractPeriodicExcitationDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractPeriodicExcitationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractPeriodicExcitationDetail:
    """Special nested class for casting AbstractPeriodicExcitationDetail to subclasses."""

    __parent__: "AbstractPeriodicExcitationDetail"

    @property
    def electric_machine_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_6024.ElectricMachinePeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6024,
        )

        return self.__parent__._cast(_6024.ElectricMachinePeriodicExcitationDetail)

    @property
    def electric_machine_rotor_x_force_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_6025.ElectricMachineRotorXForcePeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6025,
        )

        return self.__parent__._cast(
            _6025.ElectricMachineRotorXForcePeriodicExcitationDetail
        )

    @property
    def electric_machine_rotor_x_moment_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_6026.ElectricMachineRotorXMomentPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6026,
        )

        return self.__parent__._cast(
            _6026.ElectricMachineRotorXMomentPeriodicExcitationDetail
        )

    @property
    def electric_machine_rotor_y_force_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_6027.ElectricMachineRotorYForcePeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6027,
        )

        return self.__parent__._cast(
            _6027.ElectricMachineRotorYForcePeriodicExcitationDetail
        )

    @property
    def electric_machine_rotor_y_moment_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_6028.ElectricMachineRotorYMomentPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6028,
        )

        return self.__parent__._cast(
            _6028.ElectricMachineRotorYMomentPeriodicExcitationDetail
        )

    @property
    def electric_machine_rotor_z_force_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_6029.ElectricMachineRotorZForcePeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6029,
        )

        return self.__parent__._cast(
            _6029.ElectricMachineRotorZForcePeriodicExcitationDetail
        )

    @property
    def electric_machine_stator_tooth_axial_loads_excitation_detail(
        self: "CastSelf",
    ) -> "_6030.ElectricMachineStatorToothAxialLoadsExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6030,
        )

        return self.__parent__._cast(
            _6030.ElectricMachineStatorToothAxialLoadsExcitationDetail
        )

    @property
    def electric_machine_stator_tooth_loads_excitation_detail(
        self: "CastSelf",
    ) -> "_6031.ElectricMachineStatorToothLoadsExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6031,
        )

        return self.__parent__._cast(
            _6031.ElectricMachineStatorToothLoadsExcitationDetail
        )

    @property
    def electric_machine_stator_tooth_moments_excitation_detail(
        self: "CastSelf",
    ) -> "_6032.ElectricMachineStatorToothMomentsExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6032,
        )

        return self.__parent__._cast(
            _6032.ElectricMachineStatorToothMomentsExcitationDetail
        )

    @property
    def electric_machine_stator_tooth_radial_loads_excitation_detail(
        self: "CastSelf",
    ) -> "_6033.ElectricMachineStatorToothRadialLoadsExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6033,
        )

        return self.__parent__._cast(
            _6033.ElectricMachineStatorToothRadialLoadsExcitationDetail
        )

    @property
    def electric_machine_stator_tooth_tangential_loads_excitation_detail(
        self: "CastSelf",
    ) -> "_6034.ElectricMachineStatorToothTangentialLoadsExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6034,
        )

        return self.__parent__._cast(
            _6034.ElectricMachineStatorToothTangentialLoadsExcitationDetail
        )

    @property
    def electric_machine_torque_ripple_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_6035.ElectricMachineTorqueRipplePeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6035,
        )

        return self.__parent__._cast(
            _6035.ElectricMachineTorqueRipplePeriodicExcitationDetail
        )

    @property
    def gear_mesh_excitation_detail(
        self: "CastSelf",
    ) -> "_6045.GearMeshExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6045,
        )

        return self.__parent__._cast(_6045.GearMeshExcitationDetail)

    @property
    def gear_mesh_misalignment_excitation_detail(
        self: "CastSelf",
    ) -> "_6047.GearMeshMisalignmentExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6047,
        )

        return self.__parent__._cast(_6047.GearMeshMisalignmentExcitationDetail)

    @property
    def gear_mesh_te_excitation_detail(
        self: "CastSelf",
    ) -> "_6048.GearMeshTEExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6048,
        )

        return self.__parent__._cast(_6048.GearMeshTEExcitationDetail)

    @property
    def general_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_6050.GeneralPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6050,
        )

        return self.__parent__._cast(_6050.GeneralPeriodicExcitationDetail)

    @property
    def periodic_excitation_with_reference_shaft(
        self: "CastSelf",
    ) -> "_6088.PeriodicExcitationWithReferenceShaft":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6088,
        )

        return self.__parent__._cast(_6088.PeriodicExcitationWithReferenceShaft)

    @property
    def single_node_periodic_excitation_with_reference_shaft(
        self: "CastSelf",
    ) -> "_6105.SingleNodePeriodicExcitationWithReferenceShaft":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6105,
        )

        return self.__parent__._cast(
            _6105.SingleNodePeriodicExcitationWithReferenceShaft
        )

    @property
    def unbalanced_mass_excitation_detail(
        self: "CastSelf",
    ) -> "_6131.UnbalancedMassExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6131,
        )

        return self.__parent__._cast(_6131.UnbalancedMassExcitationDetail)

    @property
    def transfer_path_node_single_degreeof_freedom_excitation(
        self: "CastSelf",
    ) -> "_6149.TransferPathNodeSingleDegreeofFreedomExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
            _6149,
        )

        return self.__parent__._cast(
            _6149.TransferPathNodeSingleDegreeofFreedomExcitation
        )

    @property
    def abstract_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "AbstractPeriodicExcitationDetail":
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
class AbstractPeriodicExcitationDetail(_0.APIBase):
    """AbstractPeriodicExcitationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_PERIODIC_EXCITATION_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def harmonic_load_data(self: "Self") -> "_1564.HarmonicLoadDataBase":
        """mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicLoadData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractPeriodicExcitationDetail":
        """Cast to another type.

        Returns:
            _Cast_AbstractPeriodicExcitationDetail
        """
        return _Cast_AbstractPeriodicExcitationDetail(self)
