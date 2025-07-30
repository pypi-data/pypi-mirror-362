"""PartModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7890

_PART_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
    "PartModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7887
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5132,
        _5133,
        _5134,
        _5137,
        _5138,
        _5139,
        _5140,
        _5142,
        _5144,
        _5145,
        _5146,
        _5147,
        _5149,
        _5150,
        _5151,
        _5152,
        _5154,
        _5155,
        _5157,
        _5159,
        _5160,
        _5162,
        _5163,
        _5165,
        _5166,
        _5168,
        _5170,
        _5171,
        _5173,
        _5174,
        _5175,
        _5177,
        _5180,
        _5181,
        _5182,
        _5183,
        _5185,
        _5187,
        _5188,
        _5189,
        _5190,
        _5192,
        _5193,
        _5194,
        _5196,
        _5197,
        _5200,
        _5201,
        _5203,
        _5204,
        _5206,
        _5207,
        _5208,
        _5209,
        _5210,
        _5211,
        _5212,
        _5213,
        _5214,
        _5217,
        _5218,
        _5220,
        _5221,
        _5222,
        _5223,
        _5224,
        _5225,
        _5227,
        _5229,
        _5230,
        _5231,
        _5232,
        _5234,
        _5236,
        _5237,
        _5239,
        _5240,
        _5242,
        _5243,
        _5245,
        _5246,
        _5247,
        _5248,
        _5249,
        _5250,
        _5251,
        _5252,
        _5254,
        _5255,
        _5256,
        _5257,
        _5258,
        _5260,
        _5261,
        _5263,
        _5264,
    )
    from mastapy._private.system_model.part_model import _2698

    Self = TypeVar("Self", bound="PartModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartModalAnalysisAtAStiffness._Cast_PartModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartModalAnalysisAtAStiffness:
    """Special nested class for casting PartModalAnalysisAtAStiffness to subclasses."""

    __parent__: "PartModalAnalysisAtAStiffness"

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7890.PartStaticLoadAnalysisCase":
        return self.__parent__._cast(_7890.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7887.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7887,
        )

        return self.__parent__._cast(_7887.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

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
    def abstract_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5132.AbstractAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5132,
        )

        return self.__parent__._cast(_5132.AbstractAssemblyModalAnalysisAtAStiffness)

    @property
    def abstract_shaft_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5133.AbstractShaftModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5133,
        )

        return self.__parent__._cast(_5133.AbstractShaftModalAnalysisAtAStiffness)

    @property
    def abstract_shaft_or_housing_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5134.AbstractShaftOrHousingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5134,
        )

        return self.__parent__._cast(
            _5134.AbstractShaftOrHousingModalAnalysisAtAStiffness
        )

    @property
    def agma_gleason_conical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5137.AGMAGleasonConicalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5137,
        )

        return self.__parent__._cast(
            _5137.AGMAGleasonConicalGearModalAnalysisAtAStiffness
        )

    @property
    def agma_gleason_conical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5138.AGMAGleasonConicalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5138,
        )

        return self.__parent__._cast(
            _5138.AGMAGleasonConicalGearSetModalAnalysisAtAStiffness
        )

    @property
    def assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5139.AssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5139,
        )

        return self.__parent__._cast(_5139.AssemblyModalAnalysisAtAStiffness)

    @property
    def bearing_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5140.BearingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5140,
        )

        return self.__parent__._cast(_5140.BearingModalAnalysisAtAStiffness)

    @property
    def belt_drive_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5142.BeltDriveModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5142,
        )

        return self.__parent__._cast(_5142.BeltDriveModalAnalysisAtAStiffness)

    @property
    def bevel_differential_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5144.BevelDifferentialGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5144,
        )

        return self.__parent__._cast(
            _5144.BevelDifferentialGearModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5145.BevelDifferentialGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5145,
        )

        return self.__parent__._cast(
            _5145.BevelDifferentialGearSetModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5146.BevelDifferentialPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5146,
        )

        return self.__parent__._cast(
            _5146.BevelDifferentialPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_sun_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5147.BevelDifferentialSunGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5147,
        )

        return self.__parent__._cast(
            _5147.BevelDifferentialSunGearModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5149.BevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5149,
        )

        return self.__parent__._cast(_5149.BevelGearModalAnalysisAtAStiffness)

    @property
    def bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5150.BevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5150,
        )

        return self.__parent__._cast(_5150.BevelGearSetModalAnalysisAtAStiffness)

    @property
    def bolted_joint_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5151.BoltedJointModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5151,
        )

        return self.__parent__._cast(_5151.BoltedJointModalAnalysisAtAStiffness)

    @property
    def bolt_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5152.BoltModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5152,
        )

        return self.__parent__._cast(_5152.BoltModalAnalysisAtAStiffness)

    @property
    def clutch_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5154.ClutchHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5154,
        )

        return self.__parent__._cast(_5154.ClutchHalfModalAnalysisAtAStiffness)

    @property
    def clutch_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5155.ClutchModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5155,
        )

        return self.__parent__._cast(_5155.ClutchModalAnalysisAtAStiffness)

    @property
    def component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5157.ComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5157,
        )

        return self.__parent__._cast(_5157.ComponentModalAnalysisAtAStiffness)

    @property
    def concept_coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5159.ConceptCouplingHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5159,
        )

        return self.__parent__._cast(_5159.ConceptCouplingHalfModalAnalysisAtAStiffness)

    @property
    def concept_coupling_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5160.ConceptCouplingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5160,
        )

        return self.__parent__._cast(_5160.ConceptCouplingModalAnalysisAtAStiffness)

    @property
    def concept_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5162.ConceptGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5162,
        )

        return self.__parent__._cast(_5162.ConceptGearModalAnalysisAtAStiffness)

    @property
    def concept_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5163.ConceptGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5163,
        )

        return self.__parent__._cast(_5163.ConceptGearSetModalAnalysisAtAStiffness)

    @property
    def conical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5165.ConicalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5165,
        )

        return self.__parent__._cast(_5165.ConicalGearModalAnalysisAtAStiffness)

    @property
    def conical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5166.ConicalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5166,
        )

        return self.__parent__._cast(_5166.ConicalGearSetModalAnalysisAtAStiffness)

    @property
    def connector_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5168.ConnectorModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5168,
        )

        return self.__parent__._cast(_5168.ConnectorModalAnalysisAtAStiffness)

    @property
    def coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5170.CouplingHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5170,
        )

        return self.__parent__._cast(_5170.CouplingHalfModalAnalysisAtAStiffness)

    @property
    def coupling_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5171.CouplingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5171,
        )

        return self.__parent__._cast(_5171.CouplingModalAnalysisAtAStiffness)

    @property
    def cvt_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5173.CVTModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5173,
        )

        return self.__parent__._cast(_5173.CVTModalAnalysisAtAStiffness)

    @property
    def cvt_pulley_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5174.CVTPulleyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5174,
        )

        return self.__parent__._cast(_5174.CVTPulleyModalAnalysisAtAStiffness)

    @property
    def cycloidal_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5175.CycloidalAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5175,
        )

        return self.__parent__._cast(_5175.CycloidalAssemblyModalAnalysisAtAStiffness)

    @property
    def cycloidal_disc_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5177.CycloidalDiscModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5177,
        )

        return self.__parent__._cast(_5177.CycloidalDiscModalAnalysisAtAStiffness)

    @property
    def cylindrical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5180.CylindricalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5180,
        )

        return self.__parent__._cast(_5180.CylindricalGearModalAnalysisAtAStiffness)

    @property
    def cylindrical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5181.CylindricalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5181,
        )

        return self.__parent__._cast(_5181.CylindricalGearSetModalAnalysisAtAStiffness)

    @property
    def cylindrical_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5182.CylindricalPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5182,
        )

        return self.__parent__._cast(
            _5182.CylindricalPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def datum_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5183.DatumModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5183,
        )

        return self.__parent__._cast(_5183.DatumModalAnalysisAtAStiffness)

    @property
    def external_cad_model_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5185.ExternalCADModelModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5185,
        )

        return self.__parent__._cast(_5185.ExternalCADModelModalAnalysisAtAStiffness)

    @property
    def face_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5187.FaceGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5187,
        )

        return self.__parent__._cast(_5187.FaceGearModalAnalysisAtAStiffness)

    @property
    def face_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5188.FaceGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5188,
        )

        return self.__parent__._cast(_5188.FaceGearSetModalAnalysisAtAStiffness)

    @property
    def fe_part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5189.FEPartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5189,
        )

        return self.__parent__._cast(_5189.FEPartModalAnalysisAtAStiffness)

    @property
    def flexible_pin_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5190.FlexiblePinAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5190,
        )

        return self.__parent__._cast(_5190.FlexiblePinAssemblyModalAnalysisAtAStiffness)

    @property
    def gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5192.GearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5192,
        )

        return self.__parent__._cast(_5192.GearModalAnalysisAtAStiffness)

    @property
    def gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5193.GearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5193,
        )

        return self.__parent__._cast(_5193.GearSetModalAnalysisAtAStiffness)

    @property
    def guide_dxf_model_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5194.GuideDxfModelModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5194,
        )

        return self.__parent__._cast(_5194.GuideDxfModelModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5196.HypoidGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5196,
        )

        return self.__parent__._cast(_5196.HypoidGearModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5197.HypoidGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5197,
        )

        return self.__parent__._cast(_5197.HypoidGearSetModalAnalysisAtAStiffness)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5200.KlingelnbergCycloPalloidConicalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5200,
        )

        return self.__parent__._cast(
            _5200.KlingelnbergCycloPalloidConicalGearModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5201.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5201,
        )

        return self.__parent__._cast(
            _5201.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5203.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5203,
        )

        return self.__parent__._cast(
            _5203.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5204.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5204,
        )

        return self.__parent__._cast(
            _5204.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5206.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5206,
        )

        return self.__parent__._cast(
            _5206.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5207.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5207,
        )

        return self.__parent__._cast(
            _5207.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness
        )

    @property
    def mass_disc_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5208.MassDiscModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5208,
        )

        return self.__parent__._cast(_5208.MassDiscModalAnalysisAtAStiffness)

    @property
    def measurement_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5209.MeasurementComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5209,
        )

        return self.__parent__._cast(
            _5209.MeasurementComponentModalAnalysisAtAStiffness
        )

    @property
    def microphone_array_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5210.MicrophoneArrayModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5210,
        )

        return self.__parent__._cast(_5210.MicrophoneArrayModalAnalysisAtAStiffness)

    @property
    def microphone_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5211.MicrophoneModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5211,
        )

        return self.__parent__._cast(_5211.MicrophoneModalAnalysisAtAStiffness)

    @property
    def mountable_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5213.MountableComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5213,
        )

        return self.__parent__._cast(_5213.MountableComponentModalAnalysisAtAStiffness)

    @property
    def oil_seal_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5214.OilSealModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5214,
        )

        return self.__parent__._cast(_5214.OilSealModalAnalysisAtAStiffness)

    @property
    def part_to_part_shear_coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5217.PartToPartShearCouplingHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5217,
        )

        return self.__parent__._cast(
            _5217.PartToPartShearCouplingHalfModalAnalysisAtAStiffness
        )

    @property
    def part_to_part_shear_coupling_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5218.PartToPartShearCouplingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5218,
        )

        return self.__parent__._cast(
            _5218.PartToPartShearCouplingModalAnalysisAtAStiffness
        )

    @property
    def planetary_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5220.PlanetaryGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5220,
        )

        return self.__parent__._cast(_5220.PlanetaryGearSetModalAnalysisAtAStiffness)

    @property
    def planet_carrier_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5221.PlanetCarrierModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5221,
        )

        return self.__parent__._cast(_5221.PlanetCarrierModalAnalysisAtAStiffness)

    @property
    def point_load_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5222.PointLoadModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5222,
        )

        return self.__parent__._cast(_5222.PointLoadModalAnalysisAtAStiffness)

    @property
    def power_load_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5223.PowerLoadModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5223,
        )

        return self.__parent__._cast(_5223.PowerLoadModalAnalysisAtAStiffness)

    @property
    def pulley_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5224.PulleyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5224,
        )

        return self.__parent__._cast(_5224.PulleyModalAnalysisAtAStiffness)

    @property
    def ring_pins_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5225.RingPinsModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5225,
        )

        return self.__parent__._cast(_5225.RingPinsModalAnalysisAtAStiffness)

    @property
    def rolling_ring_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5227.RollingRingAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5227,
        )

        return self.__parent__._cast(_5227.RollingRingAssemblyModalAnalysisAtAStiffness)

    @property
    def rolling_ring_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5229.RollingRingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5229,
        )

        return self.__parent__._cast(_5229.RollingRingModalAnalysisAtAStiffness)

    @property
    def root_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5230.RootAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5230,
        )

        return self.__parent__._cast(_5230.RootAssemblyModalAnalysisAtAStiffness)

    @property
    def shaft_hub_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5231.ShaftHubConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5231,
        )

        return self.__parent__._cast(_5231.ShaftHubConnectionModalAnalysisAtAStiffness)

    @property
    def shaft_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5232.ShaftModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5232,
        )

        return self.__parent__._cast(_5232.ShaftModalAnalysisAtAStiffness)

    @property
    def specialised_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5234.SpecialisedAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5234,
        )

        return self.__parent__._cast(_5234.SpecialisedAssemblyModalAnalysisAtAStiffness)

    @property
    def spiral_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5236.SpiralBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5236,
        )

        return self.__parent__._cast(_5236.SpiralBevelGearModalAnalysisAtAStiffness)

    @property
    def spiral_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5237.SpiralBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5237,
        )

        return self.__parent__._cast(_5237.SpiralBevelGearSetModalAnalysisAtAStiffness)

    @property
    def spring_damper_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5239.SpringDamperHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5239,
        )

        return self.__parent__._cast(_5239.SpringDamperHalfModalAnalysisAtAStiffness)

    @property
    def spring_damper_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5240.SpringDamperModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5240,
        )

        return self.__parent__._cast(_5240.SpringDamperModalAnalysisAtAStiffness)

    @property
    def straight_bevel_diff_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5242.StraightBevelDiffGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5242,
        )

        return self.__parent__._cast(
            _5242.StraightBevelDiffGearModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5243.StraightBevelDiffGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5243,
        )

        return self.__parent__._cast(
            _5243.StraightBevelDiffGearSetModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5245.StraightBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5245,
        )

        return self.__parent__._cast(_5245.StraightBevelGearModalAnalysisAtAStiffness)

    @property
    def straight_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5246.StraightBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5246,
        )

        return self.__parent__._cast(
            _5246.StraightBevelGearSetModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5247.StraightBevelPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5247,
        )

        return self.__parent__._cast(
            _5247.StraightBevelPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_sun_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5248.StraightBevelSunGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5248,
        )

        return self.__parent__._cast(
            _5248.StraightBevelSunGearModalAnalysisAtAStiffness
        )

    @property
    def synchroniser_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5249.SynchroniserHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5249,
        )

        return self.__parent__._cast(_5249.SynchroniserHalfModalAnalysisAtAStiffness)

    @property
    def synchroniser_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5250.SynchroniserModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5250,
        )

        return self.__parent__._cast(_5250.SynchroniserModalAnalysisAtAStiffness)

    @property
    def synchroniser_part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5251.SynchroniserPartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5251,
        )

        return self.__parent__._cast(_5251.SynchroniserPartModalAnalysisAtAStiffness)

    @property
    def synchroniser_sleeve_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5252.SynchroniserSleeveModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5252,
        )

        return self.__parent__._cast(_5252.SynchroniserSleeveModalAnalysisAtAStiffness)

    @property
    def torque_converter_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5254.TorqueConverterModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5254,
        )

        return self.__parent__._cast(_5254.TorqueConverterModalAnalysisAtAStiffness)

    @property
    def torque_converter_pump_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5255.TorqueConverterPumpModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5255,
        )

        return self.__parent__._cast(_5255.TorqueConverterPumpModalAnalysisAtAStiffness)

    @property
    def torque_converter_turbine_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5256.TorqueConverterTurbineModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5256,
        )

        return self.__parent__._cast(
            _5256.TorqueConverterTurbineModalAnalysisAtAStiffness
        )

    @property
    def unbalanced_mass_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5257.UnbalancedMassModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5257,
        )

        return self.__parent__._cast(_5257.UnbalancedMassModalAnalysisAtAStiffness)

    @property
    def virtual_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5258.VirtualComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5258,
        )

        return self.__parent__._cast(_5258.VirtualComponentModalAnalysisAtAStiffness)

    @property
    def worm_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5260.WormGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5260,
        )

        return self.__parent__._cast(_5260.WormGearModalAnalysisAtAStiffness)

    @property
    def worm_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5261.WormGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5261,
        )

        return self.__parent__._cast(_5261.WormGearSetModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5263.ZerolBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5263,
        )

        return self.__parent__._cast(_5263.ZerolBevelGearModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5264.ZerolBevelGearSetModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5264,
        )

        return self.__parent__._cast(_5264.ZerolBevelGearSetModalAnalysisAtAStiffness)

    @property
    def part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "PartModalAnalysisAtAStiffness":
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
class PartModalAnalysisAtAStiffness(_7890.PartStaticLoadAnalysisCase):
    """PartModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def modal_analysis_at_a_stiffness(
        self: "Self",
    ) -> "_5212.ModalAnalysisAtAStiffness":
        """mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ModalAnalysisAtAStiffness

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalAnalysisAtAStiffness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PartModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_PartModalAnalysisAtAStiffness
        """
        return _Cast_PartModalAnalysisAtAStiffness(self)
