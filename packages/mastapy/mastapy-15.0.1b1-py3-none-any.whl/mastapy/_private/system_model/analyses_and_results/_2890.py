"""ConnectionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results import _2894

_CONNECTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "ConnectionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7395,
        _7400,
        _7404,
        _7407,
        _7412,
        _7417,
        _7419,
        _7422,
        _7425,
        _7428,
        _7430,
        _7434,
        _7437,
        _7441,
        _7442,
        _7444,
        _7451,
        _7456,
        _7460,
        _7462,
        _7464,
        _7467,
        _7470,
        _7481,
        _7483,
        _7490,
        _7493,
        _7497,
        _7500,
        _7503,
        _7506,
        _7509,
        _7518,
        _7525,
        _7528,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7127,
        _7133,
        _7138,
        _7141,
        _7146,
        _7151,
        _7153,
        _7156,
        _7159,
        _7162,
        _7164,
        _7167,
        _7170,
        _7174,
        _7175,
        _7177,
        _7183,
        _7188,
        _7193,
        _7195,
        _7197,
        _7200,
        _7203,
        _7213,
        _7215,
        _7222,
        _7225,
        _7229,
        _7232,
        _7235,
        _7238,
        _7241,
        _7250,
        _7256,
        _7259,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7882,
        _7883,
        _7884,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6862,
        _6864,
        _6868,
        _6871,
        _6876,
        _6880,
        _6883,
        _6885,
        _6889,
        _6892,
        _6894,
        _6896,
        _6902,
        _6906,
        _6908,
        _6910,
        _6916,
        _6921,
        _6925,
        _6927,
        _6929,
        _6932,
        _6935,
        _6944,
        _6947,
        _6954,
        _6956,
        _6961,
        _6964,
        _6966,
        _6970,
        _6973,
        _6981,
        _6988,
        _6991,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6592,
        _6594,
        _6598,
        _6601,
        _6606,
        _6610,
        _6613,
        _6615,
        _6619,
        _6622,
        _6624,
        _6626,
        _6629,
        _6633,
        _6635,
        _6637,
        _6645,
        _6650,
        _6654,
        _6656,
        _6658,
        _6661,
        _6664,
        _6673,
        _6676,
        _6683,
        _6685,
        _6690,
        _6693,
        _6695,
        _6699,
        _6702,
        _6710,
        _6717,
        _6720,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5972,
        _5974,
        _5978,
        _5981,
        _5986,
        _5990,
        _5993,
        _5996,
        _6000,
        _6003,
        _6005,
        _6007,
        _6010,
        _6014,
        _6016,
        _6018,
        _6039,
        _6046,
        _6065,
        _6067,
        _6069,
        _6072,
        _6075,
        _6085,
        _6089,
        _6097,
        _6099,
        _6104,
        _6109,
        _6111,
        _6116,
        _6119,
        _6127,
        _6135,
        _6138,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6319,
        _6321,
        _6325,
        _6328,
        _6333,
        _6337,
        _6340,
        _6342,
        _6346,
        _6349,
        _6351,
        _6353,
        _6356,
        _6360,
        _6362,
        _6364,
        _6370,
        _6375,
        _6380,
        _6382,
        _6384,
        _6387,
        _6390,
        _6400,
        _6403,
        _6410,
        _6412,
        _6417,
        _6420,
        _6422,
        _6426,
        _6429,
        _6437,
        _6444,
        _6447,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5662,
        _5663,
        _5671,
        _5673,
        _5678,
        _5683,
        _5687,
        _5689,
        _5692,
        _5695,
        _5698,
        _5700,
        _5703,
        _5707,
        _5709,
        _5710,
        _5716,
        _5721,
        _5726,
        _5733,
        _5734,
        _5737,
        _5740,
        _5754,
        _5757,
        _5764,
        _5766,
        _5773,
        _5776,
        _5780,
        _5783,
        _5786,
        _5795,
        _5804,
        _5807,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4845,
        _4846,
        _4851,
        _4853,
        _4858,
        _4863,
        _4866,
        _4868,
        _4871,
        _4874,
        _4877,
        _4880,
        _4883,
        _4887,
        _4889,
        _4890,
        _4899,
        _4905,
        _4909,
        _4912,
        _4913,
        _4916,
        _4919,
        _4936,
        _4939,
        _4946,
        _4948,
        _4954,
        _4956,
        _4959,
        _4962,
        _4965,
        _4974,
        _4983,
        _4986,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5399,
        _5400,
        _5405,
        _5407,
        _5412,
        _5417,
        _5420,
        _5422,
        _5425,
        _5428,
        _5431,
        _5433,
        _5436,
        _5440,
        _5442,
        _5443,
        _5449,
        _5454,
        _5458,
        _5461,
        _5462,
        _5465,
        _5468,
        _5479,
        _5482,
        _5489,
        _5491,
        _5496,
        _5498,
        _5501,
        _5504,
        _5507,
        _5516,
        _5522,
        _5525,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5135,
        _5136,
        _5141,
        _5143,
        _5148,
        _5153,
        _5156,
        _5158,
        _5161,
        _5164,
        _5167,
        _5169,
        _5172,
        _5176,
        _5178,
        _5179,
        _5186,
        _5191,
        _5195,
        _5198,
        _5199,
        _5202,
        _5205,
        _5216,
        _5219,
        _5226,
        _5228,
        _5233,
        _5235,
        _5238,
        _5241,
        _5244,
        _5253,
        _5259,
        _5262,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4564,
        _4565,
        _4570,
        _4572,
        _4577,
        _4582,
        _4585,
        _4587,
        _4590,
        _4593,
        _4596,
        _4598,
        _4601,
        _4605,
        _4607,
        _4608,
        _4621,
        _4626,
        _4630,
        _4633,
        _4634,
        _4637,
        _4640,
        _4662,
        _4665,
        _4672,
        _4674,
        _4679,
        _4681,
        _4684,
        _4687,
        _4690,
        _4699,
        _4705,
        _4708,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4296,
        _4297,
        _4302,
        _4304,
        _4309,
        _4314,
        _4317,
        _4319,
        _4322,
        _4325,
        _4328,
        _4330,
        _4333,
        _4337,
        _4338,
        _4341,
        _4347,
        _4354,
        _4358,
        _4361,
        _4362,
        _4365,
        _4368,
        _4378,
        _4381,
        _4390,
        _4392,
        _4397,
        _4399,
        _4402,
        _4405,
        _4408,
        _4418,
        _4424,
        _4427,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4023,
        _4024,
        _4029,
        _4031,
        _4036,
        _4041,
        _4044,
        _4046,
        _4049,
        _4052,
        _4055,
        _4057,
        _4061,
        _4065,
        _4066,
        _4068,
        _4075,
        _4080,
        _4084,
        _4087,
        _4088,
        _4091,
        _4094,
        _4104,
        _4107,
        _4114,
        _4116,
        _4121,
        _4123,
        _4126,
        _4132,
        _4135,
        _4144,
        _4150,
        _4153,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7678,
        _7683,
        _7689,
        _7692,
        _7697,
        _7701,
        _7705,
        _7707,
        _7711,
        _7715,
        _7718,
        _7720,
        _7723,
        _7727,
        _7729,
        _7732,
        _7754,
        _7761,
        _7775,
        _7780,
        _7782,
        _7785,
        _7788,
        _7800,
        _7803,
        _7815,
        _7817,
        _7822,
        _7825,
        _7827,
        _7831,
        _7834,
        _7844,
        _7855,
        _7858,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3231,
        _3232,
        _3237,
        _3239,
        _3244,
        _3249,
        _3252,
        _3254,
        _3257,
        _3260,
        _3263,
        _3265,
        _3268,
        _3272,
        _3273,
        _3275,
        _3282,
        _3287,
        _3291,
        _3294,
        _3295,
        _3298,
        _3301,
        _3311,
        _3314,
        _3321,
        _3323,
        _3328,
        _3330,
        _3333,
        _3339,
        _3342,
        _3351,
        _3357,
        _3360,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3760,
        _3761,
        _3766,
        _3768,
        _3773,
        _3778,
        _3781,
        _3783,
        _3786,
        _3789,
        _3792,
        _3794,
        _3797,
        _3801,
        _3802,
        _3804,
        _3810,
        _3815,
        _3819,
        _3822,
        _3823,
        _3826,
        _3829,
        _3839,
        _3842,
        _3849,
        _3851,
        _3856,
        _3858,
        _3861,
        _3865,
        _3868,
        _3877,
        _3883,
        _3886,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3497,
        _3498,
        _3503,
        _3505,
        _3510,
        _3515,
        _3518,
        _3520,
        _3523,
        _3526,
        _3529,
        _3531,
        _3534,
        _3538,
        _3539,
        _3541,
        _3547,
        _3552,
        _3556,
        _3559,
        _3560,
        _3563,
        _3566,
        _3576,
        _3579,
        _3586,
        _3588,
        _3593,
        _3595,
        _3598,
        _3602,
        _3605,
        _3614,
        _3620,
        _3623,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2929,
        _2930,
        _2940,
        _2942,
        _2947,
        _2952,
        _2955,
        _2958,
        _2961,
        _2965,
        _2968,
        _2970,
        _2973,
        _2977,
        _2978,
        _2980,
        _2981,
        _2982,
        _2995,
        _3000,
        _3004,
        _3008,
        _3009,
        _3012,
        _3015,
        _3029,
        _3032,
        _3038,
        _3041,
        _3048,
        _3050,
        _3053,
        _3056,
        _3059,
        _3071,
        _3079,
        _3082,
    )

    Self = TypeVar("Self", bound="ConnectionAnalysis")
    CastSelf = TypeVar("CastSelf", bound="ConnectionAnalysis._Cast_ConnectionAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionAnalysis:
    """Special nested class for casting ConnectionAnalysis to subclasses."""

    __parent__: "ConnectionAnalysis"

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2929.AbstractShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2929,
        )

        return self.__parent__._cast(
            _2929.AbstractShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2930.AGMAGleasonConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2930,
        )

        return self.__parent__._cast(_2930.AGMAGleasonConicalGearMeshSystemDeflection)

    @property
    def belt_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2940.BeltConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2940,
        )

        return self.__parent__._cast(_2940.BeltConnectionSystemDeflection)

    @property
    def bevel_differential_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2942.BevelDifferentialGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2942,
        )

        return self.__parent__._cast(_2942.BevelDifferentialGearMeshSystemDeflection)

    @property
    def bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2947.BevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2947,
        )

        return self.__parent__._cast(_2947.BevelGearMeshSystemDeflection)

    @property
    def clutch_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2952.ClutchConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2952,
        )

        return self.__parent__._cast(_2952.ClutchConnectionSystemDeflection)

    @property
    def coaxial_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2955.CoaxialConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2955,
        )

        return self.__parent__._cast(_2955.CoaxialConnectionSystemDeflection)

    @property
    def concept_coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2958.ConceptCouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2958,
        )

        return self.__parent__._cast(_2958.ConceptCouplingConnectionSystemDeflection)

    @property
    def concept_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2961.ConceptGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2961,
        )

        return self.__parent__._cast(_2961.ConceptGearMeshSystemDeflection)

    @property
    def conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2965.ConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2965,
        )

        return self.__parent__._cast(_2965.ConicalGearMeshSystemDeflection)

    @property
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2968.ConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2968,
        )

        return self.__parent__._cast(_2968.ConnectionSystemDeflection)

    @property
    def coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2970.CouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2970,
        )

        return self.__parent__._cast(_2970.CouplingConnectionSystemDeflection)

    @property
    def cvt_belt_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2973.CVTBeltConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2973,
        )

        return self.__parent__._cast(_2973.CVTBeltConnectionSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2977.CycloidalDiscCentralBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2977,
        )

        return self.__parent__._cast(
            _2977.CycloidalDiscCentralBearingConnectionSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2978.CycloidalDiscPlanetaryBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2978,
        )

        return self.__parent__._cast(
            _2978.CycloidalDiscPlanetaryBearingConnectionSystemDeflection
        )

    @property
    def cylindrical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2980.CylindricalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2980,
        )

        return self.__parent__._cast(_2980.CylindricalGearMeshSystemDeflection)

    @property
    def cylindrical_gear_mesh_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2981.CylindricalGearMeshSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2981,
        )

        return self.__parent__._cast(_2981.CylindricalGearMeshSystemDeflectionTimestep)

    @property
    def cylindrical_gear_mesh_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2982.CylindricalGearMeshSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2982,
        )

        return self.__parent__._cast(
            _2982.CylindricalGearMeshSystemDeflectionWithLTCAResults
        )

    @property
    def face_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2995.FaceGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2995,
        )

        return self.__parent__._cast(_2995.FaceGearMeshSystemDeflection)

    @property
    def gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3000.GearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3000,
        )

        return self.__parent__._cast(_3000.GearMeshSystemDeflection)

    @property
    def hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3004.HypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3004,
        )

        return self.__parent__._cast(_3004.HypoidGearMeshSystemDeflection)

    @property
    def inter_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3008.InterMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3008,
        )

        return self.__parent__._cast(
            _3008.InterMountableComponentConnectionSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3009.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3009,
        )

        return self.__parent__._cast(
            _3009.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3012.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3012,
        )

        return self.__parent__._cast(
            _3012.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3015.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3015,
        )

        return self.__parent__._cast(
            _3015.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3029.PartToPartShearCouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3029,
        )

        return self.__parent__._cast(
            _3029.PartToPartShearCouplingConnectionSystemDeflection
        )

    @property
    def planetary_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3032.PlanetaryConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3032,
        )

        return self.__parent__._cast(_3032.PlanetaryConnectionSystemDeflection)

    @property
    def ring_pins_to_disc_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3038.RingPinsToDiscConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3038,
        )

        return self.__parent__._cast(_3038.RingPinsToDiscConnectionSystemDeflection)

    @property
    def rolling_ring_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3041.RollingRingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3041,
        )

        return self.__parent__._cast(_3041.RollingRingConnectionSystemDeflection)

    @property
    def shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3048.ShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3048,
        )

        return self.__parent__._cast(
            _3048.ShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3050.SpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3050,
        )

        return self.__parent__._cast(_3050.SpiralBevelGearMeshSystemDeflection)

    @property
    def spring_damper_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3053.SpringDamperConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3053,
        )

        return self.__parent__._cast(_3053.SpringDamperConnectionSystemDeflection)

    @property
    def straight_bevel_diff_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3056.StraightBevelDiffGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3056,
        )

        return self.__parent__._cast(_3056.StraightBevelDiffGearMeshSystemDeflection)

    @property
    def straight_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3059.StraightBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3059,
        )

        return self.__parent__._cast(_3059.StraightBevelGearMeshSystemDeflection)

    @property
    def torque_converter_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3071.TorqueConverterConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3071,
        )

        return self.__parent__._cast(_3071.TorqueConverterConnectionSystemDeflection)

    @property
    def worm_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3079.WormGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3079,
        )

        return self.__parent__._cast(_3079.WormGearMeshSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3082.ZerolBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3082,
        )

        return self.__parent__._cast(_3082.ZerolBevelGearMeshSystemDeflection)

    @property
    def abstract_shaft_to_mountable_component_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3231.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3231,
        )

        return self.__parent__._cast(
            _3231.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponse
        )

    @property
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3232.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3232,
        )

        return self.__parent__._cast(
            _3232.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def belt_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3237.BeltConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3237,
        )

        return self.__parent__._cast(_3237.BeltConnectionSteadyStateSynchronousResponse)

    @property
    def bevel_differential_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3239.BevelDifferentialGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3239,
        )

        return self.__parent__._cast(
            _3239.BevelDifferentialGearMeshSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3244.BevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3244,
        )

        return self.__parent__._cast(_3244.BevelGearMeshSteadyStateSynchronousResponse)

    @property
    def clutch_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3249.ClutchConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3249,
        )

        return self.__parent__._cast(
            _3249.ClutchConnectionSteadyStateSynchronousResponse
        )

    @property
    def coaxial_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3252.CoaxialConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3252,
        )

        return self.__parent__._cast(
            _3252.CoaxialConnectionSteadyStateSynchronousResponse
        )

    @property
    def concept_coupling_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3254.ConceptCouplingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3254,
        )

        return self.__parent__._cast(
            _3254.ConceptCouplingConnectionSteadyStateSynchronousResponse
        )

    @property
    def concept_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3257.ConceptGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3257,
        )

        return self.__parent__._cast(
            _3257.ConceptGearMeshSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3260.ConicalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3260,
        )

        return self.__parent__._cast(
            _3260.ConicalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3263.ConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3263,
        )

        return self.__parent__._cast(_3263.ConnectionSteadyStateSynchronousResponse)

    @property
    def coupling_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3265.CouplingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3265,
        )

        return self.__parent__._cast(
            _3265.CouplingConnectionSteadyStateSynchronousResponse
        )

    @property
    def cvt_belt_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3268.CVTBeltConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3268,
        )

        return self.__parent__._cast(
            _3268.CVTBeltConnectionSteadyStateSynchronousResponse
        )

    @property
    def cycloidal_disc_central_bearing_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3272.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3272,
        )

        return self.__parent__._cast(
            _3272.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponse
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3273.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3273,
        )

        return self.__parent__._cast(
            _3273.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3275.CylindricalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3275,
        )

        return self.__parent__._cast(
            _3275.CylindricalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def face_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3282.FaceGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3282,
        )

        return self.__parent__._cast(_3282.FaceGearMeshSteadyStateSynchronousResponse)

    @property
    def gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3287.GearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3287,
        )

        return self.__parent__._cast(_3287.GearMeshSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3291.HypoidGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3291,
        )

        return self.__parent__._cast(_3291.HypoidGearMeshSteadyStateSynchronousResponse)

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3294.InterMountableComponentConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3294,
        )

        return self.__parent__._cast(
            _3294.InterMountableComponentConnectionSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3295.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3295,
        )

        return self.__parent__._cast(
            _3295.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3298.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3298,
        )

        return self.__parent__._cast(
            _3298.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3301.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3301,
        )

        return self.__parent__._cast(
            _3301.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def part_to_part_shear_coupling_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3311.PartToPartShearCouplingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3311,
        )

        return self.__parent__._cast(
            _3311.PartToPartShearCouplingConnectionSteadyStateSynchronousResponse
        )

    @property
    def planetary_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3314.PlanetaryConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3314,
        )

        return self.__parent__._cast(
            _3314.PlanetaryConnectionSteadyStateSynchronousResponse
        )

    @property
    def ring_pins_to_disc_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3321.RingPinsToDiscConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3321,
        )

        return self.__parent__._cast(
            _3321.RingPinsToDiscConnectionSteadyStateSynchronousResponse
        )

    @property
    def rolling_ring_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3323.RollingRingConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3323,
        )

        return self.__parent__._cast(
            _3323.RollingRingConnectionSteadyStateSynchronousResponse
        )

    @property
    def shaft_to_mountable_component_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3328.ShaftToMountableComponentConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3328,
        )

        return self.__parent__._cast(
            _3328.ShaftToMountableComponentConnectionSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3330.SpiralBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3330,
        )

        return self.__parent__._cast(
            _3330.SpiralBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def spring_damper_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3333.SpringDamperConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3333,
        )

        return self.__parent__._cast(
            _3333.SpringDamperConnectionSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3339.StraightBevelDiffGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3339,
        )

        return self.__parent__._cast(
            _3339.StraightBevelDiffGearMeshSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3342.StraightBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3342,
        )

        return self.__parent__._cast(
            _3342.StraightBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3351.TorqueConverterConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3351,
        )

        return self.__parent__._cast(
            _3351.TorqueConverterConnectionSteadyStateSynchronousResponse
        )

    @property
    def worm_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3357.WormGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3357,
        )

        return self.__parent__._cast(_3357.WormGearMeshSteadyStateSynchronousResponse)

    @property
    def zerol_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3360.ZerolBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3360,
        )

        return self.__parent__._cast(
            _3360.ZerolBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def abstract_shaft_to_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3497.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3497,
        )

        return self.__parent__._cast(
            _3497.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3498.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3498,
        )

        return self.__parent__._cast(
            _3498.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def belt_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3503.BeltConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3503,
        )

        return self.__parent__._cast(
            _3503.BeltConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3505.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3505,
        )

        return self.__parent__._cast(
            _3505.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3510.BevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3510,
        )

        return self.__parent__._cast(
            _3510.BevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def clutch_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3515.ClutchConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3515,
        )

        return self.__parent__._cast(
            _3515.ClutchConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coaxial_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3518.CoaxialConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3518,
        )

        return self.__parent__._cast(
            _3518.CoaxialConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3520.ConceptCouplingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3520,
        )

        return self.__parent__._cast(
            _3520.ConceptCouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3523.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3523,
        )

        return self.__parent__._cast(
            _3523.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3526.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3526,
        )

        return self.__parent__._cast(
            _3526.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3529.ConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3529,
        )

        return self.__parent__._cast(
            _3529.ConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3531.CouplingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3531,
        )

        return self.__parent__._cast(
            _3531.CouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cvt_belt_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3534.CVTBeltConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3534,
        )

        return self.__parent__._cast(
            _3534.CVTBeltConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_central_bearing_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3538.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3538,
        )

        return self.__parent__._cast(
            _3538.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3539.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3539,
        )

        return self.__parent__._cast(
            _3539.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3541.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3541,
        )

        return self.__parent__._cast(
            _3541.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def face_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3547.FaceGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3547,
        )

        return self.__parent__._cast(
            _3547.FaceGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3552.GearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3552,
        )

        return self.__parent__._cast(
            _3552.GearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def hypoid_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3556.HypoidGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3556,
        )

        return self.__parent__._cast(
            _3556.HypoidGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3559.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3559,
        )

        return self.__parent__._cast(
            _3559.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3560.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3560,
        )

        return self.__parent__._cast(
            _3560.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3563.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3563,
        )

        return self.__parent__._cast(
            _3563.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3566.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3566,
        )

        return self.__parent__._cast(
            _3566.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_to_part_shear_coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3576.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3576,
        )

        return self.__parent__._cast(
            _3576.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def planetary_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3579.PlanetaryConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3579,
        )

        return self.__parent__._cast(
            _3579.PlanetaryConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def ring_pins_to_disc_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3586.RingPinsToDiscConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3586,
        )

        return self.__parent__._cast(
            _3586.RingPinsToDiscConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def rolling_ring_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3588.RollingRingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3588,
        )

        return self.__parent__._cast(
            _3588.RollingRingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def shaft_to_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3593.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3593,
        )

        return self.__parent__._cast(
            _3593.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3595.SpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3595,
        )

        return self.__parent__._cast(
            _3595.SpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spring_damper_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3598.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3598,
        )

        return self.__parent__._cast(
            _3598.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3602.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3602,
        )

        return self.__parent__._cast(
            _3602.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3605.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3605,
        )

        return self.__parent__._cast(
            _3605.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3614.TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3614,
        )

        return self.__parent__._cast(
            _3614.TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def worm_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3620.WormGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3620,
        )

        return self.__parent__._cast(
            _3620.WormGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3623.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3623,
        )

        return self.__parent__._cast(
            _3623.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_shaft_to_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3760.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3760,
        )

        return self.__parent__._cast(
            _3760.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3761.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3761,
        )

        return self.__parent__._cast(
            _3761.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def belt_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3766.BeltConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3766,
        )

        return self.__parent__._cast(
            _3766.BeltConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3768.BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3768,
        )

        return self.__parent__._cast(
            _3768.BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3773.BevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3773,
        )

        return self.__parent__._cast(
            _3773.BevelGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def clutch_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3778.ClutchConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3778,
        )

        return self.__parent__._cast(
            _3778.ClutchConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coaxial_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3781.CoaxialConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3781,
        )

        return self.__parent__._cast(
            _3781.CoaxialConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3783.ConceptCouplingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3783,
        )

        return self.__parent__._cast(
            _3783.ConceptCouplingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3786.ConceptGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3786,
        )

        return self.__parent__._cast(
            _3786.ConceptGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3789.ConicalGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3789,
        )

        return self.__parent__._cast(
            _3789.ConicalGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3792.ConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3792,
        )

        return self.__parent__._cast(
            _3792.ConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3794.CouplingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3794,
        )

        return self.__parent__._cast(
            _3794.CouplingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cvt_belt_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3797.CVTBeltConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3797,
        )

        return self.__parent__._cast(
            _3797.CVTBeltConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cycloidal_disc_central_bearing_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3801.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3801,
        )

        return self.__parent__._cast(
            _3801.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3802.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3802,
        )

        return self.__parent__._cast(
            _3802.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3804.CylindricalGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3804,
        )

        return self.__parent__._cast(
            _3804.CylindricalGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def face_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3810.FaceGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3810,
        )

        return self.__parent__._cast(
            _3810.FaceGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3815.GearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3815,
        )

        return self.__parent__._cast(
            _3815.GearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def hypoid_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3819.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3819,
        )

        return self.__parent__._cast(
            _3819.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3822.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3822,
        )

        return self.__parent__._cast(
            _3822.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3823.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3823,
        )

        return self.__parent__._cast(
            _3823.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3826.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3826,
        )

        return self.__parent__._cast(
            _3826.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3829.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3829,
        )

        return self.__parent__._cast(
            _3829.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_to_part_shear_coupling_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3839.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3839,
        )

        return self.__parent__._cast(
            _3839.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def planetary_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3842.PlanetaryConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3842,
        )

        return self.__parent__._cast(
            _3842.PlanetaryConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def ring_pins_to_disc_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3849.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3849,
        )

        return self.__parent__._cast(
            _3849.RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def rolling_ring_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3851.RollingRingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3851,
        )

        return self.__parent__._cast(
            _3851.RollingRingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def shaft_to_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3856.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3856,
        )

        return self.__parent__._cast(
            _3856.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spiral_bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3858.SpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3858,
        )

        return self.__parent__._cast(
            _3858.SpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3861.SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3861,
        )

        return self.__parent__._cast(
            _3861.SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_diff_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3865.StraightBevelDiffGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3865,
        )

        return self.__parent__._cast(
            _3865.StraightBevelDiffGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3868.StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3868,
        )

        return self.__parent__._cast(
            _3868.StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3877.TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3877,
        )

        return self.__parent__._cast(
            _3877.TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def worm_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3883.WormGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3883,
        )

        return self.__parent__._cast(
            _3883.WormGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def zerol_bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3886.ZerolBevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3886,
        )

        return self.__parent__._cast(
            _3886.ZerolBevelGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_shaft_to_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4023.AbstractShaftToMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4023,
        )

        return self.__parent__._cast(
            _4023.AbstractShaftToMountableComponentConnectionStabilityAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4024.AGMAGleasonConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4024,
        )

        return self.__parent__._cast(_4024.AGMAGleasonConicalGearMeshStabilityAnalysis)

    @property
    def belt_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4029.BeltConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4029,
        )

        return self.__parent__._cast(_4029.BeltConnectionStabilityAnalysis)

    @property
    def bevel_differential_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4031.BevelDifferentialGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4031,
        )

        return self.__parent__._cast(_4031.BevelDifferentialGearMeshStabilityAnalysis)

    @property
    def bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4036.BevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4036,
        )

        return self.__parent__._cast(_4036.BevelGearMeshStabilityAnalysis)

    @property
    def clutch_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4041.ClutchConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4041,
        )

        return self.__parent__._cast(_4041.ClutchConnectionStabilityAnalysis)

    @property
    def coaxial_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4044.CoaxialConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4044,
        )

        return self.__parent__._cast(_4044.CoaxialConnectionStabilityAnalysis)

    @property
    def concept_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4046.ConceptCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4046,
        )

        return self.__parent__._cast(_4046.ConceptCouplingConnectionStabilityAnalysis)

    @property
    def concept_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4049.ConceptGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4049,
        )

        return self.__parent__._cast(_4049.ConceptGearMeshStabilityAnalysis)

    @property
    def conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4052.ConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4052,
        )

        return self.__parent__._cast(_4052.ConicalGearMeshStabilityAnalysis)

    @property
    def connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4055.ConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4055,
        )

        return self.__parent__._cast(_4055.ConnectionStabilityAnalysis)

    @property
    def coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4057.CouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4057,
        )

        return self.__parent__._cast(_4057.CouplingConnectionStabilityAnalysis)

    @property
    def cvt_belt_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4061.CVTBeltConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4061,
        )

        return self.__parent__._cast(_4061.CVTBeltConnectionStabilityAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4065.CycloidalDiscCentralBearingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4065,
        )

        return self.__parent__._cast(
            _4065.CycloidalDiscCentralBearingConnectionStabilityAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4066.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4066,
        )

        return self.__parent__._cast(
            _4066.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis
        )

    @property
    def cylindrical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4068.CylindricalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4068,
        )

        return self.__parent__._cast(_4068.CylindricalGearMeshStabilityAnalysis)

    @property
    def face_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4075.FaceGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4075,
        )

        return self.__parent__._cast(_4075.FaceGearMeshStabilityAnalysis)

    @property
    def gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4080.GearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4080,
        )

        return self.__parent__._cast(_4080.GearMeshStabilityAnalysis)

    @property
    def hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4084.HypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4084,
        )

        return self.__parent__._cast(_4084.HypoidGearMeshStabilityAnalysis)

    @property
    def inter_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4087.InterMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4087,
        )

        return self.__parent__._cast(
            _4087.InterMountableComponentConnectionStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4088.KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4088,
        )

        return self.__parent__._cast(
            _4088.KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4091.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4091,
        )

        return self.__parent__._cast(
            _4091.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4094.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4094,
        )

        return self.__parent__._cast(
            _4094.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4104.PartToPartShearCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4104,
        )

        return self.__parent__._cast(
            _4104.PartToPartShearCouplingConnectionStabilityAnalysis
        )

    @property
    def planetary_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4107.PlanetaryConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4107,
        )

        return self.__parent__._cast(_4107.PlanetaryConnectionStabilityAnalysis)

    @property
    def ring_pins_to_disc_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4114.RingPinsToDiscConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4114,
        )

        return self.__parent__._cast(_4114.RingPinsToDiscConnectionStabilityAnalysis)

    @property
    def rolling_ring_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4116.RollingRingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4116,
        )

        return self.__parent__._cast(_4116.RollingRingConnectionStabilityAnalysis)

    @property
    def shaft_to_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4121.ShaftToMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4121,
        )

        return self.__parent__._cast(
            _4121.ShaftToMountableComponentConnectionStabilityAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4123.SpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4123,
        )

        return self.__parent__._cast(_4123.SpiralBevelGearMeshStabilityAnalysis)

    @property
    def spring_damper_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4126.SpringDamperConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4126,
        )

        return self.__parent__._cast(_4126.SpringDamperConnectionStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4132.StraightBevelDiffGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4132,
        )

        return self.__parent__._cast(_4132.StraightBevelDiffGearMeshStabilityAnalysis)

    @property
    def straight_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4135.StraightBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4135,
        )

        return self.__parent__._cast(_4135.StraightBevelGearMeshStabilityAnalysis)

    @property
    def torque_converter_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4144.TorqueConverterConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4144,
        )

        return self.__parent__._cast(_4144.TorqueConverterConnectionStabilityAnalysis)

    @property
    def worm_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4150.WormGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4150,
        )

        return self.__parent__._cast(_4150.WormGearMeshStabilityAnalysis)

    @property
    def zerol_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4153.ZerolBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4153,
        )

        return self.__parent__._cast(_4153.ZerolBevelGearMeshStabilityAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4296.AbstractShaftToMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4296

        return self.__parent__._cast(
            _4296.AbstractShaftToMountableComponentConnectionPowerFlow
        )

    @property
    def agma_gleason_conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4297.AGMAGleasonConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4297

        return self.__parent__._cast(_4297.AGMAGleasonConicalGearMeshPowerFlow)

    @property
    def belt_connection_power_flow(self: "CastSelf") -> "_4302.BeltConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4302

        return self.__parent__._cast(_4302.BeltConnectionPowerFlow)

    @property
    def bevel_differential_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4304.BevelDifferentialGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4304

        return self.__parent__._cast(_4304.BevelDifferentialGearMeshPowerFlow)

    @property
    def bevel_gear_mesh_power_flow(self: "CastSelf") -> "_4309.BevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4309

        return self.__parent__._cast(_4309.BevelGearMeshPowerFlow)

    @property
    def clutch_connection_power_flow(
        self: "CastSelf",
    ) -> "_4314.ClutchConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4314

        return self.__parent__._cast(_4314.ClutchConnectionPowerFlow)

    @property
    def coaxial_connection_power_flow(
        self: "CastSelf",
    ) -> "_4317.CoaxialConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4317

        return self.__parent__._cast(_4317.CoaxialConnectionPowerFlow)

    @property
    def concept_coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4319.ConceptCouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4319

        return self.__parent__._cast(_4319.ConceptCouplingConnectionPowerFlow)

    @property
    def concept_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4322.ConceptGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4322

        return self.__parent__._cast(_4322.ConceptGearMeshPowerFlow)

    @property
    def conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4325.ConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4325

        return self.__parent__._cast(_4325.ConicalGearMeshPowerFlow)

    @property
    def connection_power_flow(self: "CastSelf") -> "_4328.ConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4328

        return self.__parent__._cast(_4328.ConnectionPowerFlow)

    @property
    def coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4330.CouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4330

        return self.__parent__._cast(_4330.CouplingConnectionPowerFlow)

    @property
    def cvt_belt_connection_power_flow(
        self: "CastSelf",
    ) -> "_4333.CVTBeltConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4333

        return self.__parent__._cast(_4333.CVTBeltConnectionPowerFlow)

    @property
    def cycloidal_disc_central_bearing_connection_power_flow(
        self: "CastSelf",
    ) -> "_4337.CycloidalDiscCentralBearingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4337

        return self.__parent__._cast(
            _4337.CycloidalDiscCentralBearingConnectionPowerFlow
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_power_flow(
        self: "CastSelf",
    ) -> "_4338.CycloidalDiscPlanetaryBearingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4338

        return self.__parent__._cast(
            _4338.CycloidalDiscPlanetaryBearingConnectionPowerFlow
        )

    @property
    def cylindrical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4341.CylindricalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4341

        return self.__parent__._cast(_4341.CylindricalGearMeshPowerFlow)

    @property
    def face_gear_mesh_power_flow(self: "CastSelf") -> "_4347.FaceGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4347

        return self.__parent__._cast(_4347.FaceGearMeshPowerFlow)

    @property
    def gear_mesh_power_flow(self: "CastSelf") -> "_4354.GearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4354

        return self.__parent__._cast(_4354.GearMeshPowerFlow)

    @property
    def hypoid_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4358.HypoidGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4358

        return self.__parent__._cast(_4358.HypoidGearMeshPowerFlow)

    @property
    def inter_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4361.InterMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4361

        return self.__parent__._cast(_4361.InterMountableComponentConnectionPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4362.KlingelnbergCycloPalloidConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4362

        return self.__parent__._cast(
            _4362.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4365.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4365

        return self.__parent__._cast(
            _4365.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4368.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4368

        return self.__parent__._cast(
            _4368.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
        )

    @property
    def part_to_part_shear_coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4378.PartToPartShearCouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4378

        return self.__parent__._cast(_4378.PartToPartShearCouplingConnectionPowerFlow)

    @property
    def planetary_connection_power_flow(
        self: "CastSelf",
    ) -> "_4381.PlanetaryConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4381

        return self.__parent__._cast(_4381.PlanetaryConnectionPowerFlow)

    @property
    def ring_pins_to_disc_connection_power_flow(
        self: "CastSelf",
    ) -> "_4390.RingPinsToDiscConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4390

        return self.__parent__._cast(_4390.RingPinsToDiscConnectionPowerFlow)

    @property
    def rolling_ring_connection_power_flow(
        self: "CastSelf",
    ) -> "_4392.RollingRingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4392

        return self.__parent__._cast(_4392.RollingRingConnectionPowerFlow)

    @property
    def shaft_to_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4397.ShaftToMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4397

        return self.__parent__._cast(_4397.ShaftToMountableComponentConnectionPowerFlow)

    @property
    def spiral_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4399.SpiralBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4399

        return self.__parent__._cast(_4399.SpiralBevelGearMeshPowerFlow)

    @property
    def spring_damper_connection_power_flow(
        self: "CastSelf",
    ) -> "_4402.SpringDamperConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4402

        return self.__parent__._cast(_4402.SpringDamperConnectionPowerFlow)

    @property
    def straight_bevel_diff_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4405.StraightBevelDiffGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4405

        return self.__parent__._cast(_4405.StraightBevelDiffGearMeshPowerFlow)

    @property
    def straight_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4408.StraightBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4408

        return self.__parent__._cast(_4408.StraightBevelGearMeshPowerFlow)

    @property
    def torque_converter_connection_power_flow(
        self: "CastSelf",
    ) -> "_4418.TorqueConverterConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4418

        return self.__parent__._cast(_4418.TorqueConverterConnectionPowerFlow)

    @property
    def worm_gear_mesh_power_flow(self: "CastSelf") -> "_4424.WormGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4424

        return self.__parent__._cast(_4424.WormGearMeshPowerFlow)

    @property
    def zerol_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4427.ZerolBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4427

        return self.__parent__._cast(_4427.ZerolBevelGearMeshPowerFlow)

    @property
    def abstract_shaft_to_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4564.AbstractShaftToMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4564,
        )

        return self.__parent__._cast(
            _4564.AbstractShaftToMountableComponentConnectionParametricStudyTool
        )

    @property
    def agma_gleason_conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4565.AGMAGleasonConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4565,
        )

        return self.__parent__._cast(
            _4565.AGMAGleasonConicalGearMeshParametricStudyTool
        )

    @property
    def belt_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4570.BeltConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4570,
        )

        return self.__parent__._cast(_4570.BeltConnectionParametricStudyTool)

    @property
    def bevel_differential_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4572.BevelDifferentialGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4572,
        )

        return self.__parent__._cast(_4572.BevelDifferentialGearMeshParametricStudyTool)

    @property
    def bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4577.BevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4577,
        )

        return self.__parent__._cast(_4577.BevelGearMeshParametricStudyTool)

    @property
    def clutch_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4582.ClutchConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4582,
        )

        return self.__parent__._cast(_4582.ClutchConnectionParametricStudyTool)

    @property
    def coaxial_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4585.CoaxialConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4585,
        )

        return self.__parent__._cast(_4585.CoaxialConnectionParametricStudyTool)

    @property
    def concept_coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4587.ConceptCouplingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4587,
        )

        return self.__parent__._cast(_4587.ConceptCouplingConnectionParametricStudyTool)

    @property
    def concept_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4590.ConceptGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4590,
        )

        return self.__parent__._cast(_4590.ConceptGearMeshParametricStudyTool)

    @property
    def conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4593.ConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4593,
        )

        return self.__parent__._cast(_4593.ConicalGearMeshParametricStudyTool)

    @property
    def connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4596.ConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4596,
        )

        return self.__parent__._cast(_4596.ConnectionParametricStudyTool)

    @property
    def coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4598.CouplingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4598,
        )

        return self.__parent__._cast(_4598.CouplingConnectionParametricStudyTool)

    @property
    def cvt_belt_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4601.CVTBeltConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4601,
        )

        return self.__parent__._cast(_4601.CVTBeltConnectionParametricStudyTool)

    @property
    def cycloidal_disc_central_bearing_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4605.CycloidalDiscCentralBearingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4605,
        )

        return self.__parent__._cast(
            _4605.CycloidalDiscCentralBearingConnectionParametricStudyTool
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4607.CycloidalDiscPlanetaryBearingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4607,
        )

        return self.__parent__._cast(
            _4607.CycloidalDiscPlanetaryBearingConnectionParametricStudyTool
        )

    @property
    def cylindrical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4608.CylindricalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4608,
        )

        return self.__parent__._cast(_4608.CylindricalGearMeshParametricStudyTool)

    @property
    def face_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4621.FaceGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4621,
        )

        return self.__parent__._cast(_4621.FaceGearMeshParametricStudyTool)

    @property
    def gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4626.GearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4626,
        )

        return self.__parent__._cast(_4626.GearMeshParametricStudyTool)

    @property
    def hypoid_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4630.HypoidGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4630,
        )

        return self.__parent__._cast(_4630.HypoidGearMeshParametricStudyTool)

    @property
    def inter_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4633.InterMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4633,
        )

        return self.__parent__._cast(
            _4633.InterMountableComponentConnectionParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4634.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4634,
        )

        return self.__parent__._cast(
            _4634.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4637.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4637,
        )

        return self.__parent__._cast(
            _4637.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4640.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4640,
        )

        return self.__parent__._cast(
            _4640.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool
        )

    @property
    def part_to_part_shear_coupling_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4662.PartToPartShearCouplingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4662,
        )

        return self.__parent__._cast(
            _4662.PartToPartShearCouplingConnectionParametricStudyTool
        )

    @property
    def planetary_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4665.PlanetaryConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4665,
        )

        return self.__parent__._cast(_4665.PlanetaryConnectionParametricStudyTool)

    @property
    def ring_pins_to_disc_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4672.RingPinsToDiscConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4672,
        )

        return self.__parent__._cast(_4672.RingPinsToDiscConnectionParametricStudyTool)

    @property
    def rolling_ring_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4674.RollingRingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4674,
        )

        return self.__parent__._cast(_4674.RollingRingConnectionParametricStudyTool)

    @property
    def shaft_to_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4679.ShaftToMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4679,
        )

        return self.__parent__._cast(
            _4679.ShaftToMountableComponentConnectionParametricStudyTool
        )

    @property
    def spiral_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4681.SpiralBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4681,
        )

        return self.__parent__._cast(_4681.SpiralBevelGearMeshParametricStudyTool)

    @property
    def spring_damper_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4684.SpringDamperConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4684,
        )

        return self.__parent__._cast(_4684.SpringDamperConnectionParametricStudyTool)

    @property
    def straight_bevel_diff_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4687.StraightBevelDiffGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4687,
        )

        return self.__parent__._cast(_4687.StraightBevelDiffGearMeshParametricStudyTool)

    @property
    def straight_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4690.StraightBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4690,
        )

        return self.__parent__._cast(_4690.StraightBevelGearMeshParametricStudyTool)

    @property
    def torque_converter_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4699.TorqueConverterConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4699,
        )

        return self.__parent__._cast(_4699.TorqueConverterConnectionParametricStudyTool)

    @property
    def worm_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4705.WormGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4705,
        )

        return self.__parent__._cast(_4705.WormGearMeshParametricStudyTool)

    @property
    def zerol_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4708.ZerolBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4708,
        )

        return self.__parent__._cast(_4708.ZerolBevelGearMeshParametricStudyTool)

    @property
    def abstract_shaft_to_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4845.AbstractShaftToMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4845,
        )

        return self.__parent__._cast(
            _4845.AbstractShaftToMountableComponentConnectionModalAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4846.AGMAGleasonConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4846,
        )

        return self.__parent__._cast(_4846.AGMAGleasonConicalGearMeshModalAnalysis)

    @property
    def belt_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4851.BeltConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4851,
        )

        return self.__parent__._cast(_4851.BeltConnectionModalAnalysis)

    @property
    def bevel_differential_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4853.BevelDifferentialGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4853,
        )

        return self.__parent__._cast(_4853.BevelDifferentialGearMeshModalAnalysis)

    @property
    def bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4858.BevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4858,
        )

        return self.__parent__._cast(_4858.BevelGearMeshModalAnalysis)

    @property
    def clutch_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4863.ClutchConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4863,
        )

        return self.__parent__._cast(_4863.ClutchConnectionModalAnalysis)

    @property
    def coaxial_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4866.CoaxialConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4866,
        )

        return self.__parent__._cast(_4866.CoaxialConnectionModalAnalysis)

    @property
    def concept_coupling_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4868.ConceptCouplingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4868,
        )

        return self.__parent__._cast(_4868.ConceptCouplingConnectionModalAnalysis)

    @property
    def concept_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4871.ConceptGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4871,
        )

        return self.__parent__._cast(_4871.ConceptGearMeshModalAnalysis)

    @property
    def conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4874.ConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4874,
        )

        return self.__parent__._cast(_4874.ConicalGearMeshModalAnalysis)

    @property
    def connection_modal_analysis(self: "CastSelf") -> "_4877.ConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4877,
        )

        return self.__parent__._cast(_4877.ConnectionModalAnalysis)

    @property
    def coupling_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4880.CouplingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4880,
        )

        return self.__parent__._cast(_4880.CouplingConnectionModalAnalysis)

    @property
    def cvt_belt_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4883.CVTBeltConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4883,
        )

        return self.__parent__._cast(_4883.CVTBeltConnectionModalAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4887.CycloidalDiscCentralBearingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4887,
        )

        return self.__parent__._cast(
            _4887.CycloidalDiscCentralBearingConnectionModalAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4889.CycloidalDiscPlanetaryBearingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4889,
        )

        return self.__parent__._cast(
            _4889.CycloidalDiscPlanetaryBearingConnectionModalAnalysis
        )

    @property
    def cylindrical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4890.CylindricalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4890,
        )

        return self.__parent__._cast(_4890.CylindricalGearMeshModalAnalysis)

    @property
    def face_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4899.FaceGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4899,
        )

        return self.__parent__._cast(_4899.FaceGearMeshModalAnalysis)

    @property
    def gear_mesh_modal_analysis(self: "CastSelf") -> "_4905.GearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4905,
        )

        return self.__parent__._cast(_4905.GearMeshModalAnalysis)

    @property
    def hypoid_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4909.HypoidGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4909,
        )

        return self.__parent__._cast(_4909.HypoidGearMeshModalAnalysis)

    @property
    def inter_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4912.InterMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4912,
        )

        return self.__parent__._cast(
            _4912.InterMountableComponentConnectionModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4913.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4913,
        )

        return self.__parent__._cast(
            _4913.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4916.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4916,
        )

        return self.__parent__._cast(
            _4916.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4919.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4919,
        )

        return self.__parent__._cast(
            _4919.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4936.PartToPartShearCouplingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4936,
        )

        return self.__parent__._cast(
            _4936.PartToPartShearCouplingConnectionModalAnalysis
        )

    @property
    def planetary_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4939.PlanetaryConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4939,
        )

        return self.__parent__._cast(_4939.PlanetaryConnectionModalAnalysis)

    @property
    def ring_pins_to_disc_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4946.RingPinsToDiscConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4946,
        )

        return self.__parent__._cast(_4946.RingPinsToDiscConnectionModalAnalysis)

    @property
    def rolling_ring_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4948.RollingRingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4948,
        )

        return self.__parent__._cast(_4948.RollingRingConnectionModalAnalysis)

    @property
    def shaft_to_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4954.ShaftToMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4954,
        )

        return self.__parent__._cast(
            _4954.ShaftToMountableComponentConnectionModalAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4956.SpiralBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4956,
        )

        return self.__parent__._cast(_4956.SpiralBevelGearMeshModalAnalysis)

    @property
    def spring_damper_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4959.SpringDamperConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4959,
        )

        return self.__parent__._cast(_4959.SpringDamperConnectionModalAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4962.StraightBevelDiffGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4962,
        )

        return self.__parent__._cast(_4962.StraightBevelDiffGearMeshModalAnalysis)

    @property
    def straight_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4965.StraightBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4965,
        )

        return self.__parent__._cast(_4965.StraightBevelGearMeshModalAnalysis)

    @property
    def torque_converter_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4974.TorqueConverterConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4974,
        )

        return self.__parent__._cast(_4974.TorqueConverterConnectionModalAnalysis)

    @property
    def worm_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4983.WormGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4983,
        )

        return self.__parent__._cast(_4983.WormGearMeshModalAnalysis)

    @property
    def zerol_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4986.ZerolBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4986,
        )

        return self.__parent__._cast(_4986.ZerolBevelGearMeshModalAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5135.AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5135,
        )

        return self.__parent__._cast(
            _5135.AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness
        )

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5136.AGMAGleasonConicalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5136,
        )

        return self.__parent__._cast(
            _5136.AGMAGleasonConicalGearMeshModalAnalysisAtAStiffness
        )

    @property
    def belt_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5141.BeltConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5141,
        )

        return self.__parent__._cast(_5141.BeltConnectionModalAnalysisAtAStiffness)

    @property
    def bevel_differential_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5143.BevelDifferentialGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5143,
        )

        return self.__parent__._cast(
            _5143.BevelDifferentialGearMeshModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5148.BevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5148,
        )

        return self.__parent__._cast(_5148.BevelGearMeshModalAnalysisAtAStiffness)

    @property
    def clutch_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5153.ClutchConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5153,
        )

        return self.__parent__._cast(_5153.ClutchConnectionModalAnalysisAtAStiffness)

    @property
    def coaxial_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5156.CoaxialConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5156,
        )

        return self.__parent__._cast(_5156.CoaxialConnectionModalAnalysisAtAStiffness)

    @property
    def concept_coupling_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5158.ConceptCouplingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5158,
        )

        return self.__parent__._cast(
            _5158.ConceptCouplingConnectionModalAnalysisAtAStiffness
        )

    @property
    def concept_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5161.ConceptGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5161,
        )

        return self.__parent__._cast(_5161.ConceptGearMeshModalAnalysisAtAStiffness)

    @property
    def conical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5164.ConicalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5164,
        )

        return self.__parent__._cast(_5164.ConicalGearMeshModalAnalysisAtAStiffness)

    @property
    def connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5167.ConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5167,
        )

        return self.__parent__._cast(_5167.ConnectionModalAnalysisAtAStiffness)

    @property
    def coupling_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5169.CouplingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5169,
        )

        return self.__parent__._cast(_5169.CouplingConnectionModalAnalysisAtAStiffness)

    @property
    def cvt_belt_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5172.CVTBeltConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5172,
        )

        return self.__parent__._cast(_5172.CVTBeltConnectionModalAnalysisAtAStiffness)

    @property
    def cycloidal_disc_central_bearing_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5176.CycloidalDiscCentralBearingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5176,
        )

        return self.__parent__._cast(
            _5176.CycloidalDiscCentralBearingConnectionModalAnalysisAtAStiffness
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5178.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5178,
        )

        return self.__parent__._cast(
            _5178.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness
        )

    @property
    def cylindrical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5179.CylindricalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5179,
        )

        return self.__parent__._cast(_5179.CylindricalGearMeshModalAnalysisAtAStiffness)

    @property
    def face_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5186.FaceGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5186,
        )

        return self.__parent__._cast(_5186.FaceGearMeshModalAnalysisAtAStiffness)

    @property
    def gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5191.GearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5191,
        )

        return self.__parent__._cast(_5191.GearMeshModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5195.HypoidGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5195,
        )

        return self.__parent__._cast(_5195.HypoidGearMeshModalAnalysisAtAStiffness)

    @property
    def inter_mountable_component_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5198.InterMountableComponentConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5198,
        )

        return self.__parent__._cast(
            _5198.InterMountableComponentConnectionModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5199.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5199,
        )

        return self.__parent__._cast(
            _5199.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5202.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5202,
        )

        return self.__parent__._cast(
            _5202.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5205.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5205,
        )

        return self.__parent__._cast(
            _5205.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtAStiffness
        )

    @property
    def part_to_part_shear_coupling_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5216.PartToPartShearCouplingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5216,
        )

        return self.__parent__._cast(
            _5216.PartToPartShearCouplingConnectionModalAnalysisAtAStiffness
        )

    @property
    def planetary_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5219.PlanetaryConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5219,
        )

        return self.__parent__._cast(_5219.PlanetaryConnectionModalAnalysisAtAStiffness)

    @property
    def ring_pins_to_disc_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5226.RingPinsToDiscConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5226,
        )

        return self.__parent__._cast(
            _5226.RingPinsToDiscConnectionModalAnalysisAtAStiffness
        )

    @property
    def rolling_ring_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5228.RollingRingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5228,
        )

        return self.__parent__._cast(
            _5228.RollingRingConnectionModalAnalysisAtAStiffness
        )

    @property
    def shaft_to_mountable_component_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5233.ShaftToMountableComponentConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5233,
        )

        return self.__parent__._cast(
            _5233.ShaftToMountableComponentConnectionModalAnalysisAtAStiffness
        )

    @property
    def spiral_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5235.SpiralBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5235,
        )

        return self.__parent__._cast(_5235.SpiralBevelGearMeshModalAnalysisAtAStiffness)

    @property
    def spring_damper_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5238.SpringDamperConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5238,
        )

        return self.__parent__._cast(
            _5238.SpringDamperConnectionModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5241.StraightBevelDiffGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5241,
        )

        return self.__parent__._cast(
            _5241.StraightBevelDiffGearMeshModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5244.StraightBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5244,
        )

        return self.__parent__._cast(
            _5244.StraightBevelGearMeshModalAnalysisAtAStiffness
        )

    @property
    def torque_converter_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5253.TorqueConverterConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5253,
        )

        return self.__parent__._cast(
            _5253.TorqueConverterConnectionModalAnalysisAtAStiffness
        )

    @property
    def worm_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5259.WormGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5259,
        )

        return self.__parent__._cast(_5259.WormGearMeshModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5262.ZerolBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5262,
        )

        return self.__parent__._cast(_5262.ZerolBevelGearMeshModalAnalysisAtAStiffness)

    @property
    def abstract_shaft_to_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5399.AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5399,
        )

        return self.__parent__._cast(
            _5399.AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed
        )

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5400.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5400,
        )

        return self.__parent__._cast(
            _5400.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed
        )

    @property
    def belt_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5405.BeltConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5405,
        )

        return self.__parent__._cast(_5405.BeltConnectionModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5407.BevelDifferentialGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5407,
        )

        return self.__parent__._cast(
            _5407.BevelDifferentialGearMeshModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5412.BevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5412,
        )

        return self.__parent__._cast(_5412.BevelGearMeshModalAnalysisAtASpeed)

    @property
    def clutch_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5417.ClutchConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5417,
        )

        return self.__parent__._cast(_5417.ClutchConnectionModalAnalysisAtASpeed)

    @property
    def coaxial_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5420.CoaxialConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5420,
        )

        return self.__parent__._cast(_5420.CoaxialConnectionModalAnalysisAtASpeed)

    @property
    def concept_coupling_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5422.ConceptCouplingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5422,
        )

        return self.__parent__._cast(
            _5422.ConceptCouplingConnectionModalAnalysisAtASpeed
        )

    @property
    def concept_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5425.ConceptGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5425,
        )

        return self.__parent__._cast(_5425.ConceptGearMeshModalAnalysisAtASpeed)

    @property
    def conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5428.ConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5428,
        )

        return self.__parent__._cast(_5428.ConicalGearMeshModalAnalysisAtASpeed)

    @property
    def connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5431.ConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5431,
        )

        return self.__parent__._cast(_5431.ConnectionModalAnalysisAtASpeed)

    @property
    def coupling_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5433.CouplingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5433,
        )

        return self.__parent__._cast(_5433.CouplingConnectionModalAnalysisAtASpeed)

    @property
    def cvt_belt_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5436.CVTBeltConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5436,
        )

        return self.__parent__._cast(_5436.CVTBeltConnectionModalAnalysisAtASpeed)

    @property
    def cycloidal_disc_central_bearing_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5440.CycloidalDiscCentralBearingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5440,
        )

        return self.__parent__._cast(
            _5440.CycloidalDiscCentralBearingConnectionModalAnalysisAtASpeed
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5442.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5442,
        )

        return self.__parent__._cast(
            _5442.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed
        )

    @property
    def cylindrical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5443.CylindricalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5443,
        )

        return self.__parent__._cast(_5443.CylindricalGearMeshModalAnalysisAtASpeed)

    @property
    def face_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5449.FaceGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5449,
        )

        return self.__parent__._cast(_5449.FaceGearMeshModalAnalysisAtASpeed)

    @property
    def gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5454.GearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5454,
        )

        return self.__parent__._cast(_5454.GearMeshModalAnalysisAtASpeed)

    @property
    def hypoid_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5458.HypoidGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5458,
        )

        return self.__parent__._cast(_5458.HypoidGearMeshModalAnalysisAtASpeed)

    @property
    def inter_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5461.InterMountableComponentConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5461,
        )

        return self.__parent__._cast(
            _5461.InterMountableComponentConnectionModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5462.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5462,
        )

        return self.__parent__._cast(
            _5462.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5465.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5465,
        )

        return self.__parent__._cast(
            _5465.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5468.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5468,
        )

        return self.__parent__._cast(
            _5468.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed
        )

    @property
    def part_to_part_shear_coupling_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5479.PartToPartShearCouplingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5479,
        )

        return self.__parent__._cast(
            _5479.PartToPartShearCouplingConnectionModalAnalysisAtASpeed
        )

    @property
    def planetary_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5482.PlanetaryConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5482,
        )

        return self.__parent__._cast(_5482.PlanetaryConnectionModalAnalysisAtASpeed)

    @property
    def ring_pins_to_disc_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5489.RingPinsToDiscConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5489,
        )

        return self.__parent__._cast(
            _5489.RingPinsToDiscConnectionModalAnalysisAtASpeed
        )

    @property
    def rolling_ring_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5491.RollingRingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5491,
        )

        return self.__parent__._cast(_5491.RollingRingConnectionModalAnalysisAtASpeed)

    @property
    def shaft_to_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5496.ShaftToMountableComponentConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5496,
        )

        return self.__parent__._cast(
            _5496.ShaftToMountableComponentConnectionModalAnalysisAtASpeed
        )

    @property
    def spiral_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5498.SpiralBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5498,
        )

        return self.__parent__._cast(_5498.SpiralBevelGearMeshModalAnalysisAtASpeed)

    @property
    def spring_damper_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5501.SpringDamperConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5501,
        )

        return self.__parent__._cast(_5501.SpringDamperConnectionModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5504.StraightBevelDiffGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5504,
        )

        return self.__parent__._cast(
            _5504.StraightBevelDiffGearMeshModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5507.StraightBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5507,
        )

        return self.__parent__._cast(_5507.StraightBevelGearMeshModalAnalysisAtASpeed)

    @property
    def torque_converter_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5516.TorqueConverterConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5516,
        )

        return self.__parent__._cast(
            _5516.TorqueConverterConnectionModalAnalysisAtASpeed
        )

    @property
    def worm_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5522.WormGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5522,
        )

        return self.__parent__._cast(_5522.WormGearMeshModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5525.ZerolBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5525,
        )

        return self.__parent__._cast(_5525.ZerolBevelGearMeshModalAnalysisAtASpeed)

    @property
    def abstract_shaft_to_mountable_component_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5662.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5662,
        )

        return self.__parent__._cast(
            _5662.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5663.AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5663,
        )

        return self.__parent__._cast(
            _5663.AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def belt_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5671.BeltConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5671,
        )

        return self.__parent__._cast(_5671.BeltConnectionMultibodyDynamicsAnalysis)

    @property
    def bevel_differential_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5673.BevelDifferentialGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5673,
        )

        return self.__parent__._cast(
            _5673.BevelDifferentialGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5678.BevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5678,
        )

        return self.__parent__._cast(_5678.BevelGearMeshMultibodyDynamicsAnalysis)

    @property
    def clutch_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5683.ClutchConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5683,
        )

        return self.__parent__._cast(_5683.ClutchConnectionMultibodyDynamicsAnalysis)

    @property
    def coaxial_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5687.CoaxialConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5687,
        )

        return self.__parent__._cast(_5687.CoaxialConnectionMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5689.ConceptCouplingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5689,
        )

        return self.__parent__._cast(
            _5689.ConceptCouplingConnectionMultibodyDynamicsAnalysis
        )

    @property
    def concept_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5692.ConceptGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5692,
        )

        return self.__parent__._cast(_5692.ConceptGearMeshMultibodyDynamicsAnalysis)

    @property
    def conical_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5695.ConicalGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5695,
        )

        return self.__parent__._cast(_5695.ConicalGearMeshMultibodyDynamicsAnalysis)

    @property
    def connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5698.ConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5698,
        )

        return self.__parent__._cast(_5698.ConnectionMultibodyDynamicsAnalysis)

    @property
    def coupling_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5700.CouplingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5700,
        )

        return self.__parent__._cast(_5700.CouplingConnectionMultibodyDynamicsAnalysis)

    @property
    def cvt_belt_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5703.CVTBeltConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5703,
        )

        return self.__parent__._cast(_5703.CVTBeltConnectionMultibodyDynamicsAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5707.CycloidalDiscCentralBearingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5707,
        )

        return self.__parent__._cast(
            _5707.CycloidalDiscCentralBearingConnectionMultibodyDynamicsAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5709.CycloidalDiscPlanetaryBearingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5709,
        )

        return self.__parent__._cast(
            _5709.CycloidalDiscPlanetaryBearingConnectionMultibodyDynamicsAnalysis
        )

    @property
    def cylindrical_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5710.CylindricalGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5710,
        )

        return self.__parent__._cast(_5710.CylindricalGearMeshMultibodyDynamicsAnalysis)

    @property
    def face_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5716.FaceGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5716,
        )

        return self.__parent__._cast(_5716.FaceGearMeshMultibodyDynamicsAnalysis)

    @property
    def gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5721.GearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5721,
        )

        return self.__parent__._cast(_5721.GearMeshMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5726.HypoidGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5726,
        )

        return self.__parent__._cast(_5726.HypoidGearMeshMultibodyDynamicsAnalysis)

    @property
    def inter_mountable_component_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5733.InterMountableComponentConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5733,
        )

        return self.__parent__._cast(
            _5733.InterMountableComponentConnectionMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5734.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5734,
        )

        return self.__parent__._cast(
            _5734.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5737.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5737,
        )

        return self.__parent__._cast(
            _5737.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5740.KlingelnbergCycloPalloidSpiralBevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5740,
        )

        return self.__parent__._cast(
            _5740.KlingelnbergCycloPalloidSpiralBevelGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5754.PartToPartShearCouplingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5754,
        )

        return self.__parent__._cast(
            _5754.PartToPartShearCouplingConnectionMultibodyDynamicsAnalysis
        )

    @property
    def planetary_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5757.PlanetaryConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5757,
        )

        return self.__parent__._cast(_5757.PlanetaryConnectionMultibodyDynamicsAnalysis)

    @property
    def ring_pins_to_disc_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5764.RingPinsToDiscConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5764,
        )

        return self.__parent__._cast(
            _5764.RingPinsToDiscConnectionMultibodyDynamicsAnalysis
        )

    @property
    def rolling_ring_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5766.RollingRingConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5766,
        )

        return self.__parent__._cast(
            _5766.RollingRingConnectionMultibodyDynamicsAnalysis
        )

    @property
    def shaft_to_mountable_component_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5773.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5773,
        )

        return self.__parent__._cast(
            _5773.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5776.SpiralBevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5776,
        )

        return self.__parent__._cast(_5776.SpiralBevelGearMeshMultibodyDynamicsAnalysis)

    @property
    def spring_damper_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5780.SpringDamperConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5780,
        )

        return self.__parent__._cast(
            _5780.SpringDamperConnectionMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5783.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5783,
        )

        return self.__parent__._cast(
            _5783.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5786.StraightBevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5786,
        )

        return self.__parent__._cast(
            _5786.StraightBevelGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def torque_converter_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5795.TorqueConverterConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5795,
        )

        return self.__parent__._cast(
            _5795.TorqueConverterConnectionMultibodyDynamicsAnalysis
        )

    @property
    def worm_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5804.WormGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5804,
        )

        return self.__parent__._cast(_5804.WormGearMeshMultibodyDynamicsAnalysis)

    @property
    def zerol_bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5807.ZerolBevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5807,
        )

        return self.__parent__._cast(_5807.ZerolBevelGearMeshMultibodyDynamicsAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5972.AbstractShaftToMountableComponentConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5972,
        )

        return self.__parent__._cast(
            _5972.AbstractShaftToMountableComponentConnectionHarmonicAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5974.AGMAGleasonConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5974,
        )

        return self.__parent__._cast(_5974.AGMAGleasonConicalGearMeshHarmonicAnalysis)

    @property
    def belt_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5978.BeltConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5978,
        )

        return self.__parent__._cast(_5978.BeltConnectionHarmonicAnalysis)

    @property
    def bevel_differential_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5981.BevelDifferentialGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5981,
        )

        return self.__parent__._cast(_5981.BevelDifferentialGearMeshHarmonicAnalysis)

    @property
    def bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5986.BevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5986,
        )

        return self.__parent__._cast(_5986.BevelGearMeshHarmonicAnalysis)

    @property
    def clutch_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5990.ClutchConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5990,
        )

        return self.__parent__._cast(_5990.ClutchConnectionHarmonicAnalysis)

    @property
    def coaxial_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5993.CoaxialConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5993,
        )

        return self.__parent__._cast(_5993.CoaxialConnectionHarmonicAnalysis)

    @property
    def concept_coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5996.ConceptCouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5996,
        )

        return self.__parent__._cast(_5996.ConceptCouplingConnectionHarmonicAnalysis)

    @property
    def concept_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6000.ConceptGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6000,
        )

        return self.__parent__._cast(_6000.ConceptGearMeshHarmonicAnalysis)

    @property
    def conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6003.ConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6003,
        )

        return self.__parent__._cast(_6003.ConicalGearMeshHarmonicAnalysis)

    @property
    def connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6005.ConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6005,
        )

        return self.__parent__._cast(_6005.ConnectionHarmonicAnalysis)

    @property
    def coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6007.CouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6007,
        )

        return self.__parent__._cast(_6007.CouplingConnectionHarmonicAnalysis)

    @property
    def cvt_belt_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6010.CVTBeltConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6010,
        )

        return self.__parent__._cast(_6010.CVTBeltConnectionHarmonicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6014.CycloidalDiscCentralBearingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6014,
        )

        return self.__parent__._cast(
            _6014.CycloidalDiscCentralBearingConnectionHarmonicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6016.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6016,
        )

        return self.__parent__._cast(
            _6016.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis
        )

    @property
    def cylindrical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6018.CylindricalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6018,
        )

        return self.__parent__._cast(_6018.CylindricalGearMeshHarmonicAnalysis)

    @property
    def face_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6039.FaceGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6039,
        )

        return self.__parent__._cast(_6039.FaceGearMeshHarmonicAnalysis)

    @property
    def gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6046.GearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6046,
        )

        return self.__parent__._cast(_6046.GearMeshHarmonicAnalysis)

    @property
    def hypoid_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6065.HypoidGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6065,
        )

        return self.__parent__._cast(_6065.HypoidGearMeshHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6067.InterMountableComponentConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6067,
        )

        return self.__parent__._cast(
            _6067.InterMountableComponentConnectionHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6069.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6069,
        )

        return self.__parent__._cast(
            _6069.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6072.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6072,
        )

        return self.__parent__._cast(
            _6072.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6075.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6075,
        )

        return self.__parent__._cast(
            _6075.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6085.PartToPartShearCouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6085,
        )

        return self.__parent__._cast(
            _6085.PartToPartShearCouplingConnectionHarmonicAnalysis
        )

    @property
    def planetary_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6089.PlanetaryConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6089,
        )

        return self.__parent__._cast(_6089.PlanetaryConnectionHarmonicAnalysis)

    @property
    def ring_pins_to_disc_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6097.RingPinsToDiscConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6097,
        )

        return self.__parent__._cast(_6097.RingPinsToDiscConnectionHarmonicAnalysis)

    @property
    def rolling_ring_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6099.RollingRingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6099,
        )

        return self.__parent__._cast(_6099.RollingRingConnectionHarmonicAnalysis)

    @property
    def shaft_to_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6104.ShaftToMountableComponentConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6104,
        )

        return self.__parent__._cast(
            _6104.ShaftToMountableComponentConnectionHarmonicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6109.SpiralBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6109,
        )

        return self.__parent__._cast(_6109.SpiralBevelGearMeshHarmonicAnalysis)

    @property
    def spring_damper_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6111.SpringDamperConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6111,
        )

        return self.__parent__._cast(_6111.SpringDamperConnectionHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6116.StraightBevelDiffGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6116,
        )

        return self.__parent__._cast(_6116.StraightBevelDiffGearMeshHarmonicAnalysis)

    @property
    def straight_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6119.StraightBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6119,
        )

        return self.__parent__._cast(_6119.StraightBevelGearMeshHarmonicAnalysis)

    @property
    def torque_converter_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6127.TorqueConverterConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6127,
        )

        return self.__parent__._cast(_6127.TorqueConverterConnectionHarmonicAnalysis)

    @property
    def worm_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6135.WormGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6135,
        )

        return self.__parent__._cast(_6135.WormGearMeshHarmonicAnalysis)

    @property
    def zerol_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6138.ZerolBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6138,
        )

        return self.__parent__._cast(_6138.ZerolBevelGearMeshHarmonicAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6319.AbstractShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6319,
        )

        return self.__parent__._cast(
            _6319.AbstractShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6321.AGMAGleasonConicalGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6321,
        )

        return self.__parent__._cast(
            _6321.AGMAGleasonConicalGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def belt_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6325.BeltConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6325,
        )

        return self.__parent__._cast(
            _6325.BeltConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6328.BevelDifferentialGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6328,
        )

        return self.__parent__._cast(
            _6328.BevelDifferentialGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6333.BevelGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6333,
        )

        return self.__parent__._cast(
            _6333.BevelGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def clutch_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6337.ClutchConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6337,
        )

        return self.__parent__._cast(
            _6337.ClutchConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coaxial_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6340.CoaxialConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6340,
        )

        return self.__parent__._cast(
            _6340.CoaxialConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_coupling_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6342.ConceptCouplingConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6342,
        )

        return self.__parent__._cast(
            _6342.ConceptCouplingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6346.ConceptGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6346,
        )

        return self.__parent__._cast(
            _6346.ConceptGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6349.ConicalGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6349,
        )

        return self.__parent__._cast(
            _6349.ConicalGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6351.ConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6351,
        )

        return self.__parent__._cast(_6351.ConnectionHarmonicAnalysisOfSingleExcitation)

    @property
    def coupling_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6353.CouplingConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6353,
        )

        return self.__parent__._cast(
            _6353.CouplingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cvt_belt_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6356.CVTBeltConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6356,
        )

        return self.__parent__._cast(
            _6356.CVTBeltConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_central_bearing_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> (
        "_6360.CycloidalDiscCentralBearingConnectionHarmonicAnalysisOfSingleExcitation"
    ):
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6360,
        )

        return self.__parent__._cast(
            _6360.CycloidalDiscCentralBearingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6362.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6362,
        )

        return self.__parent__._cast(
            _6362.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6364.CylindricalGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6364,
        )

        return self.__parent__._cast(
            _6364.CylindricalGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def face_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6370.FaceGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6370,
        )

        return self.__parent__._cast(
            _6370.FaceGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6375.GearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6375,
        )

        return self.__parent__._cast(_6375.GearMeshHarmonicAnalysisOfSingleExcitation)

    @property
    def hypoid_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6380.HypoidGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6380,
        )

        return self.__parent__._cast(
            _6380.HypoidGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def inter_mountable_component_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6382.InterMountableComponentConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6382,
        )

        return self.__parent__._cast(
            _6382.InterMountableComponentConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6384.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6384,
        )

        return self.__parent__._cast(
            _6384.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> (
        "_6387.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysisOfSingleExcitation"
    ):
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6387,
        )

        return self.__parent__._cast(
            _6387.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6390.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6390,
        )

        return self.__parent__._cast(
            _6390.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_to_part_shear_coupling_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6400.PartToPartShearCouplingConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6400,
        )

        return self.__parent__._cast(
            _6400.PartToPartShearCouplingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planetary_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6403.PlanetaryConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6403,
        )

        return self.__parent__._cast(
            _6403.PlanetaryConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def ring_pins_to_disc_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6410.RingPinsToDiscConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6410,
        )

        return self.__parent__._cast(
            _6410.RingPinsToDiscConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def rolling_ring_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6412.RollingRingConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6412,
        )

        return self.__parent__._cast(
            _6412.RollingRingConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def shaft_to_mountable_component_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6417.ShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6417,
        )

        return self.__parent__._cast(
            _6417.ShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6420.SpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6420,
        )

        return self.__parent__._cast(
            _6420.SpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6422.SpringDamperConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6422,
        )

        return self.__parent__._cast(
            _6422.SpringDamperConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6426.StraightBevelDiffGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6426,
        )

        return self.__parent__._cast(
            _6426.StraightBevelDiffGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6429.StraightBevelGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6429,
        )

        return self.__parent__._cast(
            _6429.StraightBevelGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6437.TorqueConverterConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6437,
        )

        return self.__parent__._cast(
            _6437.TorqueConverterConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def worm_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6444.WormGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6444,
        )

        return self.__parent__._cast(
            _6444.WormGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_mesh_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6447.ZerolBevelGearMeshHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6447,
        )

        return self.__parent__._cast(
            _6447.ZerolBevelGearMeshHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6592.AbstractShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6592,
        )

        return self.__parent__._cast(
            _6592.AbstractShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6594.AGMAGleasonConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6594,
        )

        return self.__parent__._cast(_6594.AGMAGleasonConicalGearMeshDynamicAnalysis)

    @property
    def belt_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6598.BeltConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6598,
        )

        return self.__parent__._cast(_6598.BeltConnectionDynamicAnalysis)

    @property
    def bevel_differential_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6601.BevelDifferentialGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6601,
        )

        return self.__parent__._cast(_6601.BevelDifferentialGearMeshDynamicAnalysis)

    @property
    def bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6606.BevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6606,
        )

        return self.__parent__._cast(_6606.BevelGearMeshDynamicAnalysis)

    @property
    def clutch_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6610.ClutchConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6610,
        )

        return self.__parent__._cast(_6610.ClutchConnectionDynamicAnalysis)

    @property
    def coaxial_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6613.CoaxialConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6613,
        )

        return self.__parent__._cast(_6613.CoaxialConnectionDynamicAnalysis)

    @property
    def concept_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6615.ConceptCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6615,
        )

        return self.__parent__._cast(_6615.ConceptCouplingConnectionDynamicAnalysis)

    @property
    def concept_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6619.ConceptGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6619,
        )

        return self.__parent__._cast(_6619.ConceptGearMeshDynamicAnalysis)

    @property
    def conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6622.ConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6622,
        )

        return self.__parent__._cast(_6622.ConicalGearMeshDynamicAnalysis)

    @property
    def connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6624.ConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6624,
        )

        return self.__parent__._cast(_6624.ConnectionDynamicAnalysis)

    @property
    def coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6626.CouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6626,
        )

        return self.__parent__._cast(_6626.CouplingConnectionDynamicAnalysis)

    @property
    def cvt_belt_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6629.CVTBeltConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6629,
        )

        return self.__parent__._cast(_6629.CVTBeltConnectionDynamicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6633.CycloidalDiscCentralBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6633,
        )

        return self.__parent__._cast(
            _6633.CycloidalDiscCentralBearingConnectionDynamicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6635.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6635,
        )

        return self.__parent__._cast(
            _6635.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis
        )

    @property
    def cylindrical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6637.CylindricalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6637,
        )

        return self.__parent__._cast(_6637.CylindricalGearMeshDynamicAnalysis)

    @property
    def face_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6645.FaceGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6645,
        )

        return self.__parent__._cast(_6645.FaceGearMeshDynamicAnalysis)

    @property
    def gear_mesh_dynamic_analysis(self: "CastSelf") -> "_6650.GearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6650,
        )

        return self.__parent__._cast(_6650.GearMeshDynamicAnalysis)

    @property
    def hypoid_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6654.HypoidGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6654,
        )

        return self.__parent__._cast(_6654.HypoidGearMeshDynamicAnalysis)

    @property
    def inter_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6656.InterMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6656,
        )

        return self.__parent__._cast(
            _6656.InterMountableComponentConnectionDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6658.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6658,
        )

        return self.__parent__._cast(
            _6658.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6661.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6661,
        )

        return self.__parent__._cast(
            _6661.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6664.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6664,
        )

        return self.__parent__._cast(
            _6664.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6673.PartToPartShearCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6673,
        )

        return self.__parent__._cast(
            _6673.PartToPartShearCouplingConnectionDynamicAnalysis
        )

    @property
    def planetary_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6676.PlanetaryConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6676,
        )

        return self.__parent__._cast(_6676.PlanetaryConnectionDynamicAnalysis)

    @property
    def ring_pins_to_disc_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6683.RingPinsToDiscConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6683,
        )

        return self.__parent__._cast(_6683.RingPinsToDiscConnectionDynamicAnalysis)

    @property
    def rolling_ring_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6685.RollingRingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6685,
        )

        return self.__parent__._cast(_6685.RollingRingConnectionDynamicAnalysis)

    @property
    def shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6690.ShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6690,
        )

        return self.__parent__._cast(
            _6690.ShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6693.SpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6693,
        )

        return self.__parent__._cast(_6693.SpiralBevelGearMeshDynamicAnalysis)

    @property
    def spring_damper_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6695.SpringDamperConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6695,
        )

        return self.__parent__._cast(_6695.SpringDamperConnectionDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6699.StraightBevelDiffGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6699,
        )

        return self.__parent__._cast(_6699.StraightBevelDiffGearMeshDynamicAnalysis)

    @property
    def straight_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6702.StraightBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6702,
        )

        return self.__parent__._cast(_6702.StraightBevelGearMeshDynamicAnalysis)

    @property
    def torque_converter_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6710.TorqueConverterConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6710,
        )

        return self.__parent__._cast(_6710.TorqueConverterConnectionDynamicAnalysis)

    @property
    def worm_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6717.WormGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6717,
        )

        return self.__parent__._cast(_6717.WormGearMeshDynamicAnalysis)

    @property
    def zerol_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6720.ZerolBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6720,
        )

        return self.__parent__._cast(_6720.ZerolBevelGearMeshDynamicAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6862.AbstractShaftToMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6862,
        )

        return self.__parent__._cast(
            _6862.AbstractShaftToMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6864.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6864,
        )

        return self.__parent__._cast(
            _6864.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis
        )

    @property
    def belt_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6868.BeltConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6868,
        )

        return self.__parent__._cast(_6868.BeltConnectionCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6871.BevelDifferentialGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6871,
        )

        return self.__parent__._cast(
            _6871.BevelDifferentialGearMeshCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6876.BevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6876,
        )

        return self.__parent__._cast(_6876.BevelGearMeshCriticalSpeedAnalysis)

    @property
    def clutch_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6880.ClutchConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6880,
        )

        return self.__parent__._cast(_6880.ClutchConnectionCriticalSpeedAnalysis)

    @property
    def coaxial_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6883.CoaxialConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6883,
        )

        return self.__parent__._cast(_6883.CoaxialConnectionCriticalSpeedAnalysis)

    @property
    def concept_coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6885.ConceptCouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6885,
        )

        return self.__parent__._cast(
            _6885.ConceptCouplingConnectionCriticalSpeedAnalysis
        )

    @property
    def concept_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6889.ConceptGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6889,
        )

        return self.__parent__._cast(_6889.ConceptGearMeshCriticalSpeedAnalysis)

    @property
    def conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6892.ConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6892,
        )

        return self.__parent__._cast(_6892.ConicalGearMeshCriticalSpeedAnalysis)

    @property
    def connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6894.ConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6894,
        )

        return self.__parent__._cast(_6894.ConnectionCriticalSpeedAnalysis)

    @property
    def coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6896.CouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6896,
        )

        return self.__parent__._cast(_6896.CouplingConnectionCriticalSpeedAnalysis)

    @property
    def cvt_belt_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6902.CVTBeltConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6902,
        )

        return self.__parent__._cast(_6902.CVTBeltConnectionCriticalSpeedAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6906.CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6906,
        )

        return self.__parent__._cast(
            _6906.CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6908.CycloidalDiscPlanetaryBearingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6908,
        )

        return self.__parent__._cast(
            _6908.CycloidalDiscPlanetaryBearingConnectionCriticalSpeedAnalysis
        )

    @property
    def cylindrical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6910.CylindricalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6910,
        )

        return self.__parent__._cast(_6910.CylindricalGearMeshCriticalSpeedAnalysis)

    @property
    def face_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6916.FaceGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6916,
        )

        return self.__parent__._cast(_6916.FaceGearMeshCriticalSpeedAnalysis)

    @property
    def gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6921.GearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6921,
        )

        return self.__parent__._cast(_6921.GearMeshCriticalSpeedAnalysis)

    @property
    def hypoid_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6925.HypoidGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6925,
        )

        return self.__parent__._cast(_6925.HypoidGearMeshCriticalSpeedAnalysis)

    @property
    def inter_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6927.InterMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6927,
        )

        return self.__parent__._cast(
            _6927.InterMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6929.KlingelnbergCycloPalloidConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6929,
        )

        return self.__parent__._cast(
            _6929.KlingelnbergCycloPalloidConicalGearMeshCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6932.KlingelnbergCycloPalloidHypoidGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6932,
        )

        return self.__parent__._cast(
            _6932.KlingelnbergCycloPalloidHypoidGearMeshCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6935.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6935,
        )

        return self.__parent__._cast(
            _6935.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6944.PartToPartShearCouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6944,
        )

        return self.__parent__._cast(
            _6944.PartToPartShearCouplingConnectionCriticalSpeedAnalysis
        )

    @property
    def planetary_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6947.PlanetaryConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6947,
        )

        return self.__parent__._cast(_6947.PlanetaryConnectionCriticalSpeedAnalysis)

    @property
    def ring_pins_to_disc_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6954.RingPinsToDiscConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6954,
        )

        return self.__parent__._cast(
            _6954.RingPinsToDiscConnectionCriticalSpeedAnalysis
        )

    @property
    def rolling_ring_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6956.RollingRingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6956,
        )

        return self.__parent__._cast(_6956.RollingRingConnectionCriticalSpeedAnalysis)

    @property
    def shaft_to_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6961.ShaftToMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6961,
        )

        return self.__parent__._cast(
            _6961.ShaftToMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6964.SpiralBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6964,
        )

        return self.__parent__._cast(_6964.SpiralBevelGearMeshCriticalSpeedAnalysis)

    @property
    def spring_damper_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6966.SpringDamperConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6966,
        )

        return self.__parent__._cast(_6966.SpringDamperConnectionCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6970.StraightBevelDiffGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6970,
        )

        return self.__parent__._cast(
            _6970.StraightBevelDiffGearMeshCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6973.StraightBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6973,
        )

        return self.__parent__._cast(_6973.StraightBevelGearMeshCriticalSpeedAnalysis)

    @property
    def torque_converter_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6981.TorqueConverterConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6981,
        )

        return self.__parent__._cast(
            _6981.TorqueConverterConnectionCriticalSpeedAnalysis
        )

    @property
    def worm_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6988.WormGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6988,
        )

        return self.__parent__._cast(_6988.WormGearMeshCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6991.ZerolBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6991,
        )

        return self.__parent__._cast(_6991.ZerolBevelGearMeshCriticalSpeedAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7127.AbstractShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7127,
        )

        return self.__parent__._cast(
            _7127.AbstractShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7133.AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7133,
        )

        return self.__parent__._cast(
            _7133.AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def belt_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7138.BeltConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7138,
        )

        return self.__parent__._cast(
            _7138.BeltConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7141.BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7141,
        )

        return self.__parent__._cast(
            _7141.BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7146.BevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7146,
        )

        return self.__parent__._cast(
            _7146.BevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def clutch_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7151.ClutchConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7151,
        )

        return self.__parent__._cast(
            _7151.ClutchConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coaxial_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7153.CoaxialConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7153,
        )

        return self.__parent__._cast(
            _7153.CoaxialConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7156.ConceptCouplingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7156,
        )

        return self.__parent__._cast(
            _7156.ConceptCouplingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7159.ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7159,
        )

        return self.__parent__._cast(
            _7159.ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7162.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7162,
        )

        return self.__parent__._cast(
            _7162.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7164.ConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7164,
        )

        return self.__parent__._cast(
            _7164.ConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7167.CouplingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7167,
        )

        return self.__parent__._cast(
            _7167.CouplingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cvt_belt_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7170.CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7170,
        )

        return self.__parent__._cast(
            _7170.CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_central_bearing_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7174.CycloidalDiscCentralBearingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7174,
        )

        return self.__parent__._cast(
            _7174.CycloidalDiscCentralBearingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7175.CycloidalDiscPlanetaryBearingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7175,
        )

        return self.__parent__._cast(
            _7175.CycloidalDiscPlanetaryBearingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7177.CylindricalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7177,
        )

        return self.__parent__._cast(
            _7177.CylindricalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7183.FaceGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7183,
        )

        return self.__parent__._cast(
            _7183.FaceGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7188.GearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7188,
        )

        return self.__parent__._cast(
            _7188.GearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7193.HypoidGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7193,
        )

        return self.__parent__._cast(
            _7193.HypoidGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def inter_mountable_component_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7195.InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7195,
        )

        return self.__parent__._cast(
            _7195.InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7197.KlingelnbergCycloPalloidConicalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7197,
        )

        return self.__parent__._cast(
            _7197.KlingelnbergCycloPalloidConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7200.KlingelnbergCycloPalloidHypoidGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7200,
        )

        return self.__parent__._cast(
            _7200.KlingelnbergCycloPalloidHypoidGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7203.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7203,
        )

        return self.__parent__._cast(
            _7203.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7213.PartToPartShearCouplingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7213,
        )

        return self.__parent__._cast(
            _7213.PartToPartShearCouplingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planetary_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7215.PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7215,
        )

        return self.__parent__._cast(
            _7215.PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def ring_pins_to_disc_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7222.RingPinsToDiscConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7222,
        )

        return self.__parent__._cast(
            _7222.RingPinsToDiscConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7225.RollingRingConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7225,
        )

        return self.__parent__._cast(
            _7225.RollingRingConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_to_mountable_component_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7229.ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7229,
        )

        return self.__parent__._cast(
            _7229.ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7232.SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7232,
        )

        return self.__parent__._cast(
            _7232.SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7235.SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7235,
        )

        return self.__parent__._cast(
            _7235.SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7238.StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7238,
        )

        return self.__parent__._cast(
            _7238.StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7241.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7241,
        )

        return self.__parent__._cast(
            _7241.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7250.TorqueConverterConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7250,
        )

        return self.__parent__._cast(
            _7250.TorqueConverterConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7256.WormGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7256,
        )

        return self.__parent__._cast(
            _7256.WormGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7259.ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7259,
        )

        return self.__parent__._cast(
            _7259.ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_shaft_to_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7395.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7395,
        )

        return self.__parent__._cast(
            _7395.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7400.AGMAGleasonConicalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7400,
        )

        return self.__parent__._cast(
            _7400.AGMAGleasonConicalGearMeshAdvancedSystemDeflection
        )

    @property
    def belt_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7404.BeltConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7404,
        )

        return self.__parent__._cast(_7404.BeltConnectionAdvancedSystemDeflection)

    @property
    def bevel_differential_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7407.BevelDifferentialGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7407,
        )

        return self.__parent__._cast(
            _7407.BevelDifferentialGearMeshAdvancedSystemDeflection
        )

    @property
    def bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7412.BevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7412,
        )

        return self.__parent__._cast(_7412.BevelGearMeshAdvancedSystemDeflection)

    @property
    def clutch_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7417.ClutchConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7417,
        )

        return self.__parent__._cast(_7417.ClutchConnectionAdvancedSystemDeflection)

    @property
    def coaxial_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7419.CoaxialConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7419,
        )

        return self.__parent__._cast(_7419.CoaxialConnectionAdvancedSystemDeflection)

    @property
    def concept_coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7422.ConceptCouplingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7422,
        )

        return self.__parent__._cast(
            _7422.ConceptCouplingConnectionAdvancedSystemDeflection
        )

    @property
    def concept_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7425.ConceptGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7425,
        )

        return self.__parent__._cast(_7425.ConceptGearMeshAdvancedSystemDeflection)

    @property
    def conical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7428.ConicalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7428,
        )

        return self.__parent__._cast(_7428.ConicalGearMeshAdvancedSystemDeflection)

    @property
    def connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7430.ConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7430,
        )

        return self.__parent__._cast(_7430.ConnectionAdvancedSystemDeflection)

    @property
    def coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7434.CouplingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7434,
        )

        return self.__parent__._cast(_7434.CouplingConnectionAdvancedSystemDeflection)

    @property
    def cvt_belt_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7437.CVTBeltConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7437,
        )

        return self.__parent__._cast(_7437.CVTBeltConnectionAdvancedSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7441.CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7441,
        )

        return self.__parent__._cast(
            _7441.CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7442.CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7442,
        )

        return self.__parent__._cast(
            _7442.CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection
        )

    @property
    def cylindrical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7444.CylindricalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7444,
        )

        return self.__parent__._cast(_7444.CylindricalGearMeshAdvancedSystemDeflection)

    @property
    def face_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7451.FaceGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7451,
        )

        return self.__parent__._cast(_7451.FaceGearMeshAdvancedSystemDeflection)

    @property
    def gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7456.GearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7456,
        )

        return self.__parent__._cast(_7456.GearMeshAdvancedSystemDeflection)

    @property
    def hypoid_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7460.HypoidGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7460,
        )

        return self.__parent__._cast(_7460.HypoidGearMeshAdvancedSystemDeflection)

    @property
    def inter_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7462.InterMountableComponentConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7462,
        )

        return self.__parent__._cast(
            _7462.InterMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7464.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7464,
        )

        return self.__parent__._cast(
            _7464.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7467.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7467,
        )

        return self.__parent__._cast(
            _7467.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7470.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7470,
        )

        return self.__parent__._cast(
            _7470.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7481.PartToPartShearCouplingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7481,
        )

        return self.__parent__._cast(
            _7481.PartToPartShearCouplingConnectionAdvancedSystemDeflection
        )

    @property
    def planetary_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7483.PlanetaryConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7483,
        )

        return self.__parent__._cast(_7483.PlanetaryConnectionAdvancedSystemDeflection)

    @property
    def ring_pins_to_disc_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7490.RingPinsToDiscConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7490,
        )

        return self.__parent__._cast(
            _7490.RingPinsToDiscConnectionAdvancedSystemDeflection
        )

    @property
    def rolling_ring_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7493.RollingRingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7493,
        )

        return self.__parent__._cast(
            _7493.RollingRingConnectionAdvancedSystemDeflection
        )

    @property
    def shaft_to_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7497.ShaftToMountableComponentConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7497,
        )

        return self.__parent__._cast(
            _7497.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7500.SpiralBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7500,
        )

        return self.__parent__._cast(_7500.SpiralBevelGearMeshAdvancedSystemDeflection)

    @property
    def spring_damper_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7503.SpringDamperConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7503,
        )

        return self.__parent__._cast(
            _7503.SpringDamperConnectionAdvancedSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7506.StraightBevelDiffGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7506,
        )

        return self.__parent__._cast(
            _7506.StraightBevelDiffGearMeshAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7509.StraightBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7509,
        )

        return self.__parent__._cast(
            _7509.StraightBevelGearMeshAdvancedSystemDeflection
        )

    @property
    def torque_converter_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7518.TorqueConverterConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7518,
        )

        return self.__parent__._cast(
            _7518.TorqueConverterConnectionAdvancedSystemDeflection
        )

    @property
    def worm_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7525.WormGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7525,
        )

        return self.__parent__._cast(_7525.WormGearMeshAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7528.ZerolBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7528,
        )

        return self.__parent__._cast(_7528.ZerolBevelGearMeshAdvancedSystemDeflection)

    @property
    def abstract_shaft_to_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7678.AbstractShaftToMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7678,
        )

        return self.__parent__._cast(
            _7678.AbstractShaftToMountableComponentConnectionLoadCase
        )

    @property
    def agma_gleason_conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7683.AGMAGleasonConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7683,
        )

        return self.__parent__._cast(_7683.AGMAGleasonConicalGearMeshLoadCase)

    @property
    def belt_connection_load_case(self: "CastSelf") -> "_7689.BeltConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7689,
        )

        return self.__parent__._cast(_7689.BeltConnectionLoadCase)

    @property
    def bevel_differential_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7692.BevelDifferentialGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7692,
        )

        return self.__parent__._cast(_7692.BevelDifferentialGearMeshLoadCase)

    @property
    def bevel_gear_mesh_load_case(self: "CastSelf") -> "_7697.BevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7697,
        )

        return self.__parent__._cast(_7697.BevelGearMeshLoadCase)

    @property
    def clutch_connection_load_case(
        self: "CastSelf",
    ) -> "_7701.ClutchConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7701,
        )

        return self.__parent__._cast(_7701.ClutchConnectionLoadCase)

    @property
    def coaxial_connection_load_case(
        self: "CastSelf",
    ) -> "_7705.CoaxialConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7705,
        )

        return self.__parent__._cast(_7705.CoaxialConnectionLoadCase)

    @property
    def concept_coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_7707.ConceptCouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7707,
        )

        return self.__parent__._cast(_7707.ConceptCouplingConnectionLoadCase)

    @property
    def concept_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7711.ConceptGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7711,
        )

        return self.__parent__._cast(_7711.ConceptGearMeshLoadCase)

    @property
    def conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7715.ConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7715,
        )

        return self.__parent__._cast(_7715.ConicalGearMeshLoadCase)

    @property
    def connection_load_case(self: "CastSelf") -> "_7718.ConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7718,
        )

        return self.__parent__._cast(_7718.ConnectionLoadCase)

    @property
    def coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_7720.CouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7720,
        )

        return self.__parent__._cast(_7720.CouplingConnectionLoadCase)

    @property
    def cvt_belt_connection_load_case(
        self: "CastSelf",
    ) -> "_7723.CVTBeltConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7723,
        )

        return self.__parent__._cast(_7723.CVTBeltConnectionLoadCase)

    @property
    def cycloidal_disc_central_bearing_connection_load_case(
        self: "CastSelf",
    ) -> "_7727.CycloidalDiscCentralBearingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7727,
        )

        return self.__parent__._cast(
            _7727.CycloidalDiscCentralBearingConnectionLoadCase
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_load_case(
        self: "CastSelf",
    ) -> "_7729.CycloidalDiscPlanetaryBearingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7729,
        )

        return self.__parent__._cast(
            _7729.CycloidalDiscPlanetaryBearingConnectionLoadCase
        )

    @property
    def cylindrical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7732.CylindricalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7732,
        )

        return self.__parent__._cast(_7732.CylindricalGearMeshLoadCase)

    @property
    def face_gear_mesh_load_case(self: "CastSelf") -> "_7754.FaceGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7754,
        )

        return self.__parent__._cast(_7754.FaceGearMeshLoadCase)

    @property
    def gear_mesh_load_case(self: "CastSelf") -> "_7761.GearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7761,
        )

        return self.__parent__._cast(_7761.GearMeshLoadCase)

    @property
    def hypoid_gear_mesh_load_case(self: "CastSelf") -> "_7775.HypoidGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7775,
        )

        return self.__parent__._cast(_7775.HypoidGearMeshLoadCase)

    @property
    def inter_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7780.InterMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7780,
        )

        return self.__parent__._cast(_7780.InterMountableComponentConnectionLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7782.KlingelnbergCycloPalloidConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7782,
        )

        return self.__parent__._cast(
            _7782.KlingelnbergCycloPalloidConicalGearMeshLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7785.KlingelnbergCycloPalloidHypoidGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7785,
        )

        return self.__parent__._cast(
            _7785.KlingelnbergCycloPalloidHypoidGearMeshLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7788.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7788,
        )

        return self.__parent__._cast(
            _7788.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
        )

    @property
    def part_to_part_shear_coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_7800.PartToPartShearCouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7800,
        )

        return self.__parent__._cast(_7800.PartToPartShearCouplingConnectionLoadCase)

    @property
    def planetary_connection_load_case(
        self: "CastSelf",
    ) -> "_7803.PlanetaryConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7803,
        )

        return self.__parent__._cast(_7803.PlanetaryConnectionLoadCase)

    @property
    def ring_pins_to_disc_connection_load_case(
        self: "CastSelf",
    ) -> "_7815.RingPinsToDiscConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7815,
        )

        return self.__parent__._cast(_7815.RingPinsToDiscConnectionLoadCase)

    @property
    def rolling_ring_connection_load_case(
        self: "CastSelf",
    ) -> "_7817.RollingRingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7817,
        )

        return self.__parent__._cast(_7817.RollingRingConnectionLoadCase)

    @property
    def shaft_to_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7822.ShaftToMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7822,
        )

        return self.__parent__._cast(_7822.ShaftToMountableComponentConnectionLoadCase)

    @property
    def spiral_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7825.SpiralBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7825,
        )

        return self.__parent__._cast(_7825.SpiralBevelGearMeshLoadCase)

    @property
    def spring_damper_connection_load_case(
        self: "CastSelf",
    ) -> "_7827.SpringDamperConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7827,
        )

        return self.__parent__._cast(_7827.SpringDamperConnectionLoadCase)

    @property
    def straight_bevel_diff_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7831.StraightBevelDiffGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7831,
        )

        return self.__parent__._cast(_7831.StraightBevelDiffGearMeshLoadCase)

    @property
    def straight_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7834.StraightBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7834,
        )

        return self.__parent__._cast(_7834.StraightBevelGearMeshLoadCase)

    @property
    def torque_converter_connection_load_case(
        self: "CastSelf",
    ) -> "_7844.TorqueConverterConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7844,
        )

        return self.__parent__._cast(_7844.TorqueConverterConnectionLoadCase)

    @property
    def worm_gear_mesh_load_case(self: "CastSelf") -> "_7855.WormGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7855,
        )

        return self.__parent__._cast(_7855.WormGearMeshLoadCase)

    @property
    def zerol_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7858.ZerolBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7858,
        )

        return self.__parent__._cast(_7858.ZerolBevelGearMeshLoadCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7880.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.ConnectionAnalysisCase)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7882.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7882,
        )

        return self.__parent__._cast(_7882.ConnectionFEAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7883.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7883,
        )

        return self.__parent__._cast(_7883.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7884.ConnectionTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7884,
        )

        return self.__parent__._cast(_7884.ConnectionTimeSeriesLoadAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "ConnectionAnalysis":
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
class ConnectionAnalysis(_2894.DesignEntitySingleContextAnalysis):
    """ConnectionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def short_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShortName")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionAnalysis
        """
        return _Cast_ConnectionAnalysis(self)
