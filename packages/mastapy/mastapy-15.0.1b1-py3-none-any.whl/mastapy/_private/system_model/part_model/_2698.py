"""Part"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model import _2414

_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility import _1702
    from mastapy._private.system_model.connections_and_sockets import _2493
    from mastapy._private.system_model.import_export import _2463
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

    Self = TypeVar("Self", bound="Part")
    CastSelf = TypeVar("CastSelf", bound="Part._Cast_Part")


__docformat__ = "restructuredtext en"
__all__ = ("Part",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Part:
    """Special nested class for casting Part to subclasses."""

    __parent__: "Part"

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def assembly(self: "CastSelf") -> "_2658.Assembly":
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
    def part(self: "CastSelf") -> "Part":
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
class Part(_2414.DesignEntity):
    """Part

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def two_d_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def two_d_drawing_full_model(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawingFullModel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_isometric_view(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThreeDIsometricView")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThreeDView")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_xy_plane_with_z_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXyPlaneWithZAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_xy_plane_with_z_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXyPlaneWithZAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_xz_plane_with_y_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXzPlaneWithYAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_xz_plane_with_y_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXzPlaneWithYAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_yz_plane_with_x_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInYzPlaneWithXAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def three_d_view_orientated_in_yz_plane_with_x_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInYzPlaneWithXAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def drawing_number(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "DrawingNumber")

        if temp is None:
            return ""

        return temp

    @drawing_number.setter
    @exception_bridge
    @enforce_parameter_types
    def drawing_number(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "DrawingNumber", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def editable_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "EditableName")

        if temp is None:
            return ""

        return temp

    @editable_name.setter
    @exception_bridge
    @enforce_parameter_types
    def editable_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "EditableName", str(value) if value is not None else ""
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
    def mass(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @mass.setter
    @exception_bridge
    @enforce_parameter_types
    def mass(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Mass", value)

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
    def use_script_to_provide_resistive_torque(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseScriptToProvideResistiveTorque")

        if temp is None:
            return False

        return temp

    @use_script_to_provide_resistive_torque.setter
    @exception_bridge
    @enforce_parameter_types
    def use_script_to_provide_resistive_torque(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseScriptToProvideResistiveTorque",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def mass_properties_from_design(self: "Self") -> "_1702.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassPropertiesFromDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mass_properties_from_design_including_planetary_duplicates(
        self: "Self",
    ) -> "_1702.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MassPropertiesFromDesignIncludingPlanetaryDuplicates"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connections(self: "Self") -> "List[_2493.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def local_connections(self: "Self") -> "List[_2493.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def connections_to(self: "Self", part: "Part") -> "List[_2493.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Args:
            part (mastapy.system_model.part_model.Part)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "ConnectionsTo", part.wrapped if part else None
            )
        )

    @exception_bridge
    @enforce_parameter_types
    def copy_to(self: "Self", container: "_2658.Assembly") -> "Part":
        """mastapy.system_model.part_model.Part

        Args:
            container (mastapy.system_model.part_model.Assembly)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "CopyTo", container.wrapped if container else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def create_geometry_export_options(self: "Self") -> "_2463.GeometryExportOptions":
        """mastapy.system_model.import_export.GeometryExportOptions"""
        method_result = pythonnet_method_call(
            self.wrapped, "CreateGeometryExportOptions"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def delete_connections(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteConnections")

    @property
    def cast_to(self: "Self") -> "_Cast_Part":
        """Cast to another type.

        Returns:
            _Cast_Part
        """
        return _Cast_Part(self)
