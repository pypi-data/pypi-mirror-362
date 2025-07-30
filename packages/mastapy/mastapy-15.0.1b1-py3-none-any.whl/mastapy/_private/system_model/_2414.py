"""DesignEntity"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
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

_DESIGN_ENTITY = python_net_import("SMT.MastaAPI.SystemModel", "DesignEntity")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model import _2411
    from mastapy._private.system_model.connections_and_sockets import (
        _2486,
        _2489,
        _2490,
        _2493,
        _2494,
        _2502,
        _2508,
        _2513,
        _2516,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2563,
        _2565,
        _2567,
        _2569,
        _2571,
        _2573,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2556,
        _2559,
        _2562,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2520,
        _2522,
        _2524,
        _2526,
        _2528,
        _2530,
        _2532,
        _2534,
        _2536,
        _2539,
        _2540,
        _2541,
        _2544,
        _2546,
        _2548,
        _2550,
        _2552,
    )
    from mastapy._private.system_model.part_model import (
        _2658,
        _2659,
        _2660,
        _2661,
        _2664,
        _2667,
        _2668,
        _2670,
        _2673,
        _2674,
        _2679,
        _2680,
        _2681,
        _2682,
        _2689,
        _2690,
        _2691,
        _2692,
        _2693,
        _2695,
        _2698,
        _2700,
        _2702,
        _2703,
        _2706,
        _2708,
        _2709,
        _2711,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2815,
        _2817,
        _2818,
        _2820,
        _2821,
        _2823,
        _2824,
        _2826,
        _2827,
        _2828,
        _2829,
        _2831,
        _2838,
        _2839,
        _2840,
        _2846,
        _2847,
        _2848,
        _2850,
        _2851,
        _2852,
        _2853,
        _2854,
        _2856,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2806, _2807, _2808
    from mastapy._private.system_model.part_model.gears import (
        _2750,
        _2751,
        _2752,
        _2753,
        _2754,
        _2755,
        _2756,
        _2757,
        _2758,
        _2759,
        _2760,
        _2761,
        _2762,
        _2763,
        _2764,
        _2765,
        _2766,
        _2767,
        _2769,
        _2771,
        _2772,
        _2773,
        _2774,
        _2775,
        _2776,
        _2777,
        _2778,
        _2779,
        _2781,
        _2782,
        _2783,
        _2784,
        _2785,
        _2786,
        _2787,
        _2788,
        _2789,
        _2790,
        _2791,
        _2792,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2714
    from mastapy._private.utility.model_validation import _1988, _1989
    from mastapy._private.utility.scripting import _1936

    Self = TypeVar("Self", bound="DesignEntity")
    CastSelf = TypeVar("CastSelf", bound="DesignEntity._Cast_DesignEntity")


__docformat__ = "restructuredtext en"
__all__ = ("DesignEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignEntity:
    """Special nested class for casting DesignEntity to subclasses."""

    __parent__: "DesignEntity"

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2486.AbstractShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2486

        return self.__parent__._cast(_2486.AbstractShaftToMountableComponentConnection)

    @property
    def belt_connection(self: "CastSelf") -> "_2489.BeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2489

        return self.__parent__._cast(_2489.BeltConnection)

    @property
    def coaxial_connection(self: "CastSelf") -> "_2490.CoaxialConnection":
        from mastapy._private.system_model.connections_and_sockets import _2490

        return self.__parent__._cast(_2490.CoaxialConnection)

    @property
    def connection(self: "CastSelf") -> "_2493.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2493

        return self.__parent__._cast(_2493.Connection)

    @property
    def cvt_belt_connection(self: "CastSelf") -> "_2494.CVTBeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2494

        return self.__parent__._cast(_2494.CVTBeltConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2502.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2502

        return self.__parent__._cast(_2502.InterMountableComponentConnection)

    @property
    def planetary_connection(self: "CastSelf") -> "_2508.PlanetaryConnection":
        from mastapy._private.system_model.connections_and_sockets import _2508

        return self.__parent__._cast(_2508.PlanetaryConnection)

    @property
    def rolling_ring_connection(self: "CastSelf") -> "_2513.RollingRingConnection":
        from mastapy._private.system_model.connections_and_sockets import _2513

        return self.__parent__._cast(_2513.RollingRingConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2516.ShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2516

        return self.__parent__._cast(_2516.ShaftToMountableComponentConnection)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2520.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2520

        return self.__parent__._cast(_2520.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2522.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2522

        return self.__parent__._cast(_2522.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2524.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2524

        return self.__parent__._cast(_2524.BevelGearMesh)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "_2526.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2526

        return self.__parent__._cast(_2526.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2528.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2528

        return self.__parent__._cast(_2528.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2530.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2530

        return self.__parent__._cast(_2530.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2532.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2532

        return self.__parent__._cast(_2532.FaceGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2534.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2534

        return self.__parent__._cast(_2534.GearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2536.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2536

        return self.__parent__._cast(_2536.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2539.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2539

        return self.__parent__._cast(_2539.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2540.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2540

        return self.__parent__._cast(_2540.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2541.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2541

        return self.__parent__._cast(_2541.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2544.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2544

        return self.__parent__._cast(_2544.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2546.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2546

        return self.__parent__._cast(_2546.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2548.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2548

        return self.__parent__._cast(_2548.StraightBevelGearMesh)

    @property
    def worm_gear_mesh(self: "CastSelf") -> "_2550.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2550

        return self.__parent__._cast(_2550.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2552.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2552

        return self.__parent__._cast(_2552.ZerolBevelGearMesh)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2556.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2556,
        )

        return self.__parent__._cast(_2556.CycloidalDiscCentralBearingConnection)

    @property
    def cycloidal_disc_planetary_bearing_connection(
        self: "CastSelf",
    ) -> "_2559.CycloidalDiscPlanetaryBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2559,
        )

        return self.__parent__._cast(_2559.CycloidalDiscPlanetaryBearingConnection)

    @property
    def ring_pins_to_disc_connection(
        self: "CastSelf",
    ) -> "_2562.RingPinsToDiscConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2562,
        )

        return self.__parent__._cast(_2562.RingPinsToDiscConnection)

    @property
    def clutch_connection(self: "CastSelf") -> "_2563.ClutchConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2563,
        )

        return self.__parent__._cast(_2563.ClutchConnection)

    @property
    def concept_coupling_connection(
        self: "CastSelf",
    ) -> "_2565.ConceptCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2565,
        )

        return self.__parent__._cast(_2565.ConceptCouplingConnection)

    @property
    def coupling_connection(self: "CastSelf") -> "_2567.CouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2567,
        )

        return self.__parent__._cast(_2567.CouplingConnection)

    @property
    def part_to_part_shear_coupling_connection(
        self: "CastSelf",
    ) -> "_2569.PartToPartShearCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2569,
        )

        return self.__parent__._cast(_2569.PartToPartShearCouplingConnection)

    @property
    def spring_damper_connection(self: "CastSelf") -> "_2571.SpringDamperConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2571,
        )

        return self.__parent__._cast(_2571.SpringDamperConnection)

    @property
    def torque_converter_connection(
        self: "CastSelf",
    ) -> "_2573.TorqueConverterConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2573,
        )

        return self.__parent__._cast(_2573.TorqueConverterConnection)

    @property
    def assembly(self: "CastSelf") -> "_2658.Assembly":
        from mastapy._private.system_model.part_model import _2658

        return self.__parent__._cast(_2658.Assembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2659

        return self.__parent__._cast(_2659.AbstractAssembly)

    @property
    def abstract_shaft(self: "CastSelf") -> "_2660.AbstractShaft":
        from mastapy._private.system_model.part_model import _2660

        return self.__parent__._cast(_2660.AbstractShaft)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2661.AbstractShaftOrHousing":
        from mastapy._private.system_model.part_model import _2661

        return self.__parent__._cast(_2661.AbstractShaftOrHousing)

    @property
    def bearing(self: "CastSelf") -> "_2664.Bearing":
        from mastapy._private.system_model.part_model import _2664

        return self.__parent__._cast(_2664.Bearing)

    @property
    def bolt(self: "CastSelf") -> "_2667.Bolt":
        from mastapy._private.system_model.part_model import _2667

        return self.__parent__._cast(_2667.Bolt)

    @property
    def bolted_joint(self: "CastSelf") -> "_2668.BoltedJoint":
        from mastapy._private.system_model.part_model import _2668

        return self.__parent__._cast(_2668.BoltedJoint)

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        from mastapy._private.system_model.part_model import _2670

        return self.__parent__._cast(_2670.Component)

    @property
    def connector(self: "CastSelf") -> "_2673.Connector":
        from mastapy._private.system_model.part_model import _2673

        return self.__parent__._cast(_2673.Connector)

    @property
    def datum(self: "CastSelf") -> "_2674.Datum":
        from mastapy._private.system_model.part_model import _2674

        return self.__parent__._cast(_2674.Datum)

    @property
    def external_cad_model(self: "CastSelf") -> "_2679.ExternalCADModel":
        from mastapy._private.system_model.part_model import _2679

        return self.__parent__._cast(_2679.ExternalCADModel)

    @property
    def fe_part(self: "CastSelf") -> "_2680.FEPart":
        from mastapy._private.system_model.part_model import _2680

        return self.__parent__._cast(_2680.FEPart)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2681.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2681

        return self.__parent__._cast(_2681.FlexiblePinAssembly)

    @property
    def guide_dxf_model(self: "CastSelf") -> "_2682.GuideDxfModel":
        from mastapy._private.system_model.part_model import _2682

        return self.__parent__._cast(_2682.GuideDxfModel)

    @property
    def mass_disc(self: "CastSelf") -> "_2689.MassDisc":
        from mastapy._private.system_model.part_model import _2689

        return self.__parent__._cast(_2689.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2690.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2690

        return self.__parent__._cast(_2690.MeasurementComponent)

    @property
    def microphone(self: "CastSelf") -> "_2691.Microphone":
        from mastapy._private.system_model.part_model import _2691

        return self.__parent__._cast(_2691.Microphone)

    @property
    def microphone_array(self: "CastSelf") -> "_2692.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2692

        return self.__parent__._cast(_2692.MicrophoneArray)

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
        from mastapy._private.system_model.part_model import _2693

        return self.__parent__._cast(_2693.MountableComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2695.OilSeal":
        from mastapy._private.system_model.part_model import _2695

        return self.__parent__._cast(_2695.OilSeal)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

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
    def root_assembly(self: "CastSelf") -> "_2706.RootAssembly":
        from mastapy._private.system_model.part_model import _2706

        return self.__parent__._cast(_2706.RootAssembly)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2708.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2708

        return self.__parent__._cast(_2708.SpecialisedAssembly)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2709.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2709

        return self.__parent__._cast(_2709.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2711.VirtualComponent":
        from mastapy._private.system_model.part_model import _2711

        return self.__parent__._cast(_2711.VirtualComponent)

    @property
    def shaft(self: "CastSelf") -> "_2714.Shaft":
        from mastapy._private.system_model.part_model.shaft_model import _2714

        return self.__parent__._cast(_2714.Shaft)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2750.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2750

        return self.__parent__._cast(_2750.AGMAGleasonConicalGear)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2751.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2751

        return self.__parent__._cast(_2751.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2752.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2752

        return self.__parent__._cast(_2752.BevelDifferentialGear)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2753.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2753

        return self.__parent__._cast(_2753.BevelDifferentialGearSet)

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
    def bevel_gear_set(self: "CastSelf") -> "_2757.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2757

        return self.__parent__._cast(_2757.BevelGearSet)

    @property
    def concept_gear(self: "CastSelf") -> "_2758.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2758

        return self.__parent__._cast(_2758.ConceptGear)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2759.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2759

        return self.__parent__._cast(_2759.ConceptGearSet)

    @property
    def conical_gear(self: "CastSelf") -> "_2760.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2760

        return self.__parent__._cast(_2760.ConicalGear)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2761.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2761

        return self.__parent__._cast(_2761.ConicalGearSet)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2762.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2762

        return self.__parent__._cast(_2762.CylindricalGear)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2763.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2763

        return self.__parent__._cast(_2763.CylindricalGearSet)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2764.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2764

        return self.__parent__._cast(_2764.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2765.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2765

        return self.__parent__._cast(_2765.FaceGear)

    @property
    def face_gear_set(self: "CastSelf") -> "_2766.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2766

        return self.__parent__._cast(_2766.FaceGearSet)

    @property
    def gear(self: "CastSelf") -> "_2767.Gear":
        from mastapy._private.system_model.part_model.gears import _2767

        return self.__parent__._cast(_2767.Gear)

    @property
    def gear_set(self: "CastSelf") -> "_2769.GearSet":
        from mastapy._private.system_model.part_model.gears import _2769

        return self.__parent__._cast(_2769.GearSet)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2771.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2771

        return self.__parent__._cast(_2771.HypoidGear)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2772.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2772

        return self.__parent__._cast(_2772.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2773.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2773

        return self.__parent__._cast(_2773.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2774.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2774

        return self.__parent__._cast(_2774.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2775.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2775

        return self.__parent__._cast(_2775.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2776.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2776

        return self.__parent__._cast(_2776.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2777.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2777

        return self.__parent__._cast(_2777.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2778.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2778

        return self.__parent__._cast(_2778.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2779.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2779

        return self.__parent__._cast(_2779.PlanetaryGearSet)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2781.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2781

        return self.__parent__._cast(_2781.SpiralBevelGear)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2782.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2782

        return self.__parent__._cast(_2782.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2783.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2783

        return self.__parent__._cast(_2783.StraightBevelDiffGear)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2784.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2784

        return self.__parent__._cast(_2784.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2785.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2785

        return self.__parent__._cast(_2785.StraightBevelGear)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2786.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2786

        return self.__parent__._cast(_2786.StraightBevelGearSet)

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
    def worm_gear_set(self: "CastSelf") -> "_2790.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2790

        return self.__parent__._cast(_2790.WormGearSet)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2791.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2791

        return self.__parent__._cast(_2791.ZerolBevelGear)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2792.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2792

        return self.__parent__._cast(_2792.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2806.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2806

        return self.__parent__._cast(_2806.CycloidalAssembly)

    @property
    def cycloidal_disc(self: "CastSelf") -> "_2807.CycloidalDisc":
        from mastapy._private.system_model.part_model.cycloidal import _2807

        return self.__parent__._cast(_2807.CycloidalDisc)

    @property
    def ring_pins(self: "CastSelf") -> "_2808.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2808

        return self.__parent__._cast(_2808.RingPins)

    @property
    def belt_drive(self: "CastSelf") -> "_2815.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2815

        return self.__parent__._cast(_2815.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2817.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2817

        return self.__parent__._cast(_2817.Clutch)

    @property
    def clutch_half(self: "CastSelf") -> "_2818.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2818

        return self.__parent__._cast(_2818.ClutchHalf)

    @property
    def concept_coupling(self: "CastSelf") -> "_2820.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2820

        return self.__parent__._cast(_2820.ConceptCoupling)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2821.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2821

        return self.__parent__._cast(_2821.ConceptCouplingHalf)

    @property
    def coupling(self: "CastSelf") -> "_2823.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2823

        return self.__parent__._cast(_2823.Coupling)

    @property
    def coupling_half(self: "CastSelf") -> "_2824.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2824

        return self.__parent__._cast(_2824.CouplingHalf)

    @property
    def cvt(self: "CastSelf") -> "_2826.CVT":
        from mastapy._private.system_model.part_model.couplings import _2826

        return self.__parent__._cast(_2826.CVT)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2827.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2827

        return self.__parent__._cast(_2827.CVTPulley)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2828.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2828

        return self.__parent__._cast(_2828.PartToPartShearCoupling)

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
    def rolling_ring_assembly(self: "CastSelf") -> "_2839.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2839

        return self.__parent__._cast(_2839.RollingRingAssembly)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2840.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2840

        return self.__parent__._cast(_2840.ShaftHubConnection)

    @property
    def spring_damper(self: "CastSelf") -> "_2846.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2846

        return self.__parent__._cast(_2846.SpringDamper)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2847.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2847

        return self.__parent__._cast(_2847.SpringDamperHalf)

    @property
    def synchroniser(self: "CastSelf") -> "_2848.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2848

        return self.__parent__._cast(_2848.Synchroniser)

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
    def torque_converter(self: "CastSelf") -> "_2853.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2853

        return self.__parent__._cast(_2853.TorqueConverter)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2854.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2854

        return self.__parent__._cast(_2854.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2856.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2856

        return self.__parent__._cast(_2856.TorqueConverterTurbine)

    @property
    def design_entity(self: "CastSelf") -> "DesignEntity":
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
class DesignEntity(_0.APIBase):
    """DesignEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @exception_bridge
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def full_name_without_root_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullNameWithoutRootName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Icon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def small_icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallIcon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def unique_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UniqueName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def design_properties(self: "Self") -> "_2411.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def all_design_entities(self: "Self") -> "List[DesignEntity]":
        """List[mastapy.system_model.DesignEntity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllDesignEntities")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def all_status_errors(self: "Self") -> "List[_1989.StatusItem]":
        """List[mastapy.utility.model_validation.StatusItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllStatusErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def status(self: "Self") -> "_1988.Status":
        """mastapy.utility.model_validation.Status

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def user_specified_data(self: "Self") -> "_1936.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DesignEntity":
        """Cast to another type.

        Returns:
            _Cast_DesignEntity
        """
        return _Cast_DesignEntity(self)
