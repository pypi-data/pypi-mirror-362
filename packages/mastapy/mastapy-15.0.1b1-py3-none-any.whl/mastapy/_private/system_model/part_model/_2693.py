"""MountableComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2670

_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import (
        _2490,
        _2493,
        _2497,
    )
    from mastapy._private.system_model.part_model import (
        _2660,
        _2664,
        _2671,
        _2673,
        _2689,
        _2690,
        _2695,
        _2698,
        _2700,
        _2702,
        _2703,
        _2709,
        _2711,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2818,
        _2821,
        _2824,
        _2827,
        _2829,
        _2831,
        _2838,
        _2840,
        _2847,
        _2850,
        _2851,
        _2852,
        _2854,
        _2856,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2808
    from mastapy._private.system_model.part_model.gears import (
        _2750,
        _2752,
        _2754,
        _2755,
        _2756,
        _2758,
        _2760,
        _2762,
        _2764,
        _2765,
        _2767,
        _2771,
        _2773,
        _2775,
        _2777,
        _2781,
        _2783,
        _2785,
        _2787,
        _2788,
        _2789,
        _2791,
    )

    Self = TypeVar("Self", bound="MountableComponent")
    CastSelf = TypeVar("CastSelf", bound="MountableComponent._Cast_MountableComponent")


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponent:
    """Special nested class for casting MountableComponent to subclasses."""

    __parent__: "MountableComponent"

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        return self.__parent__._cast(_2670.Component)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def bearing(self: "CastSelf") -> "_2664.Bearing":
        from mastapy._private.system_model.part_model import _2664

        return self.__parent__._cast(_2664.Bearing)

    @property
    def connector(self: "CastSelf") -> "_2673.Connector":
        from mastapy._private.system_model.part_model import _2673

        return self.__parent__._cast(_2673.Connector)

    @property
    def mass_disc(self: "CastSelf") -> "_2689.MassDisc":
        from mastapy._private.system_model.part_model import _2689

        return self.__parent__._cast(_2689.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2690.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2690

        return self.__parent__._cast(_2690.MeasurementComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2695.OilSeal":
        from mastapy._private.system_model.part_model import _2695

        return self.__parent__._cast(_2695.OilSeal)

    @property
    def planet_carrier(self: "CastSelf") -> "_2700.PlanetCarrier":
        from mastapy._private.system_model.part_model import _2700

        return self.__parent__._cast(_2700.PlanetCarrier)

    @property
    def point_load(self: "CastSelf") -> "_2702.PointLoad":
        from mastapy._private.system_model.part_model import _2702

        return self.__parent__._cast(_2702.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2703.PowerLoad":
        from mastapy._private.system_model.part_model import _2703

        return self.__parent__._cast(_2703.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2709.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2709

        return self.__parent__._cast(_2709.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2711.VirtualComponent":
        from mastapy._private.system_model.part_model import _2711

        return self.__parent__._cast(_2711.VirtualComponent)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2750.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2750

        return self.__parent__._cast(_2750.AGMAGleasonConicalGear)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2752.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2752

        return self.__parent__._cast(_2752.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2754.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2754

        return self.__parent__._cast(_2754.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2755.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2755

        return self.__parent__._cast(_2755.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2756.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2756

        return self.__parent__._cast(_2756.BevelGear)

    @property
    def concept_gear(self: "CastSelf") -> "_2758.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2758

        return self.__parent__._cast(_2758.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2760.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2760

        return self.__parent__._cast(_2760.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2762.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2762

        return self.__parent__._cast(_2762.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2764.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2764

        return self.__parent__._cast(_2764.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2765.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2765

        return self.__parent__._cast(_2765.FaceGear)

    @property
    def gear(self: "CastSelf") -> "_2767.Gear":
        from mastapy._private.system_model.part_model.gears import _2767

        return self.__parent__._cast(_2767.Gear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2771.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2771

        return self.__parent__._cast(_2771.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2773.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2773

        return self.__parent__._cast(_2773.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2775.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2775

        return self.__parent__._cast(_2775.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2777.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2777

        return self.__parent__._cast(_2777.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2781.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2781

        return self.__parent__._cast(_2781.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2783.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2783

        return self.__parent__._cast(_2783.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2785.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2785

        return self.__parent__._cast(_2785.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2787.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2787

        return self.__parent__._cast(_2787.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2788.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2788

        return self.__parent__._cast(_2788.StraightBevelSunGear)

    @property
    def worm_gear(self: "CastSelf") -> "_2789.WormGear":
        from mastapy._private.system_model.part_model.gears import _2789

        return self.__parent__._cast(_2789.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2791.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2791

        return self.__parent__._cast(_2791.ZerolBevelGear)

    @property
    def ring_pins(self: "CastSelf") -> "_2808.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2808

        return self.__parent__._cast(_2808.RingPins)

    @property
    def clutch_half(self: "CastSelf") -> "_2818.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2818

        return self.__parent__._cast(_2818.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2821.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2821

        return self.__parent__._cast(_2821.ConceptCouplingHalf)

    @property
    def coupling_half(self: "CastSelf") -> "_2824.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2824

        return self.__parent__._cast(_2824.CouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2827.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2827

        return self.__parent__._cast(_2827.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2829.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2829

        return self.__parent__._cast(_2829.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2831.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2831

        return self.__parent__._cast(_2831.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2838.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2838

        return self.__parent__._cast(_2838.RollingRing)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2840.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2840

        return self.__parent__._cast(_2840.ShaftHubConnection)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2847.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2847

        return self.__parent__._cast(_2847.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2850.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2850

        return self.__parent__._cast(_2850.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2851.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2851

        return self.__parent__._cast(_2851.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2852.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2852

        return self.__parent__._cast(_2852.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2854.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2854

        return self.__parent__._cast(_2854.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2856.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2856

        return self.__parent__._cast(_2856.TorqueConverterTurbine)

    @property
    def mountable_component(self: "CastSelf") -> "MountableComponent":
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
class MountableComponent(_2670.Component):
    """MountableComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def rotation_about_axis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAboutAxis")

        if temp is None:
            return 0.0

        return temp

    @rotation_about_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def rotation_about_axis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotationAboutAxis",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def inner_component(self: "Self") -> "_2660.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_connection(self: "Self") -> "_2493.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_socket(self: "Self") -> "_2497.CylindricalSocket":
        """mastapy.system_model.connections_and_sockets.CylindricalSocket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSocket")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def is_mounted(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsMounted")

        if temp is None:
            return False

        return temp

    @exception_bridge
    @enforce_parameter_types
    def mount_on(
        self: "Self", shaft: "_2660.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2490.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def try_mount_on(
        self: "Self", shaft: "_2660.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2671.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryMountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponent":
        """Cast to another type.

        Returns:
            _Cast_MountableComponent
        """
        return _Cast_MountableComponent(self)
