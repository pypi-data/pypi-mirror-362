"""PartLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
    overridable,
)
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results import _2898
from mastapy._private.system_model.analyses_and_results.static_loads import _7674, _7766

_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PartLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.electric_machines.harmonic_load_data import _1564
    from mastapy._private.system_model.analyses_and_results import _2892, _2894
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7675,
        _7676,
        _7677,
        _7682,
        _7684,
        _7687,
        _7688,
        _7690,
        _7691,
        _7693,
        _7694,
        _7695,
        _7696,
        _7698,
        _7699,
        _7700,
        _7702,
        _7703,
        _7706,
        _7708,
        _7709,
        _7710,
        _7712,
        _7713,
        _7717,
        _7719,
        _7721,
        _7722,
        _7724,
        _7725,
        _7726,
        _7728,
        _7730,
        _7734,
        _7735,
        _7738,
        _7752,
        _7753,
        _7755,
        _7756,
        _7757,
        _7759,
        _7764,
        _7765,
        _7774,
        _7776,
        _7781,
        _7783,
        _7784,
        _7786,
        _7787,
        _7789,
        _7790,
        _7791,
        _7793,
        _7794,
        _7795,
        _7797,
        _7801,
        _7802,
        _7804,
        _7806,
        _7809,
        _7810,
        _7811,
        _7814,
        _7816,
        _7818,
        _7819,
        _7820,
        _7821,
        _7823,
        _7824,
        _7826,
        _7828,
        _7829,
        _7830,
        _7832,
        _7833,
        _7835,
        _7836,
        _7837,
        _7838,
        _7839,
        _7840,
        _7841,
        _7843,
        _7845,
        _7846,
        _7847,
        _7852,
        _7853,
        _7854,
        _7856,
        _7857,
        _7859,
    )
    from mastapy._private.system_model.part_model import _2698

    Self = TypeVar("Self", bound="PartLoadCase")
    CastSelf = TypeVar("CastSelf", bound="PartLoadCase._Cast_PartLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("PartLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartLoadCase:
    """Special nested class for casting PartLoadCase to subclasses."""

    __parent__: "PartLoadCase"

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        return self.__parent__._cast(_2898.PartAnalysis)

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
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_7675.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7675,
        )

        return self.__parent__._cast(_7675.AbstractAssemblyLoadCase)

    @property
    def abstract_shaft_load_case(self: "CastSelf") -> "_7676.AbstractShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7676,
        )

        return self.__parent__._cast(_7676.AbstractShaftLoadCase)

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "_7677.AbstractShaftOrHousingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7677,
        )

        return self.__parent__._cast(_7677.AbstractShaftOrHousingLoadCase)

    @property
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7682.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7682,
        )

        return self.__parent__._cast(_7682.AGMAGleasonConicalGearLoadCase)

    @property
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7684.AGMAGleasonConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7684,
        )

        return self.__parent__._cast(_7684.AGMAGleasonConicalGearSetLoadCase)

    @property
    def assembly_load_case(self: "CastSelf") -> "_7687.AssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7687,
        )

        return self.__parent__._cast(_7687.AssemblyLoadCase)

    @property
    def bearing_load_case(self: "CastSelf") -> "_7688.BearingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7688,
        )

        return self.__parent__._cast(_7688.BearingLoadCase)

    @property
    def belt_drive_load_case(self: "CastSelf") -> "_7690.BeltDriveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7690,
        )

        return self.__parent__._cast(_7690.BeltDriveLoadCase)

    @property
    def bevel_differential_gear_load_case(
        self: "CastSelf",
    ) -> "_7691.BevelDifferentialGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7691,
        )

        return self.__parent__._cast(_7691.BevelDifferentialGearLoadCase)

    @property
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7693.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7693,
        )

        return self.__parent__._cast(_7693.BevelDifferentialGearSetLoadCase)

    @property
    def bevel_differential_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7694.BevelDifferentialPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7694,
        )

        return self.__parent__._cast(_7694.BevelDifferentialPlanetGearLoadCase)

    @property
    def bevel_differential_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7695.BevelDifferentialSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7695,
        )

        return self.__parent__._cast(_7695.BevelDifferentialSunGearLoadCase)

    @property
    def bevel_gear_load_case(self: "CastSelf") -> "_7696.BevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7696,
        )

        return self.__parent__._cast(_7696.BevelGearLoadCase)

    @property
    def bevel_gear_set_load_case(self: "CastSelf") -> "_7698.BevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7698,
        )

        return self.__parent__._cast(_7698.BevelGearSetLoadCase)

    @property
    def bolted_joint_load_case(self: "CastSelf") -> "_7699.BoltedJointLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7699,
        )

        return self.__parent__._cast(_7699.BoltedJointLoadCase)

    @property
    def bolt_load_case(self: "CastSelf") -> "_7700.BoltLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7700,
        )

        return self.__parent__._cast(_7700.BoltLoadCase)

    @property
    def clutch_half_load_case(self: "CastSelf") -> "_7702.ClutchHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7702,
        )

        return self.__parent__._cast(_7702.ClutchHalfLoadCase)

    @property
    def clutch_load_case(self: "CastSelf") -> "_7703.ClutchLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7703,
        )

        return self.__parent__._cast(_7703.ClutchLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_7706.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7706,
        )

        return self.__parent__._cast(_7706.ComponentLoadCase)

    @property
    def concept_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7708.ConceptCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7708,
        )

        return self.__parent__._cast(_7708.ConceptCouplingHalfLoadCase)

    @property
    def concept_coupling_load_case(self: "CastSelf") -> "_7709.ConceptCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7709,
        )

        return self.__parent__._cast(_7709.ConceptCouplingLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_7710.ConceptGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConceptGearLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_7712.ConceptGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConceptGearSetLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_7713.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7713,
        )

        return self.__parent__._cast(_7713.ConicalGearLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_7717.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7717,
        )

        return self.__parent__._cast(_7717.ConicalGearSetLoadCase)

    @property
    def connector_load_case(self: "CastSelf") -> "_7719.ConnectorLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7719,
        )

        return self.__parent__._cast(_7719.ConnectorLoadCase)

    @property
    def coupling_half_load_case(self: "CastSelf") -> "_7721.CouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7721,
        )

        return self.__parent__._cast(_7721.CouplingHalfLoadCase)

    @property
    def coupling_load_case(self: "CastSelf") -> "_7722.CouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7722,
        )

        return self.__parent__._cast(_7722.CouplingLoadCase)

    @property
    def cvt_load_case(self: "CastSelf") -> "_7724.CVTLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7724,
        )

        return self.__parent__._cast(_7724.CVTLoadCase)

    @property
    def cvt_pulley_load_case(self: "CastSelf") -> "_7725.CVTPulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7725,
        )

        return self.__parent__._cast(_7725.CVTPulleyLoadCase)

    @property
    def cycloidal_assembly_load_case(
        self: "CastSelf",
    ) -> "_7726.CycloidalAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7726,
        )

        return self.__parent__._cast(_7726.CycloidalAssemblyLoadCase)

    @property
    def cycloidal_disc_load_case(self: "CastSelf") -> "_7728.CycloidalDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7728,
        )

        return self.__parent__._cast(_7728.CycloidalDiscLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_7730.CylindricalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7730,
        )

        return self.__parent__._cast(_7730.CylindricalGearLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7734.CylindricalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7734,
        )

        return self.__parent__._cast(_7734.CylindricalGearSetLoadCase)

    @property
    def cylindrical_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7735.CylindricalPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7735,
        )

        return self.__parent__._cast(_7735.CylindricalPlanetGearLoadCase)

    @property
    def datum_load_case(self: "CastSelf") -> "_7738.DatumLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7738,
        )

        return self.__parent__._cast(_7738.DatumLoadCase)

    @property
    def external_cad_model_load_case(
        self: "CastSelf",
    ) -> "_7752.ExternalCADModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7752,
        )

        return self.__parent__._cast(_7752.ExternalCADModelLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_7753.FaceGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7753,
        )

        return self.__parent__._cast(_7753.FaceGearLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_7755.FaceGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7755,
        )

        return self.__parent__._cast(_7755.FaceGearSetLoadCase)

    @property
    def fe_part_load_case(self: "CastSelf") -> "_7756.FEPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7756,
        )

        return self.__parent__._cast(_7756.FEPartLoadCase)

    @property
    def flexible_pin_assembly_load_case(
        self: "CastSelf",
    ) -> "_7757.FlexiblePinAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7757,
        )

        return self.__parent__._cast(_7757.FlexiblePinAssemblyLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7759.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7759,
        )

        return self.__parent__._cast(_7759.GearLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7764.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7764,
        )

        return self.__parent__._cast(_7764.GearSetLoadCase)

    @property
    def guide_dxf_model_load_case(self: "CastSelf") -> "_7765.GuideDxfModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7765,
        )

        return self.__parent__._cast(_7765.GuideDxfModelLoadCase)

    @property
    def hypoid_gear_load_case(self: "CastSelf") -> "_7774.HypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7774,
        )

        return self.__parent__._cast(_7774.HypoidGearLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7776.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7776,
        )

        return self.__parent__._cast(_7776.HypoidGearSetLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7781.KlingelnbergCycloPalloidConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7781,
        )

        return self.__parent__._cast(_7781.KlingelnbergCycloPalloidConicalGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7783.KlingelnbergCycloPalloidConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7783,
        )

        return self.__parent__._cast(
            _7783.KlingelnbergCycloPalloidConicalGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "CastSelf",
    ) -> "_7784.KlingelnbergCycloPalloidHypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7784,
        )

        return self.__parent__._cast(_7784.KlingelnbergCycloPalloidHypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7786,
        )

        return self.__parent__._cast(
            _7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7787.KlingelnbergCycloPalloidSpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7787,
        )

        return self.__parent__._cast(
            _7787.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7789,
        )

        return self.__parent__._cast(
            _7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        )

    @property
    def mass_disc_load_case(self: "CastSelf") -> "_7790.MassDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7790,
        )

        return self.__parent__._cast(_7790.MassDiscLoadCase)

    @property
    def measurement_component_load_case(
        self: "CastSelf",
    ) -> "_7791.MeasurementComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7791,
        )

        return self.__parent__._cast(_7791.MeasurementComponentLoadCase)

    @property
    def microphone_array_load_case(self: "CastSelf") -> "_7793.MicrophoneArrayLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7793,
        )

        return self.__parent__._cast(_7793.MicrophoneArrayLoadCase)

    @property
    def microphone_load_case(self: "CastSelf") -> "_7794.MicrophoneLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7794,
        )

        return self.__parent__._cast(_7794.MicrophoneLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7795.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7795,
        )

        return self.__parent__._cast(_7795.MountableComponentLoadCase)

    @property
    def oil_seal_load_case(self: "CastSelf") -> "_7797.OilSealLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7797,
        )

        return self.__parent__._cast(_7797.OilSealLoadCase)

    @property
    def part_to_part_shear_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7801.PartToPartShearCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7801,
        )

        return self.__parent__._cast(_7801.PartToPartShearCouplingHalfLoadCase)

    @property
    def part_to_part_shear_coupling_load_case(
        self: "CastSelf",
    ) -> "_7802.PartToPartShearCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7802,
        )

        return self.__parent__._cast(_7802.PartToPartShearCouplingLoadCase)

    @property
    def planetary_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7804.PlanetaryGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7804,
        )

        return self.__parent__._cast(_7804.PlanetaryGearSetLoadCase)

    @property
    def planet_carrier_load_case(self: "CastSelf") -> "_7806.PlanetCarrierLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7806,
        )

        return self.__parent__._cast(_7806.PlanetCarrierLoadCase)

    @property
    def point_load_load_case(self: "CastSelf") -> "_7809.PointLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7809,
        )

        return self.__parent__._cast(_7809.PointLoadLoadCase)

    @property
    def power_load_load_case(self: "CastSelf") -> "_7810.PowerLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7810,
        )

        return self.__parent__._cast(_7810.PowerLoadLoadCase)

    @property
    def pulley_load_case(self: "CastSelf") -> "_7811.PulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7811,
        )

        return self.__parent__._cast(_7811.PulleyLoadCase)

    @property
    def ring_pins_load_case(self: "CastSelf") -> "_7814.RingPinsLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7814,
        )

        return self.__parent__._cast(_7814.RingPinsLoadCase)

    @property
    def rolling_ring_assembly_load_case(
        self: "CastSelf",
    ) -> "_7816.RollingRingAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7816,
        )

        return self.__parent__._cast(_7816.RollingRingAssemblyLoadCase)

    @property
    def rolling_ring_load_case(self: "CastSelf") -> "_7818.RollingRingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7818,
        )

        return self.__parent__._cast(_7818.RollingRingLoadCase)

    @property
    def root_assembly_load_case(self: "CastSelf") -> "_7819.RootAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7819,
        )

        return self.__parent__._cast(_7819.RootAssemblyLoadCase)

    @property
    def shaft_hub_connection_load_case(
        self: "CastSelf",
    ) -> "_7820.ShaftHubConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7820,
        )

        return self.__parent__._cast(_7820.ShaftHubConnectionLoadCase)

    @property
    def shaft_load_case(self: "CastSelf") -> "_7821.ShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7821,
        )

        return self.__parent__._cast(_7821.ShaftLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7823.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7823,
        )

        return self.__parent__._cast(_7823.SpecialisedAssemblyLoadCase)

    @property
    def spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7824.SpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7824,
        )

        return self.__parent__._cast(_7824.SpiralBevelGearLoadCase)

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7826.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7826,
        )

        return self.__parent__._cast(_7826.SpiralBevelGearSetLoadCase)

    @property
    def spring_damper_half_load_case(
        self: "CastSelf",
    ) -> "_7828.SpringDamperHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7828,
        )

        return self.__parent__._cast(_7828.SpringDamperHalfLoadCase)

    @property
    def spring_damper_load_case(self: "CastSelf") -> "_7829.SpringDamperLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7829,
        )

        return self.__parent__._cast(_7829.SpringDamperLoadCase)

    @property
    def straight_bevel_diff_gear_load_case(
        self: "CastSelf",
    ) -> "_7830.StraightBevelDiffGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7830,
        )

        return self.__parent__._cast(_7830.StraightBevelDiffGearLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7832.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7832,
        )

        return self.__parent__._cast(_7832.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7833.StraightBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7833,
        )

        return self.__parent__._cast(_7833.StraightBevelGearLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7835.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7835,
        )

        return self.__parent__._cast(_7835.StraightBevelGearSetLoadCase)

    @property
    def straight_bevel_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7836.StraightBevelPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7836,
        )

        return self.__parent__._cast(_7836.StraightBevelPlanetGearLoadCase)

    @property
    def straight_bevel_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7837.StraightBevelSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7837,
        )

        return self.__parent__._cast(_7837.StraightBevelSunGearLoadCase)

    @property
    def synchroniser_half_load_case(
        self: "CastSelf",
    ) -> "_7838.SynchroniserHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7838,
        )

        return self.__parent__._cast(_7838.SynchroniserHalfLoadCase)

    @property
    def synchroniser_load_case(self: "CastSelf") -> "_7839.SynchroniserLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7839,
        )

        return self.__parent__._cast(_7839.SynchroniserLoadCase)

    @property
    def synchroniser_part_load_case(
        self: "CastSelf",
    ) -> "_7840.SynchroniserPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7840,
        )

        return self.__parent__._cast(_7840.SynchroniserPartLoadCase)

    @property
    def synchroniser_sleeve_load_case(
        self: "CastSelf",
    ) -> "_7841.SynchroniserSleeveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7841,
        )

        return self.__parent__._cast(_7841.SynchroniserSleeveLoadCase)

    @property
    def torque_converter_load_case(self: "CastSelf") -> "_7845.TorqueConverterLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7845,
        )

        return self.__parent__._cast(_7845.TorqueConverterLoadCase)

    @property
    def torque_converter_pump_load_case(
        self: "CastSelf",
    ) -> "_7846.TorqueConverterPumpLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7846,
        )

        return self.__parent__._cast(_7846.TorqueConverterPumpLoadCase)

    @property
    def torque_converter_turbine_load_case(
        self: "CastSelf",
    ) -> "_7847.TorqueConverterTurbineLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7847,
        )

        return self.__parent__._cast(_7847.TorqueConverterTurbineLoadCase)

    @property
    def unbalanced_mass_load_case(self: "CastSelf") -> "_7852.UnbalancedMassLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7852,
        )

        return self.__parent__._cast(_7852.UnbalancedMassLoadCase)

    @property
    def virtual_component_load_case(
        self: "CastSelf",
    ) -> "_7853.VirtualComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7853,
        )

        return self.__parent__._cast(_7853.VirtualComponentLoadCase)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_7854.WormGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7854,
        )

        return self.__parent__._cast(_7854.WormGearLoadCase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_7856.WormGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7856,
        )

        return self.__parent__._cast(_7856.WormGearSetLoadCase)

    @property
    def zerol_bevel_gear_load_case(self: "CastSelf") -> "_7857.ZerolBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7857,
        )

        return self.__parent__._cast(_7857.ZerolBevelGearLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7859.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7859,
        )

        return self.__parent__._cast(_7859.ZerolBevelGearSetLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "PartLoadCase":
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
class PartLoadCase(_2898.PartAnalysis):
    """PartLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def excitation_data_is_up_to_date(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitationDataIsUpToDate")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def harmonic_excitation_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.static_loads.HarmonicExcitationType]"""
        temp = pythonnet_property_get(self.wrapped, "HarmonicExcitationType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @harmonic_excitation_type.setter
    @exception_bridge
    @enforce_parameter_types
    def harmonic_excitation_type(
        self: "Self", value: "_7766.HarmonicExcitationType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "HarmonicExcitationType", value)

    @property
    @exception_bridge
    def load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = pythonnet_property_get(
            self.wrapped,
            "LoadCaseForHarmonicExcitationTypeAdvancedSystemDeflectionCurrentLoadCaseSetUp",
        )

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up.setter
    @exception_bridge
    @enforce_parameter_types
    def load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up(
        self: "Self", value: "_7674.StaticLoadCase"
    ) -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(
            self.wrapped,
            "LoadCaseForHarmonicExcitationTypeAdvancedSystemDeflectionCurrentLoadCaseSetUp",
            value,
        )

    @property
    @exception_bridge
    def override_resistive_torque_script(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideResistiveTorqueScript")

        if temp is None:
            return False

        return temp

    @override_resistive_torque_script.setter
    @exception_bridge
    @enforce_parameter_types
    def override_resistive_torque_script(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideResistiveTorqueScript",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_script_to_provide_resistive_torque(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "UseScriptToProvideResistiveTorque")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @use_script_to_provide_resistive_torque.setter
    @exception_bridge
    @enforce_parameter_types
    def use_script_to_provide_resistive_torque(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UseScriptToProvideResistiveTorque", value)

    @property
    @exception_bridge
    def use_this_load_case_for_advanced_system_deflection_current_load_case_set_up(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UseThisLoadCaseForAdvancedSystemDeflectionCurrentLoadCaseSetUp",
        )

        if temp is None:
            return False

        return temp

    @use_this_load_case_for_advanced_system_deflection_current_load_case_set_up.setter
    @exception_bridge
    @enforce_parameter_types
    def use_this_load_case_for_advanced_system_deflection_current_load_case_set_up(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseThisLoadCaseForAdvancedSystemDeflectionCurrentLoadCaseSetUp",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2698.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def static_load_case(self: "Self") -> "_7674.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def time_series_load_case(self: "Self") -> "_7843.TimeSeriesLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TimeSeriesLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeSeriesLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def clear_user_specified_excitation_data_for_this_load_case(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ClearUserSpecifiedExcitationDataForThisLoadCase"
        )

    @exception_bridge
    def get_harmonic_load_data_for_import(self: "Self") -> "_1564.HarmonicLoadDataBase":
        """mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataBase"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetHarmonicLoadDataForImport"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartLoadCase":
        """Cast to another type.

        Returns:
            _Cast_PartLoadCase
        """
        return _Cast_PartLoadCase(self)
