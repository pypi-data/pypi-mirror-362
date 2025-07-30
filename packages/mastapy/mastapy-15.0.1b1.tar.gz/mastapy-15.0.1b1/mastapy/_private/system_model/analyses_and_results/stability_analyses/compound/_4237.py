"""PartCompoundStabilityAnalysis"""

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

_PART_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "PartCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7885
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4103,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4156,
        _4157,
        _4158,
        _4160,
        _4162,
        _4163,
        _4164,
        _4166,
        _4167,
        _4169,
        _4170,
        _4171,
        _4172,
        _4174,
        _4175,
        _4176,
        _4177,
        _4179,
        _4181,
        _4182,
        _4184,
        _4185,
        _4187,
        _4188,
        _4190,
        _4192,
        _4193,
        _4195,
        _4197,
        _4198,
        _4199,
        _4201,
        _4203,
        _4205,
        _4206,
        _4207,
        _4208,
        _4209,
        _4211,
        _4212,
        _4213,
        _4214,
        _4216,
        _4217,
        _4218,
        _4220,
        _4222,
        _4224,
        _4225,
        _4227,
        _4228,
        _4230,
        _4231,
        _4232,
        _4233,
        _4234,
        _4235,
        _4236,
        _4238,
        _4240,
        _4242,
        _4243,
        _4244,
        _4245,
        _4246,
        _4247,
        _4249,
        _4250,
        _4252,
        _4253,
        _4254,
        _4256,
        _4257,
        _4259,
        _4260,
        _4262,
        _4263,
        _4265,
        _4266,
        _4268,
        _4269,
        _4270,
        _4271,
        _4272,
        _4273,
        _4274,
        _4275,
        _4277,
        _4278,
        _4279,
        _4280,
        _4281,
        _4283,
        _4284,
        _4286,
    )

    Self = TypeVar("Self", bound="PartCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartCompoundStabilityAnalysis._Cast_PartCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartCompoundStabilityAnalysis:
    """Special nested class for casting PartCompoundStabilityAnalysis to subclasses."""

    __parent__: "PartCompoundStabilityAnalysis"

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
    def abstract_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4156.AbstractAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4156,
        )

        return self.__parent__._cast(_4156.AbstractAssemblyCompoundStabilityAnalysis)

    @property
    def abstract_shaft_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4157.AbstractShaftCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4157,
        )

        return self.__parent__._cast(_4157.AbstractShaftCompoundStabilityAnalysis)

    @property
    def abstract_shaft_or_housing_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4158.AbstractShaftOrHousingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4158,
        )

        return self.__parent__._cast(
            _4158.AbstractShaftOrHousingCompoundStabilityAnalysis
        )

    @property
    def agma_gleason_conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4160.AGMAGleasonConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4160,
        )

        return self.__parent__._cast(
            _4160.AGMAGleasonConicalGearCompoundStabilityAnalysis
        )

    @property
    def agma_gleason_conical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4162.AGMAGleasonConicalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4162,
        )

        return self.__parent__._cast(
            _4162.AGMAGleasonConicalGearSetCompoundStabilityAnalysis
        )

    @property
    def assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4163.AssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4163,
        )

        return self.__parent__._cast(_4163.AssemblyCompoundStabilityAnalysis)

    @property
    def bearing_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4164.BearingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4164,
        )

        return self.__parent__._cast(_4164.BearingCompoundStabilityAnalysis)

    @property
    def belt_drive_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4166.BeltDriveCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4166,
        )

        return self.__parent__._cast(_4166.BeltDriveCompoundStabilityAnalysis)

    @property
    def bevel_differential_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4167.BevelDifferentialGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4167,
        )

        return self.__parent__._cast(
            _4167.BevelDifferentialGearCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4169.BevelDifferentialGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4169,
        )

        return self.__parent__._cast(
            _4169.BevelDifferentialGearSetCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4170.BevelDifferentialPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4170,
        )

        return self.__parent__._cast(
            _4170.BevelDifferentialPlanetGearCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4171.BevelDifferentialSunGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4171,
        )

        return self.__parent__._cast(
            _4171.BevelDifferentialSunGearCompoundStabilityAnalysis
        )

    @property
    def bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4172.BevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4172,
        )

        return self.__parent__._cast(_4172.BevelGearCompoundStabilityAnalysis)

    @property
    def bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4174.BevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4174,
        )

        return self.__parent__._cast(_4174.BevelGearSetCompoundStabilityAnalysis)

    @property
    def bolt_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4175.BoltCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4175,
        )

        return self.__parent__._cast(_4175.BoltCompoundStabilityAnalysis)

    @property
    def bolted_joint_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4176.BoltedJointCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4176,
        )

        return self.__parent__._cast(_4176.BoltedJointCompoundStabilityAnalysis)

    @property
    def clutch_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4177.ClutchCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4177,
        )

        return self.__parent__._cast(_4177.ClutchCompoundStabilityAnalysis)

    @property
    def clutch_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4179.ClutchHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4179,
        )

        return self.__parent__._cast(_4179.ClutchHalfCompoundStabilityAnalysis)

    @property
    def component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4181.ComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4181,
        )

        return self.__parent__._cast(_4181.ComponentCompoundStabilityAnalysis)

    @property
    def concept_coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4182.ConceptCouplingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4182,
        )

        return self.__parent__._cast(_4182.ConceptCouplingCompoundStabilityAnalysis)

    @property
    def concept_coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4184.ConceptCouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4184,
        )

        return self.__parent__._cast(_4184.ConceptCouplingHalfCompoundStabilityAnalysis)

    @property
    def concept_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4185.ConceptGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4185,
        )

        return self.__parent__._cast(_4185.ConceptGearCompoundStabilityAnalysis)

    @property
    def concept_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4187.ConceptGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4187,
        )

        return self.__parent__._cast(_4187.ConceptGearSetCompoundStabilityAnalysis)

    @property
    def conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4188.ConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4188,
        )

        return self.__parent__._cast(_4188.ConicalGearCompoundStabilityAnalysis)

    @property
    def conical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4190.ConicalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4190,
        )

        return self.__parent__._cast(_4190.ConicalGearSetCompoundStabilityAnalysis)

    @property
    def connector_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4192.ConnectorCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4192,
        )

        return self.__parent__._cast(_4192.ConnectorCompoundStabilityAnalysis)

    @property
    def coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4193.CouplingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4193,
        )

        return self.__parent__._cast(_4193.CouplingCompoundStabilityAnalysis)

    @property
    def coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4195.CouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4195,
        )

        return self.__parent__._cast(_4195.CouplingHalfCompoundStabilityAnalysis)

    @property
    def cvt_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4197.CVTCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4197,
        )

        return self.__parent__._cast(_4197.CVTCompoundStabilityAnalysis)

    @property
    def cvt_pulley_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4198.CVTPulleyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4198,
        )

        return self.__parent__._cast(_4198.CVTPulleyCompoundStabilityAnalysis)

    @property
    def cycloidal_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4199.CycloidalAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4199,
        )

        return self.__parent__._cast(_4199.CycloidalAssemblyCompoundStabilityAnalysis)

    @property
    def cycloidal_disc_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4201.CycloidalDiscCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4201,
        )

        return self.__parent__._cast(_4201.CycloidalDiscCompoundStabilityAnalysis)

    @property
    def cylindrical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4203.CylindricalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4203,
        )

        return self.__parent__._cast(_4203.CylindricalGearCompoundStabilityAnalysis)

    @property
    def cylindrical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4205.CylindricalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4205,
        )

        return self.__parent__._cast(_4205.CylindricalGearSetCompoundStabilityAnalysis)

    @property
    def cylindrical_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4206.CylindricalPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4206,
        )

        return self.__parent__._cast(
            _4206.CylindricalPlanetGearCompoundStabilityAnalysis
        )

    @property
    def datum_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4207.DatumCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4207,
        )

        return self.__parent__._cast(_4207.DatumCompoundStabilityAnalysis)

    @property
    def external_cad_model_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4208.ExternalCADModelCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4208,
        )

        return self.__parent__._cast(_4208.ExternalCADModelCompoundStabilityAnalysis)

    @property
    def face_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4209.FaceGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4209,
        )

        return self.__parent__._cast(_4209.FaceGearCompoundStabilityAnalysis)

    @property
    def face_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4211.FaceGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4211,
        )

        return self.__parent__._cast(_4211.FaceGearSetCompoundStabilityAnalysis)

    @property
    def fe_part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4212.FEPartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4212,
        )

        return self.__parent__._cast(_4212.FEPartCompoundStabilityAnalysis)

    @property
    def flexible_pin_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4213.FlexiblePinAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4213,
        )

        return self.__parent__._cast(_4213.FlexiblePinAssemblyCompoundStabilityAnalysis)

    @property
    def gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4214.GearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4214,
        )

        return self.__parent__._cast(_4214.GearCompoundStabilityAnalysis)

    @property
    def gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4216.GearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4216,
        )

        return self.__parent__._cast(_4216.GearSetCompoundStabilityAnalysis)

    @property
    def guide_dxf_model_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4217.GuideDxfModelCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4217,
        )

        return self.__parent__._cast(_4217.GuideDxfModelCompoundStabilityAnalysis)

    @property
    def hypoid_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4218.HypoidGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4218,
        )

        return self.__parent__._cast(_4218.HypoidGearCompoundStabilityAnalysis)

    @property
    def hypoid_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4220.HypoidGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4220,
        )

        return self.__parent__._cast(_4220.HypoidGearSetCompoundStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4222.KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4222,
        )

        return self.__parent__._cast(
            _4222.KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4224.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4224,
        )

        return self.__parent__._cast(
            _4224.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4225.KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4225,
        )

        return self.__parent__._cast(
            _4225.KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4227.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4227,
        )

        return self.__parent__._cast(
            _4227.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4228.KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4228,
        )

        return self.__parent__._cast(
            _4228.KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4230.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4230,
        )

        return self.__parent__._cast(
            _4230.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis
        )

    @property
    def mass_disc_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4231.MassDiscCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4231,
        )

        return self.__parent__._cast(_4231.MassDiscCompoundStabilityAnalysis)

    @property
    def measurement_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4232.MeasurementComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4232,
        )

        return self.__parent__._cast(
            _4232.MeasurementComponentCompoundStabilityAnalysis
        )

    @property
    def microphone_array_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4233.MicrophoneArrayCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4233,
        )

        return self.__parent__._cast(_4233.MicrophoneArrayCompoundStabilityAnalysis)

    @property
    def microphone_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4234.MicrophoneCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4234,
        )

        return self.__parent__._cast(_4234.MicrophoneCompoundStabilityAnalysis)

    @property
    def mountable_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4235.MountableComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4235,
        )

        return self.__parent__._cast(_4235.MountableComponentCompoundStabilityAnalysis)

    @property
    def oil_seal_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4236.OilSealCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4236,
        )

        return self.__parent__._cast(_4236.OilSealCompoundStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4238.PartToPartShearCouplingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4238,
        )

        return self.__parent__._cast(
            _4238.PartToPartShearCouplingCompoundStabilityAnalysis
        )

    @property
    def part_to_part_shear_coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4240.PartToPartShearCouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4240,
        )

        return self.__parent__._cast(
            _4240.PartToPartShearCouplingHalfCompoundStabilityAnalysis
        )

    @property
    def planetary_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4242.PlanetaryGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4242,
        )

        return self.__parent__._cast(_4242.PlanetaryGearSetCompoundStabilityAnalysis)

    @property
    def planet_carrier_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4243.PlanetCarrierCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4243,
        )

        return self.__parent__._cast(_4243.PlanetCarrierCompoundStabilityAnalysis)

    @property
    def point_load_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4244.PointLoadCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4244,
        )

        return self.__parent__._cast(_4244.PointLoadCompoundStabilityAnalysis)

    @property
    def power_load_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4245.PowerLoadCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4245,
        )

        return self.__parent__._cast(_4245.PowerLoadCompoundStabilityAnalysis)

    @property
    def pulley_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4246.PulleyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4246,
        )

        return self.__parent__._cast(_4246.PulleyCompoundStabilityAnalysis)

    @property
    def ring_pins_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4247.RingPinsCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4247,
        )

        return self.__parent__._cast(_4247.RingPinsCompoundStabilityAnalysis)

    @property
    def rolling_ring_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4249.RollingRingAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4249,
        )

        return self.__parent__._cast(_4249.RollingRingAssemblyCompoundStabilityAnalysis)

    @property
    def rolling_ring_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4250.RollingRingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4250,
        )

        return self.__parent__._cast(_4250.RollingRingCompoundStabilityAnalysis)

    @property
    def root_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4252.RootAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4252,
        )

        return self.__parent__._cast(_4252.RootAssemblyCompoundStabilityAnalysis)

    @property
    def shaft_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4253.ShaftCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4253,
        )

        return self.__parent__._cast(_4253.ShaftCompoundStabilityAnalysis)

    @property
    def shaft_hub_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4254.ShaftHubConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4254,
        )

        return self.__parent__._cast(_4254.ShaftHubConnectionCompoundStabilityAnalysis)

    @property
    def specialised_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4256.SpecialisedAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4256,
        )

        return self.__parent__._cast(_4256.SpecialisedAssemblyCompoundStabilityAnalysis)

    @property
    def spiral_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4257.SpiralBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4257,
        )

        return self.__parent__._cast(_4257.SpiralBevelGearCompoundStabilityAnalysis)

    @property
    def spiral_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4259.SpiralBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4259,
        )

        return self.__parent__._cast(_4259.SpiralBevelGearSetCompoundStabilityAnalysis)

    @property
    def spring_damper_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4260.SpringDamperCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4260,
        )

        return self.__parent__._cast(_4260.SpringDamperCompoundStabilityAnalysis)

    @property
    def spring_damper_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4262.SpringDamperHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4262,
        )

        return self.__parent__._cast(_4262.SpringDamperHalfCompoundStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4263.StraightBevelDiffGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4263,
        )

        return self.__parent__._cast(
            _4263.StraightBevelDiffGearCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_diff_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4265.StraightBevelDiffGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4265,
        )

        return self.__parent__._cast(
            _4265.StraightBevelDiffGearSetCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4266.StraightBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4266,
        )

        return self.__parent__._cast(_4266.StraightBevelGearCompoundStabilityAnalysis)

    @property
    def straight_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4268.StraightBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4268,
        )

        return self.__parent__._cast(
            _4268.StraightBevelGearSetCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4269.StraightBevelPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4269,
        )

        return self.__parent__._cast(
            _4269.StraightBevelPlanetGearCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4270.StraightBevelSunGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4270,
        )

        return self.__parent__._cast(
            _4270.StraightBevelSunGearCompoundStabilityAnalysis
        )

    @property
    def synchroniser_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4271.SynchroniserCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4271,
        )

        return self.__parent__._cast(_4271.SynchroniserCompoundStabilityAnalysis)

    @property
    def synchroniser_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4272.SynchroniserHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4272,
        )

        return self.__parent__._cast(_4272.SynchroniserHalfCompoundStabilityAnalysis)

    @property
    def synchroniser_part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4273.SynchroniserPartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4273,
        )

        return self.__parent__._cast(_4273.SynchroniserPartCompoundStabilityAnalysis)

    @property
    def synchroniser_sleeve_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4274.SynchroniserSleeveCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4274,
        )

        return self.__parent__._cast(_4274.SynchroniserSleeveCompoundStabilityAnalysis)

    @property
    def torque_converter_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4275.TorqueConverterCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4275,
        )

        return self.__parent__._cast(_4275.TorqueConverterCompoundStabilityAnalysis)

    @property
    def torque_converter_pump_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4277.TorqueConverterPumpCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4277,
        )

        return self.__parent__._cast(_4277.TorqueConverterPumpCompoundStabilityAnalysis)

    @property
    def torque_converter_turbine_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4278.TorqueConverterTurbineCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4278,
        )

        return self.__parent__._cast(
            _4278.TorqueConverterTurbineCompoundStabilityAnalysis
        )

    @property
    def unbalanced_mass_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4279.UnbalancedMassCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4279,
        )

        return self.__parent__._cast(_4279.UnbalancedMassCompoundStabilityAnalysis)

    @property
    def virtual_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4280.VirtualComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4280,
        )

        return self.__parent__._cast(_4280.VirtualComponentCompoundStabilityAnalysis)

    @property
    def worm_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4281.WormGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4281,
        )

        return self.__parent__._cast(_4281.WormGearCompoundStabilityAnalysis)

    @property
    def worm_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4283.WormGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4283,
        )

        return self.__parent__._cast(_4283.WormGearSetCompoundStabilityAnalysis)

    @property
    def zerol_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4284.ZerolBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4284,
        )

        return self.__parent__._cast(_4284.ZerolBevelGearCompoundStabilityAnalysis)

    @property
    def zerol_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4286.ZerolBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4286,
        )

        return self.__parent__._cast(_4286.ZerolBevelGearSetCompoundStabilityAnalysis)

    @property
    def part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "PartCompoundStabilityAnalysis":
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
class PartCompoundStabilityAnalysis(_7888.PartCompoundAnalysis):
    """PartCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases(self: "Self") -> "List[_4103.PartStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.PartStabilityAnalysis]

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
    ) -> "List[_4103.PartStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.PartStabilityAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_PartCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartCompoundStabilityAnalysis
        """
        return _Cast_PartCompoundStabilityAnalysis(self)
