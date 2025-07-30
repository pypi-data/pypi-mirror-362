"""PartCompoundHarmonicAnalysis"""

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

_PART_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "PartCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7885
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6084,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6185,
        _6186,
        _6187,
        _6189,
        _6191,
        _6192,
        _6193,
        _6195,
        _6196,
        _6198,
        _6199,
        _6200,
        _6201,
        _6203,
        _6204,
        _6205,
        _6206,
        _6208,
        _6210,
        _6211,
        _6213,
        _6214,
        _6216,
        _6217,
        _6219,
        _6221,
        _6222,
        _6224,
        _6226,
        _6227,
        _6228,
        _6230,
        _6232,
        _6234,
        _6235,
        _6236,
        _6237,
        _6238,
        _6240,
        _6241,
        _6242,
        _6243,
        _6245,
        _6246,
        _6247,
        _6249,
        _6251,
        _6253,
        _6254,
        _6256,
        _6257,
        _6259,
        _6260,
        _6261,
        _6262,
        _6263,
        _6264,
        _6265,
        _6267,
        _6269,
        _6271,
        _6272,
        _6273,
        _6274,
        _6275,
        _6276,
        _6278,
        _6279,
        _6281,
        _6282,
        _6283,
        _6285,
        _6286,
        _6288,
        _6289,
        _6291,
        _6292,
        _6294,
        _6295,
        _6297,
        _6298,
        _6299,
        _6300,
        _6301,
        _6302,
        _6303,
        _6304,
        _6306,
        _6307,
        _6308,
        _6309,
        _6310,
        _6312,
        _6313,
        _6315,
    )

    Self = TypeVar("Self", bound="PartCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartCompoundHarmonicAnalysis._Cast_PartCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartCompoundHarmonicAnalysis:
    """Special nested class for casting PartCompoundHarmonicAnalysis to subclasses."""

    __parent__: "PartCompoundHarmonicAnalysis"

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
    def abstract_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6185.AbstractAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6185,
        )

        return self.__parent__._cast(_6185.AbstractAssemblyCompoundHarmonicAnalysis)

    @property
    def abstract_shaft_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6186.AbstractShaftCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6186,
        )

        return self.__parent__._cast(_6186.AbstractShaftCompoundHarmonicAnalysis)

    @property
    def abstract_shaft_or_housing_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6187.AbstractShaftOrHousingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6187,
        )

        return self.__parent__._cast(
            _6187.AbstractShaftOrHousingCompoundHarmonicAnalysis
        )

    @property
    def agma_gleason_conical_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6189.AGMAGleasonConicalGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6189,
        )

        return self.__parent__._cast(
            _6189.AGMAGleasonConicalGearCompoundHarmonicAnalysis
        )

    @property
    def agma_gleason_conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6191.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6191,
        )

        return self.__parent__._cast(
            _6191.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis
        )

    @property
    def assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6192.AssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6192,
        )

        return self.__parent__._cast(_6192.AssemblyCompoundHarmonicAnalysis)

    @property
    def bearing_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6193.BearingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6193,
        )

        return self.__parent__._cast(_6193.BearingCompoundHarmonicAnalysis)

    @property
    def belt_drive_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6195.BeltDriveCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6195,
        )

        return self.__parent__._cast(_6195.BeltDriveCompoundHarmonicAnalysis)

    @property
    def bevel_differential_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6196.BevelDifferentialGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6196,
        )

        return self.__parent__._cast(
            _6196.BevelDifferentialGearCompoundHarmonicAnalysis
        )

    @property
    def bevel_differential_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6198.BevelDifferentialGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6198,
        )

        return self.__parent__._cast(
            _6198.BevelDifferentialGearSetCompoundHarmonicAnalysis
        )

    @property
    def bevel_differential_planet_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6199.BevelDifferentialPlanetGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6199,
        )

        return self.__parent__._cast(
            _6199.BevelDifferentialPlanetGearCompoundHarmonicAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6200.BevelDifferentialSunGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6200,
        )

        return self.__parent__._cast(
            _6200.BevelDifferentialSunGearCompoundHarmonicAnalysis
        )

    @property
    def bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6201.BevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6201,
        )

        return self.__parent__._cast(_6201.BevelGearCompoundHarmonicAnalysis)

    @property
    def bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6203.BevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6203,
        )

        return self.__parent__._cast(_6203.BevelGearSetCompoundHarmonicAnalysis)

    @property
    def bolt_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6204.BoltCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6204,
        )

        return self.__parent__._cast(_6204.BoltCompoundHarmonicAnalysis)

    @property
    def bolted_joint_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6205.BoltedJointCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6205,
        )

        return self.__parent__._cast(_6205.BoltedJointCompoundHarmonicAnalysis)

    @property
    def clutch_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6206.ClutchCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6206,
        )

        return self.__parent__._cast(_6206.ClutchCompoundHarmonicAnalysis)

    @property
    def clutch_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6208.ClutchHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6208,
        )

        return self.__parent__._cast(_6208.ClutchHalfCompoundHarmonicAnalysis)

    @property
    def component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6210.ComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6210,
        )

        return self.__parent__._cast(_6210.ComponentCompoundHarmonicAnalysis)

    @property
    def concept_coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6211.ConceptCouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6211,
        )

        return self.__parent__._cast(_6211.ConceptCouplingCompoundHarmonicAnalysis)

    @property
    def concept_coupling_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6213.ConceptCouplingHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6213,
        )

        return self.__parent__._cast(_6213.ConceptCouplingHalfCompoundHarmonicAnalysis)

    @property
    def concept_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6214.ConceptGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6214,
        )

        return self.__parent__._cast(_6214.ConceptGearCompoundHarmonicAnalysis)

    @property
    def concept_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6216.ConceptGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6216,
        )

        return self.__parent__._cast(_6216.ConceptGearSetCompoundHarmonicAnalysis)

    @property
    def conical_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6217.ConicalGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6217,
        )

        return self.__parent__._cast(_6217.ConicalGearCompoundHarmonicAnalysis)

    @property
    def conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6219.ConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6219,
        )

        return self.__parent__._cast(_6219.ConicalGearSetCompoundHarmonicAnalysis)

    @property
    def connector_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6221.ConnectorCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6221,
        )

        return self.__parent__._cast(_6221.ConnectorCompoundHarmonicAnalysis)

    @property
    def coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6222.CouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6222,
        )

        return self.__parent__._cast(_6222.CouplingCompoundHarmonicAnalysis)

    @property
    def coupling_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6224.CouplingHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6224,
        )

        return self.__parent__._cast(_6224.CouplingHalfCompoundHarmonicAnalysis)

    @property
    def cvt_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6226.CVTCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6226,
        )

        return self.__parent__._cast(_6226.CVTCompoundHarmonicAnalysis)

    @property
    def cvt_pulley_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6227.CVTPulleyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6227,
        )

        return self.__parent__._cast(_6227.CVTPulleyCompoundHarmonicAnalysis)

    @property
    def cycloidal_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6228.CycloidalAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6228,
        )

        return self.__parent__._cast(_6228.CycloidalAssemblyCompoundHarmonicAnalysis)

    @property
    def cycloidal_disc_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6230.CycloidalDiscCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6230,
        )

        return self.__parent__._cast(_6230.CycloidalDiscCompoundHarmonicAnalysis)

    @property
    def cylindrical_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6232.CylindricalGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6232,
        )

        return self.__parent__._cast(_6232.CylindricalGearCompoundHarmonicAnalysis)

    @property
    def cylindrical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6234.CylindricalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6234,
        )

        return self.__parent__._cast(_6234.CylindricalGearSetCompoundHarmonicAnalysis)

    @property
    def cylindrical_planet_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6235.CylindricalPlanetGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6235,
        )

        return self.__parent__._cast(
            _6235.CylindricalPlanetGearCompoundHarmonicAnalysis
        )

    @property
    def datum_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6236.DatumCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6236,
        )

        return self.__parent__._cast(_6236.DatumCompoundHarmonicAnalysis)

    @property
    def external_cad_model_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6237.ExternalCADModelCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6237,
        )

        return self.__parent__._cast(_6237.ExternalCADModelCompoundHarmonicAnalysis)

    @property
    def face_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6238.FaceGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6238,
        )

        return self.__parent__._cast(_6238.FaceGearCompoundHarmonicAnalysis)

    @property
    def face_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6240.FaceGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6240,
        )

        return self.__parent__._cast(_6240.FaceGearSetCompoundHarmonicAnalysis)

    @property
    def fe_part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6241.FEPartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6241,
        )

        return self.__parent__._cast(_6241.FEPartCompoundHarmonicAnalysis)

    @property
    def flexible_pin_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6242.FlexiblePinAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6242,
        )

        return self.__parent__._cast(_6242.FlexiblePinAssemblyCompoundHarmonicAnalysis)

    @property
    def gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6243.GearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6243,
        )

        return self.__parent__._cast(_6243.GearCompoundHarmonicAnalysis)

    @property
    def gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6245.GearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6245,
        )

        return self.__parent__._cast(_6245.GearSetCompoundHarmonicAnalysis)

    @property
    def guide_dxf_model_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6246.GuideDxfModelCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6246,
        )

        return self.__parent__._cast(_6246.GuideDxfModelCompoundHarmonicAnalysis)

    @property
    def hypoid_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6247.HypoidGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6247,
        )

        return self.__parent__._cast(_6247.HypoidGearCompoundHarmonicAnalysis)

    @property
    def hypoid_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6249.HypoidGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6249,
        )

        return self.__parent__._cast(_6249.HypoidGearSetCompoundHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6251.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6251,
        )

        return self.__parent__._cast(
            _6251.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6253.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6253,
        )

        return self.__parent__._cast(
            _6253.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6254.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6254,
        )

        return self.__parent__._cast(
            _6254.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6256.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6256,
        )

        return self.__parent__._cast(
            _6256.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6257.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6257,
        )

        return self.__parent__._cast(
            _6257.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6259.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6259,
        )

        return self.__parent__._cast(
            _6259.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis
        )

    @property
    def mass_disc_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6260.MassDiscCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6260,
        )

        return self.__parent__._cast(_6260.MassDiscCompoundHarmonicAnalysis)

    @property
    def measurement_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6261.MeasurementComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6261,
        )

        return self.__parent__._cast(_6261.MeasurementComponentCompoundHarmonicAnalysis)

    @property
    def microphone_array_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6262.MicrophoneArrayCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6262,
        )

        return self.__parent__._cast(_6262.MicrophoneArrayCompoundHarmonicAnalysis)

    @property
    def microphone_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6263.MicrophoneCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6263,
        )

        return self.__parent__._cast(_6263.MicrophoneCompoundHarmonicAnalysis)

    @property
    def mountable_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6264.MountableComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6264,
        )

        return self.__parent__._cast(_6264.MountableComponentCompoundHarmonicAnalysis)

    @property
    def oil_seal_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6265.OilSealCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6265,
        )

        return self.__parent__._cast(_6265.OilSealCompoundHarmonicAnalysis)

    @property
    def part_to_part_shear_coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6267.PartToPartShearCouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6267,
        )

        return self.__parent__._cast(
            _6267.PartToPartShearCouplingCompoundHarmonicAnalysis
        )

    @property
    def part_to_part_shear_coupling_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6269.PartToPartShearCouplingHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6269,
        )

        return self.__parent__._cast(
            _6269.PartToPartShearCouplingHalfCompoundHarmonicAnalysis
        )

    @property
    def planetary_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6271.PlanetaryGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6271,
        )

        return self.__parent__._cast(_6271.PlanetaryGearSetCompoundHarmonicAnalysis)

    @property
    def planet_carrier_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6272.PlanetCarrierCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6272,
        )

        return self.__parent__._cast(_6272.PlanetCarrierCompoundHarmonicAnalysis)

    @property
    def point_load_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6273.PointLoadCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6273,
        )

        return self.__parent__._cast(_6273.PointLoadCompoundHarmonicAnalysis)

    @property
    def power_load_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6274.PowerLoadCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6274,
        )

        return self.__parent__._cast(_6274.PowerLoadCompoundHarmonicAnalysis)

    @property
    def pulley_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6275.PulleyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6275,
        )

        return self.__parent__._cast(_6275.PulleyCompoundHarmonicAnalysis)

    @property
    def ring_pins_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6276.RingPinsCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6276,
        )

        return self.__parent__._cast(_6276.RingPinsCompoundHarmonicAnalysis)

    @property
    def rolling_ring_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6278.RollingRingAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6278,
        )

        return self.__parent__._cast(_6278.RollingRingAssemblyCompoundHarmonicAnalysis)

    @property
    def rolling_ring_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6279.RollingRingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6279,
        )

        return self.__parent__._cast(_6279.RollingRingCompoundHarmonicAnalysis)

    @property
    def root_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6281.RootAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6281,
        )

        return self.__parent__._cast(_6281.RootAssemblyCompoundHarmonicAnalysis)

    @property
    def shaft_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6282.ShaftCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6282,
        )

        return self.__parent__._cast(_6282.ShaftCompoundHarmonicAnalysis)

    @property
    def shaft_hub_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6283.ShaftHubConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6283,
        )

        return self.__parent__._cast(_6283.ShaftHubConnectionCompoundHarmonicAnalysis)

    @property
    def specialised_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6285.SpecialisedAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6285,
        )

        return self.__parent__._cast(_6285.SpecialisedAssemblyCompoundHarmonicAnalysis)

    @property
    def spiral_bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6286.SpiralBevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6286,
        )

        return self.__parent__._cast(_6286.SpiralBevelGearCompoundHarmonicAnalysis)

    @property
    def spiral_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6288.SpiralBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6288,
        )

        return self.__parent__._cast(_6288.SpiralBevelGearSetCompoundHarmonicAnalysis)

    @property
    def spring_damper_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6289.SpringDamperCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6289,
        )

        return self.__parent__._cast(_6289.SpringDamperCompoundHarmonicAnalysis)

    @property
    def spring_damper_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6291.SpringDamperHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6291,
        )

        return self.__parent__._cast(_6291.SpringDamperHalfCompoundHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6292.StraightBevelDiffGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6292,
        )

        return self.__parent__._cast(
            _6292.StraightBevelDiffGearCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_diff_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6294.StraightBevelDiffGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6294,
        )

        return self.__parent__._cast(
            _6294.StraightBevelDiffGearSetCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6295.StraightBevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6295,
        )

        return self.__parent__._cast(_6295.StraightBevelGearCompoundHarmonicAnalysis)

    @property
    def straight_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6297.StraightBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6297,
        )

        return self.__parent__._cast(_6297.StraightBevelGearSetCompoundHarmonicAnalysis)

    @property
    def straight_bevel_planet_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6298.StraightBevelPlanetGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6298,
        )

        return self.__parent__._cast(
            _6298.StraightBevelPlanetGearCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6299.StraightBevelSunGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6299,
        )

        return self.__parent__._cast(_6299.StraightBevelSunGearCompoundHarmonicAnalysis)

    @property
    def synchroniser_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6300.SynchroniserCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6300,
        )

        return self.__parent__._cast(_6300.SynchroniserCompoundHarmonicAnalysis)

    @property
    def synchroniser_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6301.SynchroniserHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6301,
        )

        return self.__parent__._cast(_6301.SynchroniserHalfCompoundHarmonicAnalysis)

    @property
    def synchroniser_part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6302.SynchroniserPartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6302,
        )

        return self.__parent__._cast(_6302.SynchroniserPartCompoundHarmonicAnalysis)

    @property
    def synchroniser_sleeve_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6303.SynchroniserSleeveCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6303,
        )

        return self.__parent__._cast(_6303.SynchroniserSleeveCompoundHarmonicAnalysis)

    @property
    def torque_converter_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6304.TorqueConverterCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6304,
        )

        return self.__parent__._cast(_6304.TorqueConverterCompoundHarmonicAnalysis)

    @property
    def torque_converter_pump_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6306.TorqueConverterPumpCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6306,
        )

        return self.__parent__._cast(_6306.TorqueConverterPumpCompoundHarmonicAnalysis)

    @property
    def torque_converter_turbine_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6307.TorqueConverterTurbineCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6307,
        )

        return self.__parent__._cast(
            _6307.TorqueConverterTurbineCompoundHarmonicAnalysis
        )

    @property
    def unbalanced_mass_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6308.UnbalancedMassCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6308,
        )

        return self.__parent__._cast(_6308.UnbalancedMassCompoundHarmonicAnalysis)

    @property
    def virtual_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6309.VirtualComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6309,
        )

        return self.__parent__._cast(_6309.VirtualComponentCompoundHarmonicAnalysis)

    @property
    def worm_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6310.WormGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6310,
        )

        return self.__parent__._cast(_6310.WormGearCompoundHarmonicAnalysis)

    @property
    def worm_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6312.WormGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6312,
        )

        return self.__parent__._cast(_6312.WormGearSetCompoundHarmonicAnalysis)

    @property
    def zerol_bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6313.ZerolBevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6313,
        )

        return self.__parent__._cast(_6313.ZerolBevelGearCompoundHarmonicAnalysis)

    @property
    def zerol_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6315.ZerolBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6315,
        )

        return self.__parent__._cast(_6315.ZerolBevelGearSetCompoundHarmonicAnalysis)

    @property
    def part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "PartCompoundHarmonicAnalysis":
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
class PartCompoundHarmonicAnalysis(_7888.PartCompoundAnalysis):
    """PartCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases(self: "Self") -> "List[_6084.PartHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.PartHarmonicAnalysis]

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
    ) -> "List[_6084.PartHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.PartHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_PartCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartCompoundHarmonicAnalysis
        """
        return _Cast_PartCompoundHarmonicAnalysis(self)
