"""PartFEAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7890

_PART_FE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases", "PartFEAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7887
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6589,
        _6590,
        _6591,
        _6593,
        _6595,
        _6596,
        _6597,
        _6599,
        _6600,
        _6602,
        _6603,
        _6604,
        _6605,
        _6607,
        _6608,
        _6609,
        _6611,
        _6612,
        _6614,
        _6616,
        _6617,
        _6618,
        _6620,
        _6621,
        _6623,
        _6625,
        _6627,
        _6628,
        _6630,
        _6631,
        _6632,
        _6634,
        _6636,
        _6638,
        _6639,
        _6640,
        _6643,
        _6644,
        _6646,
        _6647,
        _6648,
        _6649,
        _6651,
        _6652,
        _6653,
        _6655,
        _6657,
        _6659,
        _6660,
        _6662,
        _6663,
        _6665,
        _6666,
        _6667,
        _6668,
        _6669,
        _6670,
        _6671,
        _6672,
        _6674,
        _6675,
        _6677,
        _6678,
        _6679,
        _6680,
        _6681,
        _6682,
        _6684,
        _6686,
        _6687,
        _6688,
        _6689,
        _6691,
        _6692,
        _6694,
        _6696,
        _6697,
        _6698,
        _6700,
        _6701,
        _6703,
        _6704,
        _6705,
        _6706,
        _6707,
        _6708,
        _6709,
        _6711,
        _6712,
        _6713,
        _6714,
        _6715,
        _6716,
        _6718,
        _6719,
        _6721,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2926,
        _2927,
        _2928,
        _2931,
        _2932,
        _2933,
        _2939,
        _2941,
        _2943,
        _2944,
        _2945,
        _2946,
        _2948,
        _2949,
        _2950,
        _2951,
        _2953,
        _2954,
        _2956,
        _2959,
        _2960,
        _2962,
        _2963,
        _2966,
        _2967,
        _2969,
        _2971,
        _2972,
        _2974,
        _2975,
        _2976,
        _2979,
        _2983,
        _2984,
        _2985,
        _2986,
        _2987,
        _2988,
        _2991,
        _2992,
        _2993,
        _2996,
        _2997,
        _2998,
        _2999,
        _3001,
        _3002,
        _3003,
        _3005,
        _3006,
        _3010,
        _3011,
        _3013,
        _3014,
        _3016,
        _3017,
        _3020,
        _3021,
        _3023,
        _3024,
        _3025,
        _3027,
        _3028,
        _3030,
        _3031,
        _3033,
        _3034,
        _3035,
        _3036,
        _3037,
        _3040,
        _3042,
        _3043,
        _3044,
        _3047,
        _3049,
        _3051,
        _3052,
        _3054,
        _3055,
        _3057,
        _3058,
        _3060,
        _3061,
        _3062,
        _3063,
        _3064,
        _3065,
        _3066,
        _3067,
        _3072,
        _3073,
        _3074,
        _3077,
        _3078,
        _3080,
        _3081,
        _3083,
        _3084,
    )

    Self = TypeVar("Self", bound="PartFEAnalysis")
    CastSelf = TypeVar("CastSelf", bound="PartFEAnalysis._Cast_PartFEAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("PartFEAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartFEAnalysis:
    """Special nested class for casting PartFEAnalysis to subclasses."""

    __parent__: "PartFEAnalysis"

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
    def abstract_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2926.AbstractAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2926,
        )

        return self.__parent__._cast(_2926.AbstractAssemblySystemDeflection)

    @property
    def abstract_shaft_or_housing_system_deflection(
        self: "CastSelf",
    ) -> "_2927.AbstractShaftOrHousingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2927,
        )

        return self.__parent__._cast(_2927.AbstractShaftOrHousingSystemDeflection)

    @property
    def abstract_shaft_system_deflection(
        self: "CastSelf",
    ) -> "_2928.AbstractShaftSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2928,
        )

        return self.__parent__._cast(_2928.AbstractShaftSystemDeflection)

    @property
    def agma_gleason_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2931.AGMAGleasonConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2931,
        )

        return self.__parent__._cast(_2931.AGMAGleasonConicalGearSetSystemDeflection)

    @property
    def agma_gleason_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2932.AGMAGleasonConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2932,
        )

        return self.__parent__._cast(_2932.AGMAGleasonConicalGearSystemDeflection)

    @property
    def assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2933.AssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2933,
        )

        return self.__parent__._cast(_2933.AssemblySystemDeflection)

    @property
    def bearing_system_deflection(self: "CastSelf") -> "_2939.BearingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2939,
        )

        return self.__parent__._cast(_2939.BearingSystemDeflection)

    @property
    def belt_drive_system_deflection(
        self: "CastSelf",
    ) -> "_2941.BeltDriveSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2941,
        )

        return self.__parent__._cast(_2941.BeltDriveSystemDeflection)

    @property
    def bevel_differential_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2943.BevelDifferentialGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2943,
        )

        return self.__parent__._cast(_2943.BevelDifferentialGearSetSystemDeflection)

    @property
    def bevel_differential_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2944.BevelDifferentialGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2944,
        )

        return self.__parent__._cast(_2944.BevelDifferentialGearSystemDeflection)

    @property
    def bevel_differential_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2945.BevelDifferentialPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2945,
        )

        return self.__parent__._cast(_2945.BevelDifferentialPlanetGearSystemDeflection)

    @property
    def bevel_differential_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2946.BevelDifferentialSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2946,
        )

        return self.__parent__._cast(_2946.BevelDifferentialSunGearSystemDeflection)

    @property
    def bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2948.BevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2948,
        )

        return self.__parent__._cast(_2948.BevelGearSetSystemDeflection)

    @property
    def bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2949.BevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2949,
        )

        return self.__parent__._cast(_2949.BevelGearSystemDeflection)

    @property
    def bolted_joint_system_deflection(
        self: "CastSelf",
    ) -> "_2950.BoltedJointSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2950,
        )

        return self.__parent__._cast(_2950.BoltedJointSystemDeflection)

    @property
    def bolt_system_deflection(self: "CastSelf") -> "_2951.BoltSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2951,
        )

        return self.__parent__._cast(_2951.BoltSystemDeflection)

    @property
    def clutch_half_system_deflection(
        self: "CastSelf",
    ) -> "_2953.ClutchHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2953,
        )

        return self.__parent__._cast(_2953.ClutchHalfSystemDeflection)

    @property
    def clutch_system_deflection(self: "CastSelf") -> "_2954.ClutchSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2954,
        )

        return self.__parent__._cast(_2954.ClutchSystemDeflection)

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2956.ComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2956,
        )

        return self.__parent__._cast(_2956.ComponentSystemDeflection)

    @property
    def concept_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2959.ConceptCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2959,
        )

        return self.__parent__._cast(_2959.ConceptCouplingHalfSystemDeflection)

    @property
    def concept_coupling_system_deflection(
        self: "CastSelf",
    ) -> "_2960.ConceptCouplingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2960,
        )

        return self.__parent__._cast(_2960.ConceptCouplingSystemDeflection)

    @property
    def concept_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2962.ConceptGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2962,
        )

        return self.__parent__._cast(_2962.ConceptGearSetSystemDeflection)

    @property
    def concept_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2963.ConceptGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2963,
        )

        return self.__parent__._cast(_2963.ConceptGearSystemDeflection)

    @property
    def conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2966.ConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2966,
        )

        return self.__parent__._cast(_2966.ConicalGearSetSystemDeflection)

    @property
    def conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2967.ConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2967,
        )

        return self.__parent__._cast(_2967.ConicalGearSystemDeflection)

    @property
    def connector_system_deflection(
        self: "CastSelf",
    ) -> "_2969.ConnectorSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2969,
        )

        return self.__parent__._cast(_2969.ConnectorSystemDeflection)

    @property
    def coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2971.CouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2971,
        )

        return self.__parent__._cast(_2971.CouplingHalfSystemDeflection)

    @property
    def coupling_system_deflection(
        self: "CastSelf",
    ) -> "_2972.CouplingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2972,
        )

        return self.__parent__._cast(_2972.CouplingSystemDeflection)

    @property
    def cvt_pulley_system_deflection(
        self: "CastSelf",
    ) -> "_2974.CVTPulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2974,
        )

        return self.__parent__._cast(_2974.CVTPulleySystemDeflection)

    @property
    def cvt_system_deflection(self: "CastSelf") -> "_2975.CVTSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2975,
        )

        return self.__parent__._cast(_2975.CVTSystemDeflection)

    @property
    def cycloidal_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2976.CycloidalAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2976,
        )

        return self.__parent__._cast(_2976.CycloidalAssemblySystemDeflection)

    @property
    def cycloidal_disc_system_deflection(
        self: "CastSelf",
    ) -> "_2979.CycloidalDiscSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2979,
        )

        return self.__parent__._cast(_2979.CycloidalDiscSystemDeflection)

    @property
    def cylindrical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2983.CylindricalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2983,
        )

        return self.__parent__._cast(_2983.CylindricalGearSetSystemDeflection)

    @property
    def cylindrical_gear_set_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2984.CylindricalGearSetSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2984,
        )

        return self.__parent__._cast(_2984.CylindricalGearSetSystemDeflectionTimestep)

    @property
    def cylindrical_gear_set_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2985.CylindricalGearSetSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2985,
        )

        return self.__parent__._cast(
            _2985.CylindricalGearSetSystemDeflectionWithLTCAResults
        )

    @property
    def cylindrical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2986.CylindricalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2986,
        )

        return self.__parent__._cast(_2986.CylindricalGearSystemDeflection)

    @property
    def cylindrical_gear_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2987.CylindricalGearSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2987,
        )

        return self.__parent__._cast(_2987.CylindricalGearSystemDeflectionTimestep)

    @property
    def cylindrical_gear_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2988.CylindricalGearSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2988,
        )

        return self.__parent__._cast(
            _2988.CylindricalGearSystemDeflectionWithLTCAResults
        )

    @property
    def cylindrical_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2991.CylindricalPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2991,
        )

        return self.__parent__._cast(_2991.CylindricalPlanetGearSystemDeflection)

    @property
    def datum_system_deflection(self: "CastSelf") -> "_2992.DatumSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2992,
        )

        return self.__parent__._cast(_2992.DatumSystemDeflection)

    @property
    def external_cad_model_system_deflection(
        self: "CastSelf",
    ) -> "_2993.ExternalCADModelSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2993,
        )

        return self.__parent__._cast(_2993.ExternalCADModelSystemDeflection)

    @property
    def face_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2996.FaceGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2996,
        )

        return self.__parent__._cast(_2996.FaceGearSetSystemDeflection)

    @property
    def face_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2997.FaceGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2997,
        )

        return self.__parent__._cast(_2997.FaceGearSystemDeflection)

    @property
    def fe_part_system_deflection(self: "CastSelf") -> "_2998.FEPartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2998,
        )

        return self.__parent__._cast(_2998.FEPartSystemDeflection)

    @property
    def flexible_pin_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2999.FlexiblePinAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2999,
        )

        return self.__parent__._cast(_2999.FlexiblePinAssemblySystemDeflection)

    @property
    def gear_set_system_deflection(self: "CastSelf") -> "_3001.GearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3001,
        )

        return self.__parent__._cast(_3001.GearSetSystemDeflection)

    @property
    def gear_system_deflection(self: "CastSelf") -> "_3002.GearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3002,
        )

        return self.__parent__._cast(_3002.GearSystemDeflection)

    @property
    def guide_dxf_model_system_deflection(
        self: "CastSelf",
    ) -> "_3003.GuideDxfModelSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3003,
        )

        return self.__parent__._cast(_3003.GuideDxfModelSystemDeflection)

    @property
    def hypoid_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3005.HypoidGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3005,
        )

        return self.__parent__._cast(_3005.HypoidGearSetSystemDeflection)

    @property
    def hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3006.HypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3006,
        )

        return self.__parent__._cast(_3006.HypoidGearSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3010.KlingelnbergCycloPalloidConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3010,
        )

        return self.__parent__._cast(
            _3010.KlingelnbergCycloPalloidConicalGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3011.KlingelnbergCycloPalloidConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3011,
        )

        return self.__parent__._cast(
            _3011.KlingelnbergCycloPalloidConicalGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3013.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3013,
        )

        return self.__parent__._cast(
            _3013.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3014.KlingelnbergCycloPalloidHypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3014,
        )

        return self.__parent__._cast(
            _3014.KlingelnbergCycloPalloidHypoidGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3016.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3016,
        )

        return self.__parent__._cast(
            _3016.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3017.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3017,
        )

        return self.__parent__._cast(
            _3017.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection
        )

    @property
    def mass_disc_system_deflection(
        self: "CastSelf",
    ) -> "_3020.MassDiscSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3020,
        )

        return self.__parent__._cast(_3020.MassDiscSystemDeflection)

    @property
    def measurement_component_system_deflection(
        self: "CastSelf",
    ) -> "_3021.MeasurementComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3021,
        )

        return self.__parent__._cast(_3021.MeasurementComponentSystemDeflection)

    @property
    def microphone_array_system_deflection(
        self: "CastSelf",
    ) -> "_3023.MicrophoneArraySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3023,
        )

        return self.__parent__._cast(_3023.MicrophoneArraySystemDeflection)

    @property
    def microphone_system_deflection(
        self: "CastSelf",
    ) -> "_3024.MicrophoneSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3024,
        )

        return self.__parent__._cast(_3024.MicrophoneSystemDeflection)

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "_3025.MountableComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3025,
        )

        return self.__parent__._cast(_3025.MountableComponentSystemDeflection)

    @property
    def oil_seal_system_deflection(self: "CastSelf") -> "_3027.OilSealSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3027,
        )

        return self.__parent__._cast(_3027.OilSealSystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_3028.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3028,
        )

        return self.__parent__._cast(_3028.PartSystemDeflection)

    @property
    def part_to_part_shear_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_3030.PartToPartShearCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3030,
        )

        return self.__parent__._cast(_3030.PartToPartShearCouplingHalfSystemDeflection)

    @property
    def part_to_part_shear_coupling_system_deflection(
        self: "CastSelf",
    ) -> "_3031.PartToPartShearCouplingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3031,
        )

        return self.__parent__._cast(_3031.PartToPartShearCouplingSystemDeflection)

    @property
    def planet_carrier_system_deflection(
        self: "CastSelf",
    ) -> "_3033.PlanetCarrierSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3033,
        )

        return self.__parent__._cast(_3033.PlanetCarrierSystemDeflection)

    @property
    def point_load_system_deflection(
        self: "CastSelf",
    ) -> "_3034.PointLoadSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3034,
        )

        return self.__parent__._cast(_3034.PointLoadSystemDeflection)

    @property
    def power_load_system_deflection(
        self: "CastSelf",
    ) -> "_3035.PowerLoadSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3035,
        )

        return self.__parent__._cast(_3035.PowerLoadSystemDeflection)

    @property
    def pulley_system_deflection(self: "CastSelf") -> "_3036.PulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3036,
        )

        return self.__parent__._cast(_3036.PulleySystemDeflection)

    @property
    def ring_pins_system_deflection(
        self: "CastSelf",
    ) -> "_3037.RingPinsSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3037,
        )

        return self.__parent__._cast(_3037.RingPinsSystemDeflection)

    @property
    def rolling_ring_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_3040.RollingRingAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3040,
        )

        return self.__parent__._cast(_3040.RollingRingAssemblySystemDeflection)

    @property
    def rolling_ring_system_deflection(
        self: "CastSelf",
    ) -> "_3042.RollingRingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3042,
        )

        return self.__parent__._cast(_3042.RollingRingSystemDeflection)

    @property
    def root_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_3043.RootAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3043,
        )

        return self.__parent__._cast(_3043.RootAssemblySystemDeflection)

    @property
    def shaft_hub_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3044.ShaftHubConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3044,
        )

        return self.__parent__._cast(_3044.ShaftHubConnectionSystemDeflection)

    @property
    def shaft_system_deflection(self: "CastSelf") -> "_3047.ShaftSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3047,
        )

        return self.__parent__._cast(_3047.ShaftSystemDeflection)

    @property
    def specialised_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_3049.SpecialisedAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3049,
        )

        return self.__parent__._cast(_3049.SpecialisedAssemblySystemDeflection)

    @property
    def spiral_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3051.SpiralBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3051,
        )

        return self.__parent__._cast(_3051.SpiralBevelGearSetSystemDeflection)

    @property
    def spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3052.SpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3052,
        )

        return self.__parent__._cast(_3052.SpiralBevelGearSystemDeflection)

    @property
    def spring_damper_half_system_deflection(
        self: "CastSelf",
    ) -> "_3054.SpringDamperHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3054,
        )

        return self.__parent__._cast(_3054.SpringDamperHalfSystemDeflection)

    @property
    def spring_damper_system_deflection(
        self: "CastSelf",
    ) -> "_3055.SpringDamperSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3055,
        )

        return self.__parent__._cast(_3055.SpringDamperSystemDeflection)

    @property
    def straight_bevel_diff_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3057.StraightBevelDiffGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3057,
        )

        return self.__parent__._cast(_3057.StraightBevelDiffGearSetSystemDeflection)

    @property
    def straight_bevel_diff_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3058.StraightBevelDiffGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3058,
        )

        return self.__parent__._cast(_3058.StraightBevelDiffGearSystemDeflection)

    @property
    def straight_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3060.StraightBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3060,
        )

        return self.__parent__._cast(_3060.StraightBevelGearSetSystemDeflection)

    @property
    def straight_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3061.StraightBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3061,
        )

        return self.__parent__._cast(_3061.StraightBevelGearSystemDeflection)

    @property
    def straight_bevel_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3062.StraightBevelPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3062,
        )

        return self.__parent__._cast(_3062.StraightBevelPlanetGearSystemDeflection)

    @property
    def straight_bevel_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3063.StraightBevelSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3063,
        )

        return self.__parent__._cast(_3063.StraightBevelSunGearSystemDeflection)

    @property
    def synchroniser_half_system_deflection(
        self: "CastSelf",
    ) -> "_3064.SynchroniserHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3064,
        )

        return self.__parent__._cast(_3064.SynchroniserHalfSystemDeflection)

    @property
    def synchroniser_part_system_deflection(
        self: "CastSelf",
    ) -> "_3065.SynchroniserPartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3065,
        )

        return self.__parent__._cast(_3065.SynchroniserPartSystemDeflection)

    @property
    def synchroniser_sleeve_system_deflection(
        self: "CastSelf",
    ) -> "_3066.SynchroniserSleeveSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3066,
        )

        return self.__parent__._cast(_3066.SynchroniserSleeveSystemDeflection)

    @property
    def synchroniser_system_deflection(
        self: "CastSelf",
    ) -> "_3067.SynchroniserSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3067,
        )

        return self.__parent__._cast(_3067.SynchroniserSystemDeflection)

    @property
    def torque_converter_pump_system_deflection(
        self: "CastSelf",
    ) -> "_3072.TorqueConverterPumpSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3072,
        )

        return self.__parent__._cast(_3072.TorqueConverterPumpSystemDeflection)

    @property
    def torque_converter_system_deflection(
        self: "CastSelf",
    ) -> "_3073.TorqueConverterSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3073,
        )

        return self.__parent__._cast(_3073.TorqueConverterSystemDeflection)

    @property
    def torque_converter_turbine_system_deflection(
        self: "CastSelf",
    ) -> "_3074.TorqueConverterTurbineSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3074,
        )

        return self.__parent__._cast(_3074.TorqueConverterTurbineSystemDeflection)

    @property
    def unbalanced_mass_system_deflection(
        self: "CastSelf",
    ) -> "_3077.UnbalancedMassSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3077,
        )

        return self.__parent__._cast(_3077.UnbalancedMassSystemDeflection)

    @property
    def virtual_component_system_deflection(
        self: "CastSelf",
    ) -> "_3078.VirtualComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3078,
        )

        return self.__parent__._cast(_3078.VirtualComponentSystemDeflection)

    @property
    def worm_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3080.WormGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3080,
        )

        return self.__parent__._cast(_3080.WormGearSetSystemDeflection)

    @property
    def worm_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3081.WormGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3081,
        )

        return self.__parent__._cast(_3081.WormGearSystemDeflection)

    @property
    def zerol_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_3083.ZerolBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3083,
        )

        return self.__parent__._cast(_3083.ZerolBevelGearSetSystemDeflection)

    @property
    def zerol_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3084.ZerolBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3084,
        )

        return self.__parent__._cast(_3084.ZerolBevelGearSystemDeflection)

    @property
    def abstract_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6589.AbstractAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6589,
        )

        return self.__parent__._cast(_6589.AbstractAssemblyDynamicAnalysis)

    @property
    def abstract_shaft_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6590.AbstractShaftDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6590,
        )

        return self.__parent__._cast(_6590.AbstractShaftDynamicAnalysis)

    @property
    def abstract_shaft_or_housing_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6591.AbstractShaftOrHousingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6591,
        )

        return self.__parent__._cast(_6591.AbstractShaftOrHousingDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6593.AGMAGleasonConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6593,
        )

        return self.__parent__._cast(_6593.AGMAGleasonConicalGearDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6595.AGMAGleasonConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6595,
        )

        return self.__parent__._cast(_6595.AGMAGleasonConicalGearSetDynamicAnalysis)

    @property
    def assembly_dynamic_analysis(self: "CastSelf") -> "_6596.AssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6596,
        )

        return self.__parent__._cast(_6596.AssemblyDynamicAnalysis)

    @property
    def bearing_dynamic_analysis(self: "CastSelf") -> "_6597.BearingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6597,
        )

        return self.__parent__._cast(_6597.BearingDynamicAnalysis)

    @property
    def belt_drive_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6599.BeltDriveDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6599,
        )

        return self.__parent__._cast(_6599.BeltDriveDynamicAnalysis)

    @property
    def bevel_differential_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6600.BevelDifferentialGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6600,
        )

        return self.__parent__._cast(_6600.BevelDifferentialGearDynamicAnalysis)

    @property
    def bevel_differential_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6602.BevelDifferentialGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6602,
        )

        return self.__parent__._cast(_6602.BevelDifferentialGearSetDynamicAnalysis)

    @property
    def bevel_differential_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6603.BevelDifferentialPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6603,
        )

        return self.__parent__._cast(_6603.BevelDifferentialPlanetGearDynamicAnalysis)

    @property
    def bevel_differential_sun_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6604.BevelDifferentialSunGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6604,
        )

        return self.__parent__._cast(_6604.BevelDifferentialSunGearDynamicAnalysis)

    @property
    def bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6605.BevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6605,
        )

        return self.__parent__._cast(_6605.BevelGearDynamicAnalysis)

    @property
    def bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6607.BevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6607,
        )

        return self.__parent__._cast(_6607.BevelGearSetDynamicAnalysis)

    @property
    def bolt_dynamic_analysis(self: "CastSelf") -> "_6608.BoltDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6608,
        )

        return self.__parent__._cast(_6608.BoltDynamicAnalysis)

    @property
    def bolted_joint_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6609.BoltedJointDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6609,
        )

        return self.__parent__._cast(_6609.BoltedJointDynamicAnalysis)

    @property
    def clutch_dynamic_analysis(self: "CastSelf") -> "_6611.ClutchDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6611,
        )

        return self.__parent__._cast(_6611.ClutchDynamicAnalysis)

    @property
    def clutch_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6612.ClutchHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6612,
        )

        return self.__parent__._cast(_6612.ClutchHalfDynamicAnalysis)

    @property
    def component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6614.ComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6614,
        )

        return self.__parent__._cast(_6614.ComponentDynamicAnalysis)

    @property
    def concept_coupling_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6616.ConceptCouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6616,
        )

        return self.__parent__._cast(_6616.ConceptCouplingDynamicAnalysis)

    @property
    def concept_coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6617.ConceptCouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6617,
        )

        return self.__parent__._cast(_6617.ConceptCouplingHalfDynamicAnalysis)

    @property
    def concept_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6618.ConceptGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6618,
        )

        return self.__parent__._cast(_6618.ConceptGearDynamicAnalysis)

    @property
    def concept_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6620.ConceptGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6620,
        )

        return self.__parent__._cast(_6620.ConceptGearSetDynamicAnalysis)

    @property
    def conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6621.ConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6621,
        )

        return self.__parent__._cast(_6621.ConicalGearDynamicAnalysis)

    @property
    def conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6623.ConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6623,
        )

        return self.__parent__._cast(_6623.ConicalGearSetDynamicAnalysis)

    @property
    def connector_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6625.ConnectorDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6625,
        )

        return self.__parent__._cast(_6625.ConnectorDynamicAnalysis)

    @property
    def coupling_dynamic_analysis(self: "CastSelf") -> "_6627.CouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6627,
        )

        return self.__parent__._cast(_6627.CouplingDynamicAnalysis)

    @property
    def coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6628.CouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6628,
        )

        return self.__parent__._cast(_6628.CouplingHalfDynamicAnalysis)

    @property
    def cvt_dynamic_analysis(self: "CastSelf") -> "_6630.CVTDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6630,
        )

        return self.__parent__._cast(_6630.CVTDynamicAnalysis)

    @property
    def cvt_pulley_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6631.CVTPulleyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6631,
        )

        return self.__parent__._cast(_6631.CVTPulleyDynamicAnalysis)

    @property
    def cycloidal_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6632.CycloidalAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6632,
        )

        return self.__parent__._cast(_6632.CycloidalAssemblyDynamicAnalysis)

    @property
    def cycloidal_disc_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6634.CycloidalDiscDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6634,
        )

        return self.__parent__._cast(_6634.CycloidalDiscDynamicAnalysis)

    @property
    def cylindrical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6636.CylindricalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6636,
        )

        return self.__parent__._cast(_6636.CylindricalGearDynamicAnalysis)

    @property
    def cylindrical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6638.CylindricalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6638,
        )

        return self.__parent__._cast(_6638.CylindricalGearSetDynamicAnalysis)

    @property
    def cylindrical_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6639.CylindricalPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6639,
        )

        return self.__parent__._cast(_6639.CylindricalPlanetGearDynamicAnalysis)

    @property
    def datum_dynamic_analysis(self: "CastSelf") -> "_6640.DatumDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6640,
        )

        return self.__parent__._cast(_6640.DatumDynamicAnalysis)

    @property
    def external_cad_model_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6643.ExternalCADModelDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6643,
        )

        return self.__parent__._cast(_6643.ExternalCADModelDynamicAnalysis)

    @property
    def face_gear_dynamic_analysis(self: "CastSelf") -> "_6644.FaceGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6644,
        )

        return self.__parent__._cast(_6644.FaceGearDynamicAnalysis)

    @property
    def face_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6646.FaceGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6646,
        )

        return self.__parent__._cast(_6646.FaceGearSetDynamicAnalysis)

    @property
    def fe_part_dynamic_analysis(self: "CastSelf") -> "_6647.FEPartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6647,
        )

        return self.__parent__._cast(_6647.FEPartDynamicAnalysis)

    @property
    def flexible_pin_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6648.FlexiblePinAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6648,
        )

        return self.__parent__._cast(_6648.FlexiblePinAssemblyDynamicAnalysis)

    @property
    def gear_dynamic_analysis(self: "CastSelf") -> "_6649.GearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6649,
        )

        return self.__parent__._cast(_6649.GearDynamicAnalysis)

    @property
    def gear_set_dynamic_analysis(self: "CastSelf") -> "_6651.GearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6651,
        )

        return self.__parent__._cast(_6651.GearSetDynamicAnalysis)

    @property
    def guide_dxf_model_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6652.GuideDxfModelDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6652,
        )

        return self.__parent__._cast(_6652.GuideDxfModelDynamicAnalysis)

    @property
    def hypoid_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6653.HypoidGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6653,
        )

        return self.__parent__._cast(_6653.HypoidGearDynamicAnalysis)

    @property
    def hypoid_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6655.HypoidGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6655,
        )

        return self.__parent__._cast(_6655.HypoidGearSetDynamicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6657.KlingelnbergCycloPalloidConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6657,
        )

        return self.__parent__._cast(
            _6657.KlingelnbergCycloPalloidConicalGearDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6659.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6659,
        )

        return self.__parent__._cast(
            _6659.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6660.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6660,
        )

        return self.__parent__._cast(
            _6660.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6662.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6662,
        )

        return self.__parent__._cast(
            _6662.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6663.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6663,
        )

        return self.__parent__._cast(
            _6663.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6665.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6665,
        )

        return self.__parent__._cast(
            _6665.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis
        )

    @property
    def mass_disc_dynamic_analysis(self: "CastSelf") -> "_6666.MassDiscDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6666,
        )

        return self.__parent__._cast(_6666.MassDiscDynamicAnalysis)

    @property
    def measurement_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6667.MeasurementComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6667,
        )

        return self.__parent__._cast(_6667.MeasurementComponentDynamicAnalysis)

    @property
    def microphone_array_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6668.MicrophoneArrayDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6668,
        )

        return self.__parent__._cast(_6668.MicrophoneArrayDynamicAnalysis)

    @property
    def microphone_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6669.MicrophoneDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6669,
        )

        return self.__parent__._cast(_6669.MicrophoneDynamicAnalysis)

    @property
    def mountable_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6670.MountableComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6670,
        )

        return self.__parent__._cast(_6670.MountableComponentDynamicAnalysis)

    @property
    def oil_seal_dynamic_analysis(self: "CastSelf") -> "_6671.OilSealDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6671,
        )

        return self.__parent__._cast(_6671.OilSealDynamicAnalysis)

    @property
    def part_dynamic_analysis(self: "CastSelf") -> "_6672.PartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6672,
        )

        return self.__parent__._cast(_6672.PartDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6674.PartToPartShearCouplingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6674,
        )

        return self.__parent__._cast(_6674.PartToPartShearCouplingDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6675.PartToPartShearCouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6675,
        )

        return self.__parent__._cast(_6675.PartToPartShearCouplingHalfDynamicAnalysis)

    @property
    def planetary_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6677.PlanetaryGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6677,
        )

        return self.__parent__._cast(_6677.PlanetaryGearSetDynamicAnalysis)

    @property
    def planet_carrier_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6678.PlanetCarrierDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6678,
        )

        return self.__parent__._cast(_6678.PlanetCarrierDynamicAnalysis)

    @property
    def point_load_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6679.PointLoadDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6679,
        )

        return self.__parent__._cast(_6679.PointLoadDynamicAnalysis)

    @property
    def power_load_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6680.PowerLoadDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6680,
        )

        return self.__parent__._cast(_6680.PowerLoadDynamicAnalysis)

    @property
    def pulley_dynamic_analysis(self: "CastSelf") -> "_6681.PulleyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6681,
        )

        return self.__parent__._cast(_6681.PulleyDynamicAnalysis)

    @property
    def ring_pins_dynamic_analysis(self: "CastSelf") -> "_6682.RingPinsDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6682,
        )

        return self.__parent__._cast(_6682.RingPinsDynamicAnalysis)

    @property
    def rolling_ring_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6684.RollingRingAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6684,
        )

        return self.__parent__._cast(_6684.RollingRingAssemblyDynamicAnalysis)

    @property
    def rolling_ring_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6686.RollingRingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6686,
        )

        return self.__parent__._cast(_6686.RollingRingDynamicAnalysis)

    @property
    def root_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6687.RootAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6687,
        )

        return self.__parent__._cast(_6687.RootAssemblyDynamicAnalysis)

    @property
    def shaft_dynamic_analysis(self: "CastSelf") -> "_6688.ShaftDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6688,
        )

        return self.__parent__._cast(_6688.ShaftDynamicAnalysis)

    @property
    def shaft_hub_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6689.ShaftHubConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6689,
        )

        return self.__parent__._cast(_6689.ShaftHubConnectionDynamicAnalysis)

    @property
    def specialised_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6691.SpecialisedAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6691,
        )

        return self.__parent__._cast(_6691.SpecialisedAssemblyDynamicAnalysis)

    @property
    def spiral_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6692.SpiralBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6692,
        )

        return self.__parent__._cast(_6692.SpiralBevelGearDynamicAnalysis)

    @property
    def spiral_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6694.SpiralBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6694,
        )

        return self.__parent__._cast(_6694.SpiralBevelGearSetDynamicAnalysis)

    @property
    def spring_damper_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6696.SpringDamperDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6696,
        )

        return self.__parent__._cast(_6696.SpringDamperDynamicAnalysis)

    @property
    def spring_damper_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6697.SpringDamperHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6697,
        )

        return self.__parent__._cast(_6697.SpringDamperHalfDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6698.StraightBevelDiffGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6698,
        )

        return self.__parent__._cast(_6698.StraightBevelDiffGearDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6700.StraightBevelDiffGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6700,
        )

        return self.__parent__._cast(_6700.StraightBevelDiffGearSetDynamicAnalysis)

    @property
    def straight_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6701.StraightBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6701,
        )

        return self.__parent__._cast(_6701.StraightBevelGearDynamicAnalysis)

    @property
    def straight_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6703.StraightBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6703,
        )

        return self.__parent__._cast(_6703.StraightBevelGearSetDynamicAnalysis)

    @property
    def straight_bevel_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6704.StraightBevelPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6704,
        )

        return self.__parent__._cast(_6704.StraightBevelPlanetGearDynamicAnalysis)

    @property
    def straight_bevel_sun_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6705.StraightBevelSunGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6705,
        )

        return self.__parent__._cast(_6705.StraightBevelSunGearDynamicAnalysis)

    @property
    def synchroniser_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6706.SynchroniserDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6706,
        )

        return self.__parent__._cast(_6706.SynchroniserDynamicAnalysis)

    @property
    def synchroniser_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6707.SynchroniserHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6707,
        )

        return self.__parent__._cast(_6707.SynchroniserHalfDynamicAnalysis)

    @property
    def synchroniser_part_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6708.SynchroniserPartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6708,
        )

        return self.__parent__._cast(_6708.SynchroniserPartDynamicAnalysis)

    @property
    def synchroniser_sleeve_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6709.SynchroniserSleeveDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6709,
        )

        return self.__parent__._cast(_6709.SynchroniserSleeveDynamicAnalysis)

    @property
    def torque_converter_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6711.TorqueConverterDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6711,
        )

        return self.__parent__._cast(_6711.TorqueConverterDynamicAnalysis)

    @property
    def torque_converter_pump_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6712.TorqueConverterPumpDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6712,
        )

        return self.__parent__._cast(_6712.TorqueConverterPumpDynamicAnalysis)

    @property
    def torque_converter_turbine_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6713.TorqueConverterTurbineDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6713,
        )

        return self.__parent__._cast(_6713.TorqueConverterTurbineDynamicAnalysis)

    @property
    def unbalanced_mass_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6714.UnbalancedMassDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6714,
        )

        return self.__parent__._cast(_6714.UnbalancedMassDynamicAnalysis)

    @property
    def virtual_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6715.VirtualComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6715,
        )

        return self.__parent__._cast(_6715.VirtualComponentDynamicAnalysis)

    @property
    def worm_gear_dynamic_analysis(self: "CastSelf") -> "_6716.WormGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6716,
        )

        return self.__parent__._cast(_6716.WormGearDynamicAnalysis)

    @property
    def worm_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6718.WormGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6718,
        )

        return self.__parent__._cast(_6718.WormGearSetDynamicAnalysis)

    @property
    def zerol_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6719.ZerolBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6719,
        )

        return self.__parent__._cast(_6719.ZerolBevelGearDynamicAnalysis)

    @property
    def zerol_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6721.ZerolBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6721,
        )

        return self.__parent__._cast(_6721.ZerolBevelGearSetDynamicAnalysis)

    @property
    def part_fe_analysis(self: "CastSelf") -> "PartFEAnalysis":
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
class PartFEAnalysis(_7890.PartStaticLoadAnalysisCase):
    """PartFEAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_FE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PartFEAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartFEAnalysis
        """
        return _Cast_PartFEAnalysis(self)
