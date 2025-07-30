"""ComponentCompoundModalAnalysis"""

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
    _5082,
)

_COMPONENT_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "ComponentCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4867
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _5002,
        _5003,
        _5005,
        _5009,
        _5012,
        _5015,
        _5016,
        _5017,
        _5020,
        _5024,
        _5029,
        _5030,
        _5033,
        _5037,
        _5040,
        _5043,
        _5046,
        _5048,
        _5051,
        _5052,
        _5053,
        _5054,
        _5057,
        _5059,
        _5062,
        _5063,
        _5067,
        _5070,
        _5073,
        _5076,
        _5077,
        _5079,
        _5080,
        _5081,
        _5085,
        _5088,
        _5089,
        _5090,
        _5091,
        _5092,
        _5095,
        _5098,
        _5099,
        _5102,
        _5107,
        _5108,
        _5111,
        _5114,
        _5115,
        _5117,
        _5118,
        _5119,
        _5122,
        _5123,
        _5124,
        _5125,
        _5126,
        _5129,
    )

    Self = TypeVar("Self", bound="ComponentCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentCompoundModalAnalysis._Cast_ComponentCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentCompoundModalAnalysis:
    """Special nested class for casting ComponentCompoundModalAnalysis to subclasses."""

    __parent__: "ComponentCompoundModalAnalysis"

    @property
    def part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5082.PartCompoundModalAnalysis":
        return self.__parent__._cast(_5082.PartCompoundModalAnalysis)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7888.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7888,
        )

        return self.__parent__._cast(_7888.PartCompoundAnalysis)

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
    def abstract_shaft_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5002.AbstractShaftCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5002,
        )

        return self.__parent__._cast(_5002.AbstractShaftCompoundModalAnalysis)

    @property
    def abstract_shaft_or_housing_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5003.AbstractShaftOrHousingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5003,
        )

        return self.__parent__._cast(_5003.AbstractShaftOrHousingCompoundModalAnalysis)

    @property
    def agma_gleason_conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5005.AGMAGleasonConicalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5005,
        )

        return self.__parent__._cast(_5005.AGMAGleasonConicalGearCompoundModalAnalysis)

    @property
    def bearing_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5009.BearingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5009,
        )

        return self.__parent__._cast(_5009.BearingCompoundModalAnalysis)

    @property
    def bevel_differential_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5012.BevelDifferentialGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5012,
        )

        return self.__parent__._cast(_5012.BevelDifferentialGearCompoundModalAnalysis)

    @property
    def bevel_differential_planet_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5015.BevelDifferentialPlanetGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5015,
        )

        return self.__parent__._cast(
            _5015.BevelDifferentialPlanetGearCompoundModalAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5016.BevelDifferentialSunGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5016,
        )

        return self.__parent__._cast(
            _5016.BevelDifferentialSunGearCompoundModalAnalysis
        )

    @property
    def bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5017.BevelGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5017,
        )

        return self.__parent__._cast(_5017.BevelGearCompoundModalAnalysis)

    @property
    def bolt_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5020.BoltCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5020,
        )

        return self.__parent__._cast(_5020.BoltCompoundModalAnalysis)

    @property
    def clutch_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5024.ClutchHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5024,
        )

        return self.__parent__._cast(_5024.ClutchHalfCompoundModalAnalysis)

    @property
    def concept_coupling_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5029.ConceptCouplingHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5029,
        )

        return self.__parent__._cast(_5029.ConceptCouplingHalfCompoundModalAnalysis)

    @property
    def concept_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5030.ConceptGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5030,
        )

        return self.__parent__._cast(_5030.ConceptGearCompoundModalAnalysis)

    @property
    def conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5033.ConicalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5033,
        )

        return self.__parent__._cast(_5033.ConicalGearCompoundModalAnalysis)

    @property
    def connector_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5037.ConnectorCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5037,
        )

        return self.__parent__._cast(_5037.ConnectorCompoundModalAnalysis)

    @property
    def coupling_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5040.CouplingHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5040,
        )

        return self.__parent__._cast(_5040.CouplingHalfCompoundModalAnalysis)

    @property
    def cvt_pulley_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5043.CVTPulleyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5043,
        )

        return self.__parent__._cast(_5043.CVTPulleyCompoundModalAnalysis)

    @property
    def cycloidal_disc_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5046.CycloidalDiscCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5046,
        )

        return self.__parent__._cast(_5046.CycloidalDiscCompoundModalAnalysis)

    @property
    def cylindrical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5048.CylindricalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5048,
        )

        return self.__parent__._cast(_5048.CylindricalGearCompoundModalAnalysis)

    @property
    def cylindrical_planet_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5051.CylindricalPlanetGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5051,
        )

        return self.__parent__._cast(_5051.CylindricalPlanetGearCompoundModalAnalysis)

    @property
    def datum_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5052.DatumCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5052,
        )

        return self.__parent__._cast(_5052.DatumCompoundModalAnalysis)

    @property
    def external_cad_model_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5053.ExternalCADModelCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5053,
        )

        return self.__parent__._cast(_5053.ExternalCADModelCompoundModalAnalysis)

    @property
    def face_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5054.FaceGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5054,
        )

        return self.__parent__._cast(_5054.FaceGearCompoundModalAnalysis)

    @property
    def fe_part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5057.FEPartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5057,
        )

        return self.__parent__._cast(_5057.FEPartCompoundModalAnalysis)

    @property
    def gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5059.GearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5059,
        )

        return self.__parent__._cast(_5059.GearCompoundModalAnalysis)

    @property
    def guide_dxf_model_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5062.GuideDxfModelCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5062,
        )

        return self.__parent__._cast(_5062.GuideDxfModelCompoundModalAnalysis)

    @property
    def hypoid_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5063.HypoidGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5063,
        )

        return self.__parent__._cast(_5063.HypoidGearCompoundModalAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5067.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5067,
        )

        return self.__parent__._cast(
            _5067.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5070.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5070,
        )

        return self.__parent__._cast(
            _5070.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5073.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5073,
        )

        return self.__parent__._cast(
            _5073.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis
        )

    @property
    def mass_disc_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5076.MassDiscCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5076,
        )

        return self.__parent__._cast(_5076.MassDiscCompoundModalAnalysis)

    @property
    def measurement_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5077.MeasurementComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5077,
        )

        return self.__parent__._cast(_5077.MeasurementComponentCompoundModalAnalysis)

    @property
    def microphone_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5079.MicrophoneCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5079,
        )

        return self.__parent__._cast(_5079.MicrophoneCompoundModalAnalysis)

    @property
    def mountable_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5080.MountableComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5080,
        )

        return self.__parent__._cast(_5080.MountableComponentCompoundModalAnalysis)

    @property
    def oil_seal_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5081.OilSealCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5081,
        )

        return self.__parent__._cast(_5081.OilSealCompoundModalAnalysis)

    @property
    def part_to_part_shear_coupling_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5085.PartToPartShearCouplingHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5085,
        )

        return self.__parent__._cast(
            _5085.PartToPartShearCouplingHalfCompoundModalAnalysis
        )

    @property
    def planet_carrier_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5088.PlanetCarrierCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5088,
        )

        return self.__parent__._cast(_5088.PlanetCarrierCompoundModalAnalysis)

    @property
    def point_load_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5089.PointLoadCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5089,
        )

        return self.__parent__._cast(_5089.PointLoadCompoundModalAnalysis)

    @property
    def power_load_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5090.PowerLoadCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5090,
        )

        return self.__parent__._cast(_5090.PowerLoadCompoundModalAnalysis)

    @property
    def pulley_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5091.PulleyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5091,
        )

        return self.__parent__._cast(_5091.PulleyCompoundModalAnalysis)

    @property
    def ring_pins_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5092.RingPinsCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5092,
        )

        return self.__parent__._cast(_5092.RingPinsCompoundModalAnalysis)

    @property
    def rolling_ring_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5095.RollingRingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5095,
        )

        return self.__parent__._cast(_5095.RollingRingCompoundModalAnalysis)

    @property
    def shaft_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5098.ShaftCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5098,
        )

        return self.__parent__._cast(_5098.ShaftCompoundModalAnalysis)

    @property
    def shaft_hub_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5099.ShaftHubConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5099,
        )

        return self.__parent__._cast(_5099.ShaftHubConnectionCompoundModalAnalysis)

    @property
    def spiral_bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5102.SpiralBevelGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5102,
        )

        return self.__parent__._cast(_5102.SpiralBevelGearCompoundModalAnalysis)

    @property
    def spring_damper_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5107.SpringDamperHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5107,
        )

        return self.__parent__._cast(_5107.SpringDamperHalfCompoundModalAnalysis)

    @property
    def straight_bevel_diff_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5108.StraightBevelDiffGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5108,
        )

        return self.__parent__._cast(_5108.StraightBevelDiffGearCompoundModalAnalysis)

    @property
    def straight_bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5111.StraightBevelGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5111,
        )

        return self.__parent__._cast(_5111.StraightBevelGearCompoundModalAnalysis)

    @property
    def straight_bevel_planet_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5114.StraightBevelPlanetGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5114,
        )

        return self.__parent__._cast(_5114.StraightBevelPlanetGearCompoundModalAnalysis)

    @property
    def straight_bevel_sun_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5115.StraightBevelSunGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5115,
        )

        return self.__parent__._cast(_5115.StraightBevelSunGearCompoundModalAnalysis)

    @property
    def synchroniser_half_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5117.SynchroniserHalfCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5117,
        )

        return self.__parent__._cast(_5117.SynchroniserHalfCompoundModalAnalysis)

    @property
    def synchroniser_part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5118.SynchroniserPartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5118,
        )

        return self.__parent__._cast(_5118.SynchroniserPartCompoundModalAnalysis)

    @property
    def synchroniser_sleeve_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5119.SynchroniserSleeveCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5119,
        )

        return self.__parent__._cast(_5119.SynchroniserSleeveCompoundModalAnalysis)

    @property
    def torque_converter_pump_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5122.TorqueConverterPumpCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5122,
        )

        return self.__parent__._cast(_5122.TorqueConverterPumpCompoundModalAnalysis)

    @property
    def torque_converter_turbine_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5123.TorqueConverterTurbineCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5123,
        )

        return self.__parent__._cast(_5123.TorqueConverterTurbineCompoundModalAnalysis)

    @property
    def unbalanced_mass_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5124.UnbalancedMassCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5124,
        )

        return self.__parent__._cast(_5124.UnbalancedMassCompoundModalAnalysis)

    @property
    def virtual_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5125.VirtualComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5125,
        )

        return self.__parent__._cast(_5125.VirtualComponentCompoundModalAnalysis)

    @property
    def worm_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5126.WormGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5126,
        )

        return self.__parent__._cast(_5126.WormGearCompoundModalAnalysis)

    @property
    def zerol_bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5129.ZerolBevelGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5129,
        )

        return self.__parent__._cast(_5129.ZerolBevelGearCompoundModalAnalysis)

    @property
    def component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "ComponentCompoundModalAnalysis":
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
class ComponentCompoundModalAnalysis(_5082.PartCompoundModalAnalysis):
    """ComponentCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases(self: "Self") -> "List[_4867.ComponentModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ComponentModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4867.ComponentModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ComponentModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ComponentCompoundModalAnalysis
        """
        return _Cast_ComponentCompoundModalAnalysis(self)
