"""PartCompoundModalAnalysisAtASpeed"""

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
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7888

_PART_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
    "PartCompoundModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7885
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5478,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5528,
        _5529,
        _5530,
        _5532,
        _5534,
        _5535,
        _5536,
        _5538,
        _5539,
        _5541,
        _5542,
        _5543,
        _5544,
        _5546,
        _5547,
        _5548,
        _5549,
        _5551,
        _5553,
        _5554,
        _5556,
        _5557,
        _5559,
        _5560,
        _5562,
        _5564,
        _5565,
        _5567,
        _5569,
        _5570,
        _5571,
        _5573,
        _5575,
        _5577,
        _5578,
        _5579,
        _5580,
        _5581,
        _5583,
        _5584,
        _5585,
        _5586,
        _5588,
        _5589,
        _5590,
        _5592,
        _5594,
        _5596,
        _5597,
        _5599,
        _5600,
        _5602,
        _5603,
        _5604,
        _5605,
        _5606,
        _5607,
        _5608,
        _5610,
        _5612,
        _5614,
        _5615,
        _5616,
        _5617,
        _5618,
        _5619,
        _5621,
        _5622,
        _5624,
        _5625,
        _5626,
        _5628,
        _5629,
        _5631,
        _5632,
        _5634,
        _5635,
        _5637,
        _5638,
        _5640,
        _5641,
        _5642,
        _5643,
        _5644,
        _5645,
        _5646,
        _5647,
        _5649,
        _5650,
        _5651,
        _5652,
        _5653,
        _5655,
        _5656,
        _5658,
    )

    Self = TypeVar("Self", bound="PartCompoundModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartCompoundModalAnalysisAtASpeed._Cast_PartCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartCompoundModalAnalysisAtASpeed:
    """Special nested class for casting PartCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "PartCompoundModalAnalysisAtASpeed"

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7888.PartCompoundAnalysis":
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
    def abstract_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5528.AbstractAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5528,
        )

        return self.__parent__._cast(
            _5528.AbstractAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def abstract_shaft_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5529.AbstractShaftCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5529,
        )

        return self.__parent__._cast(_5529.AbstractShaftCompoundModalAnalysisAtASpeed)

    @property
    def abstract_shaft_or_housing_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5530.AbstractShaftOrHousingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5530,
        )

        return self.__parent__._cast(
            _5530.AbstractShaftOrHousingCompoundModalAnalysisAtASpeed
        )

    @property
    def agma_gleason_conical_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5532.AGMAGleasonConicalGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5532,
        )

        return self.__parent__._cast(
            _5532.AGMAGleasonConicalGearCompoundModalAnalysisAtASpeed
        )

    @property
    def agma_gleason_conical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5534.AGMAGleasonConicalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5534,
        )

        return self.__parent__._cast(
            _5534.AGMAGleasonConicalGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5535.AssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5535,
        )

        return self.__parent__._cast(_5535.AssemblyCompoundModalAnalysisAtASpeed)

    @property
    def bearing_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5536.BearingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5536,
        )

        return self.__parent__._cast(_5536.BearingCompoundModalAnalysisAtASpeed)

    @property
    def belt_drive_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5538.BeltDriveCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5538,
        )

        return self.__parent__._cast(_5538.BeltDriveCompoundModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5539.BevelDifferentialGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5539,
        )

        return self.__parent__._cast(
            _5539.BevelDifferentialGearCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5541.BevelDifferentialGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5541,
        )

        return self.__parent__._cast(
            _5541.BevelDifferentialGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_planet_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5542.BevelDifferentialPlanetGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5542,
        )

        return self.__parent__._cast(
            _5542.BevelDifferentialPlanetGearCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_sun_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5543.BevelDifferentialSunGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5543,
        )

        return self.__parent__._cast(
            _5543.BevelDifferentialSunGearCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5544.BevelGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5544,
        )

        return self.__parent__._cast(_5544.BevelGearCompoundModalAnalysisAtASpeed)

    @property
    def bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5546.BevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5546,
        )

        return self.__parent__._cast(_5546.BevelGearSetCompoundModalAnalysisAtASpeed)

    @property
    def bolt_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5547.BoltCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5547,
        )

        return self.__parent__._cast(_5547.BoltCompoundModalAnalysisAtASpeed)

    @property
    def bolted_joint_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5548.BoltedJointCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5548,
        )

        return self.__parent__._cast(_5548.BoltedJointCompoundModalAnalysisAtASpeed)

    @property
    def clutch_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5549.ClutchCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5549,
        )

        return self.__parent__._cast(_5549.ClutchCompoundModalAnalysisAtASpeed)

    @property
    def clutch_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5551.ClutchHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5551,
        )

        return self.__parent__._cast(_5551.ClutchHalfCompoundModalAnalysisAtASpeed)

    @property
    def component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5553.ComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5553,
        )

        return self.__parent__._cast(_5553.ComponentCompoundModalAnalysisAtASpeed)

    @property
    def concept_coupling_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5554.ConceptCouplingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5554,
        )

        return self.__parent__._cast(_5554.ConceptCouplingCompoundModalAnalysisAtASpeed)

    @property
    def concept_coupling_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5556.ConceptCouplingHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5556,
        )

        return self.__parent__._cast(
            _5556.ConceptCouplingHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def concept_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5557.ConceptGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5557,
        )

        return self.__parent__._cast(_5557.ConceptGearCompoundModalAnalysisAtASpeed)

    @property
    def concept_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5559.ConceptGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5559,
        )

        return self.__parent__._cast(_5559.ConceptGearSetCompoundModalAnalysisAtASpeed)

    @property
    def conical_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5560.ConicalGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5560,
        )

        return self.__parent__._cast(_5560.ConicalGearCompoundModalAnalysisAtASpeed)

    @property
    def conical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5562.ConicalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5562,
        )

        return self.__parent__._cast(_5562.ConicalGearSetCompoundModalAnalysisAtASpeed)

    @property
    def connector_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5564.ConnectorCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5564,
        )

        return self.__parent__._cast(_5564.ConnectorCompoundModalAnalysisAtASpeed)

    @property
    def coupling_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5565.CouplingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5565,
        )

        return self.__parent__._cast(_5565.CouplingCompoundModalAnalysisAtASpeed)

    @property
    def coupling_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5567.CouplingHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5567,
        )

        return self.__parent__._cast(_5567.CouplingHalfCompoundModalAnalysisAtASpeed)

    @property
    def cvt_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5569.CVTCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5569,
        )

        return self.__parent__._cast(_5569.CVTCompoundModalAnalysisAtASpeed)

    @property
    def cvt_pulley_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5570.CVTPulleyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5570,
        )

        return self.__parent__._cast(_5570.CVTPulleyCompoundModalAnalysisAtASpeed)

    @property
    def cycloidal_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5571.CycloidalAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5571,
        )

        return self.__parent__._cast(
            _5571.CycloidalAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def cycloidal_disc_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5573.CycloidalDiscCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5573,
        )

        return self.__parent__._cast(_5573.CycloidalDiscCompoundModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5575.CylindricalGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5575,
        )

        return self.__parent__._cast(_5575.CylindricalGearCompoundModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5577.CylindricalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5577,
        )

        return self.__parent__._cast(
            _5577.CylindricalGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def cylindrical_planet_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5578.CylindricalPlanetGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5578,
        )

        return self.__parent__._cast(
            _5578.CylindricalPlanetGearCompoundModalAnalysisAtASpeed
        )

    @property
    def datum_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5579.DatumCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5579,
        )

        return self.__parent__._cast(_5579.DatumCompoundModalAnalysisAtASpeed)

    @property
    def external_cad_model_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5580.ExternalCADModelCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5580,
        )

        return self.__parent__._cast(
            _5580.ExternalCADModelCompoundModalAnalysisAtASpeed
        )

    @property
    def face_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5581.FaceGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5581,
        )

        return self.__parent__._cast(_5581.FaceGearCompoundModalAnalysisAtASpeed)

    @property
    def face_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5583.FaceGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5583,
        )

        return self.__parent__._cast(_5583.FaceGearSetCompoundModalAnalysisAtASpeed)

    @property
    def fe_part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5584.FEPartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5584,
        )

        return self.__parent__._cast(_5584.FEPartCompoundModalAnalysisAtASpeed)

    @property
    def flexible_pin_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5585.FlexiblePinAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5585,
        )

        return self.__parent__._cast(
            _5585.FlexiblePinAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5586.GearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5586,
        )

        return self.__parent__._cast(_5586.GearCompoundModalAnalysisAtASpeed)

    @property
    def gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5588.GearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5588,
        )

        return self.__parent__._cast(_5588.GearSetCompoundModalAnalysisAtASpeed)

    @property
    def guide_dxf_model_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5589.GuideDxfModelCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5589,
        )

        return self.__parent__._cast(_5589.GuideDxfModelCompoundModalAnalysisAtASpeed)

    @property
    def hypoid_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5590.HypoidGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5590,
        )

        return self.__parent__._cast(_5590.HypoidGearCompoundModalAnalysisAtASpeed)

    @property
    def hypoid_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5592.HypoidGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5592,
        )

        return self.__parent__._cast(_5592.HypoidGearSetCompoundModalAnalysisAtASpeed)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5594.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5594,
        )

        return self.__parent__._cast(
            _5594.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5596.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5596,
        )

        return self.__parent__._cast(
            _5596.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5597.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5597,
        )

        return self.__parent__._cast(
            _5597.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5599.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5599,
        )

        return self.__parent__._cast(
            _5599.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5600.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5600,
        )

        return self.__parent__._cast(
            _5600.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_5602.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5602,
        )

        return self.__parent__._cast(
            _5602.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def mass_disc_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5603.MassDiscCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5603,
        )

        return self.__parent__._cast(_5603.MassDiscCompoundModalAnalysisAtASpeed)

    @property
    def measurement_component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5604.MeasurementComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5604,
        )

        return self.__parent__._cast(
            _5604.MeasurementComponentCompoundModalAnalysisAtASpeed
        )

    @property
    def microphone_array_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5605.MicrophoneArrayCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5605,
        )

        return self.__parent__._cast(_5605.MicrophoneArrayCompoundModalAnalysisAtASpeed)

    @property
    def microphone_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5606.MicrophoneCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5606,
        )

        return self.__parent__._cast(_5606.MicrophoneCompoundModalAnalysisAtASpeed)

    @property
    def mountable_component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5607.MountableComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5607,
        )

        return self.__parent__._cast(
            _5607.MountableComponentCompoundModalAnalysisAtASpeed
        )

    @property
    def oil_seal_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5608.OilSealCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5608,
        )

        return self.__parent__._cast(_5608.OilSealCompoundModalAnalysisAtASpeed)

    @property
    def part_to_part_shear_coupling_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5610.PartToPartShearCouplingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5610,
        )

        return self.__parent__._cast(
            _5610.PartToPartShearCouplingCompoundModalAnalysisAtASpeed
        )

    @property
    def part_to_part_shear_coupling_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5612.PartToPartShearCouplingHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5612,
        )

        return self.__parent__._cast(
            _5612.PartToPartShearCouplingHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def planetary_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5614.PlanetaryGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5614,
        )

        return self.__parent__._cast(
            _5614.PlanetaryGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def planet_carrier_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5615.PlanetCarrierCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5615,
        )

        return self.__parent__._cast(_5615.PlanetCarrierCompoundModalAnalysisAtASpeed)

    @property
    def point_load_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5616.PointLoadCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5616,
        )

        return self.__parent__._cast(_5616.PointLoadCompoundModalAnalysisAtASpeed)

    @property
    def power_load_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5617.PowerLoadCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5617,
        )

        return self.__parent__._cast(_5617.PowerLoadCompoundModalAnalysisAtASpeed)

    @property
    def pulley_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5618.PulleyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5618,
        )

        return self.__parent__._cast(_5618.PulleyCompoundModalAnalysisAtASpeed)

    @property
    def ring_pins_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5619.RingPinsCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5619,
        )

        return self.__parent__._cast(_5619.RingPinsCompoundModalAnalysisAtASpeed)

    @property
    def rolling_ring_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5621.RollingRingAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5621,
        )

        return self.__parent__._cast(
            _5621.RollingRingAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def rolling_ring_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5622.RollingRingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5622,
        )

        return self.__parent__._cast(_5622.RollingRingCompoundModalAnalysisAtASpeed)

    @property
    def root_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5624.RootAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5624,
        )

        return self.__parent__._cast(_5624.RootAssemblyCompoundModalAnalysisAtASpeed)

    @property
    def shaft_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5625.ShaftCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5625,
        )

        return self.__parent__._cast(_5625.ShaftCompoundModalAnalysisAtASpeed)

    @property
    def shaft_hub_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5626.ShaftHubConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5626,
        )

        return self.__parent__._cast(
            _5626.ShaftHubConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def specialised_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5628.SpecialisedAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5628,
        )

        return self.__parent__._cast(
            _5628.SpecialisedAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def spiral_bevel_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5629.SpiralBevelGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5629,
        )

        return self.__parent__._cast(_5629.SpiralBevelGearCompoundModalAnalysisAtASpeed)

    @property
    def spiral_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5631.SpiralBevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5631,
        )

        return self.__parent__._cast(
            _5631.SpiralBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def spring_damper_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5632.SpringDamperCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5632,
        )

        return self.__parent__._cast(_5632.SpringDamperCompoundModalAnalysisAtASpeed)

    @property
    def spring_damper_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5634.SpringDamperHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5634,
        )

        return self.__parent__._cast(
            _5634.SpringDamperHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_diff_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5635.StraightBevelDiffGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5635,
        )

        return self.__parent__._cast(
            _5635.StraightBevelDiffGearCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_diff_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5637.StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5637,
        )

        return self.__parent__._cast(
            _5637.StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5638.StraightBevelGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5638,
        )

        return self.__parent__._cast(
            _5638.StraightBevelGearCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5640.StraightBevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5640,
        )

        return self.__parent__._cast(
            _5640.StraightBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_planet_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5641.StraightBevelPlanetGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5641,
        )

        return self.__parent__._cast(
            _5641.StraightBevelPlanetGearCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_sun_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5642.StraightBevelSunGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5642,
        )

        return self.__parent__._cast(
            _5642.StraightBevelSunGearCompoundModalAnalysisAtASpeed
        )

    @property
    def synchroniser_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5643.SynchroniserCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5643,
        )

        return self.__parent__._cast(_5643.SynchroniserCompoundModalAnalysisAtASpeed)

    @property
    def synchroniser_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5644.SynchroniserHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5644,
        )

        return self.__parent__._cast(
            _5644.SynchroniserHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def synchroniser_part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5645.SynchroniserPartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5645,
        )

        return self.__parent__._cast(
            _5645.SynchroniserPartCompoundModalAnalysisAtASpeed
        )

    @property
    def synchroniser_sleeve_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5646.SynchroniserSleeveCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5646,
        )

        return self.__parent__._cast(
            _5646.SynchroniserSleeveCompoundModalAnalysisAtASpeed
        )

    @property
    def torque_converter_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5647.TorqueConverterCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5647,
        )

        return self.__parent__._cast(_5647.TorqueConverterCompoundModalAnalysisAtASpeed)

    @property
    def torque_converter_pump_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5649.TorqueConverterPumpCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5649,
        )

        return self.__parent__._cast(
            _5649.TorqueConverterPumpCompoundModalAnalysisAtASpeed
        )

    @property
    def torque_converter_turbine_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5650.TorqueConverterTurbineCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5650,
        )

        return self.__parent__._cast(
            _5650.TorqueConverterTurbineCompoundModalAnalysisAtASpeed
        )

    @property
    def unbalanced_mass_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5651.UnbalancedMassCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5651,
        )

        return self.__parent__._cast(_5651.UnbalancedMassCompoundModalAnalysisAtASpeed)

    @property
    def virtual_component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5652.VirtualComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5652,
        )

        return self.__parent__._cast(
            _5652.VirtualComponentCompoundModalAnalysisAtASpeed
        )

    @property
    def worm_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5653.WormGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5653,
        )

        return self.__parent__._cast(_5653.WormGearCompoundModalAnalysisAtASpeed)

    @property
    def worm_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5655.WormGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5655,
        )

        return self.__parent__._cast(_5655.WormGearSetCompoundModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5656.ZerolBevelGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5656,
        )

        return self.__parent__._cast(_5656.ZerolBevelGearCompoundModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5658.ZerolBevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5658,
        )

        return self.__parent__._cast(
            _5658.ZerolBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "PartCompoundModalAnalysisAtASpeed":
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
class PartCompoundModalAnalysisAtASpeed(_7888.PartCompoundAnalysis):
    """PartCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5478.PartModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.PartModalAnalysisAtASpeed]

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
    ) -> "List[_5478.PartModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.PartModalAnalysisAtASpeed]

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
    def cast_to(self: "Self") -> "_Cast_PartCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_PartCompoundModalAnalysisAtASpeed
        """
        return _Cast_PartCompoundModalAnalysisAtASpeed(self)
