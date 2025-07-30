"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4020 import (
        AbstractAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4021 import (
        AbstractShaftOrHousingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4022 import (
        AbstractShaftStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4023 import (
        AbstractShaftToMountableComponentConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4024 import (
        AGMAGleasonConicalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4025 import (
        AGMAGleasonConicalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4026 import (
        AGMAGleasonConicalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4027 import (
        AssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4028 import (
        BearingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4029 import (
        BeltConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4030 import (
        BeltDriveStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4031 import (
        BevelDifferentialGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4032 import (
        BevelDifferentialGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4033 import (
        BevelDifferentialGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4034 import (
        BevelDifferentialPlanetGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4035 import (
        BevelDifferentialSunGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4036 import (
        BevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4037 import (
        BevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4038 import (
        BevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4039 import (
        BoltedJointStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4040 import (
        BoltStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4041 import (
        ClutchConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4042 import (
        ClutchHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4043 import (
        ClutchStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4044 import (
        CoaxialConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4045 import (
        ComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4046 import (
        ConceptCouplingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4047 import (
        ConceptCouplingHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4048 import (
        ConceptCouplingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4049 import (
        ConceptGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4050 import (
        ConceptGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4051 import (
        ConceptGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4052 import (
        ConicalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4053 import (
        ConicalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4054 import (
        ConicalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4055 import (
        ConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4056 import (
        ConnectorStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4057 import (
        CouplingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4058 import (
        CouplingHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4059 import (
        CouplingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4060 import (
        CriticalSpeed,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4061 import (
        CVTBeltConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4062 import (
        CVTPulleyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4063 import (
        CVTStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4064 import (
        CycloidalAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4065 import (
        CycloidalDiscCentralBearingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4066 import (
        CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4067 import (
        CycloidalDiscStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4068 import (
        CylindricalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4069 import (
        CylindricalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4070 import (
        CylindricalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4071 import (
        CylindricalPlanetGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4072 import (
        DatumStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4073 import (
        DynamicModelForStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4074 import (
        ExternalCADModelStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4075 import (
        FaceGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4076 import (
        FaceGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4077 import (
        FaceGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4078 import (
        FEPartStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4079 import (
        FlexiblePinAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4080 import (
        GearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4081 import (
        GearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4082 import (
        GearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4083 import (
        GuideDxfModelStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4084 import (
        HypoidGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4085 import (
        HypoidGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4086 import (
        HypoidGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4087 import (
        InterMountableComponentConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4088 import (
        KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4089 import (
        KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4090 import (
        KlingelnbergCycloPalloidConicalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4091 import (
        KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4092 import (
        KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4093 import (
        KlingelnbergCycloPalloidHypoidGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4094 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4095 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4096 import (
        KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4097 import (
        MassDiscStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4098 import (
        MeasurementComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4099 import (
        MicrophoneArrayStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4100 import (
        MicrophoneStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4101 import (
        MountableComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4102 import (
        OilSealStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4103 import (
        PartStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4104 import (
        PartToPartShearCouplingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4105 import (
        PartToPartShearCouplingHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4106 import (
        PartToPartShearCouplingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4107 import (
        PlanetaryConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4108 import (
        PlanetaryGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4109 import (
        PlanetCarrierStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4110 import (
        PointLoadStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4111 import (
        PowerLoadStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4112 import (
        PulleyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4113 import (
        RingPinsStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4114 import (
        RingPinsToDiscConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4115 import (
        RollingRingAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4116 import (
        RollingRingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4117 import (
        RollingRingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4118 import (
        RootAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4119 import (
        ShaftHubConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4120 import (
        ShaftStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4121 import (
        ShaftToMountableComponentConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4122 import (
        SpecialisedAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4123 import (
        SpiralBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4124 import (
        SpiralBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4125 import (
        SpiralBevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4126 import (
        SpringDamperConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4127 import (
        SpringDamperHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4128 import (
        SpringDamperStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4129 import (
        StabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4130 import (
        StabilityAnalysisDrawStyle,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4131 import (
        StabilityAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4132 import (
        StraightBevelDiffGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4133 import (
        StraightBevelDiffGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4134 import (
        StraightBevelDiffGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4135 import (
        StraightBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4136 import (
        StraightBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4137 import (
        StraightBevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4138 import (
        StraightBevelPlanetGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4139 import (
        StraightBevelSunGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4140 import (
        SynchroniserHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4141 import (
        SynchroniserPartStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4142 import (
        SynchroniserSleeveStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4143 import (
        SynchroniserStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4144 import (
        TorqueConverterConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4145 import (
        TorqueConverterPumpStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4146 import (
        TorqueConverterStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4147 import (
        TorqueConverterTurbineStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4148 import (
        UnbalancedMassStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4149 import (
        VirtualComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4150 import (
        WormGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4151 import (
        WormGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4152 import (
        WormGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4153 import (
        ZerolBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4154 import (
        ZerolBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4155 import (
        ZerolBevelGearStabilityAnalysis,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.stability_analyses._4020": [
            "AbstractAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4021": [
            "AbstractShaftOrHousingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4022": [
            "AbstractShaftStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4023": [
            "AbstractShaftToMountableComponentConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4024": [
            "AGMAGleasonConicalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4025": [
            "AGMAGleasonConicalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4026": [
            "AGMAGleasonConicalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4027": [
            "AssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4028": [
            "BearingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4029": [
            "BeltConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4030": [
            "BeltDriveStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4031": [
            "BevelDifferentialGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4032": [
            "BevelDifferentialGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4033": [
            "BevelDifferentialGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4034": [
            "BevelDifferentialPlanetGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4035": [
            "BevelDifferentialSunGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4036": [
            "BevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4037": [
            "BevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4038": [
            "BevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4039": [
            "BoltedJointStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4040": [
            "BoltStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4041": [
            "ClutchConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4042": [
            "ClutchHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4043": [
            "ClutchStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4044": [
            "CoaxialConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4045": [
            "ComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4046": [
            "ConceptCouplingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4047": [
            "ConceptCouplingHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4048": [
            "ConceptCouplingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4049": [
            "ConceptGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4050": [
            "ConceptGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4051": [
            "ConceptGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4052": [
            "ConicalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4053": [
            "ConicalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4054": [
            "ConicalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4055": [
            "ConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4056": [
            "ConnectorStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4057": [
            "CouplingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4058": [
            "CouplingHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4059": [
            "CouplingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4060": [
            "CriticalSpeed"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4061": [
            "CVTBeltConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4062": [
            "CVTPulleyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4063": [
            "CVTStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4064": [
            "CycloidalAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4065": [
            "CycloidalDiscCentralBearingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4066": [
            "CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4067": [
            "CycloidalDiscStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4068": [
            "CylindricalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4069": [
            "CylindricalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4070": [
            "CylindricalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4071": [
            "CylindricalPlanetGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4072": [
            "DatumStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4073": [
            "DynamicModelForStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4074": [
            "ExternalCADModelStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4075": [
            "FaceGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4076": [
            "FaceGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4077": [
            "FaceGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4078": [
            "FEPartStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4079": [
            "FlexiblePinAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4080": [
            "GearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4081": [
            "GearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4082": [
            "GearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4083": [
            "GuideDxfModelStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4084": [
            "HypoidGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4085": [
            "HypoidGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4086": [
            "HypoidGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4087": [
            "InterMountableComponentConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4088": [
            "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4089": [
            "KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4090": [
            "KlingelnbergCycloPalloidConicalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4091": [
            "KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4092": [
            "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4093": [
            "KlingelnbergCycloPalloidHypoidGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4094": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4095": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4096": [
            "KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4097": [
            "MassDiscStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4098": [
            "MeasurementComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4099": [
            "MicrophoneArrayStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4100": [
            "MicrophoneStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4101": [
            "MountableComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4102": [
            "OilSealStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4103": [
            "PartStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4104": [
            "PartToPartShearCouplingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4105": [
            "PartToPartShearCouplingHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4106": [
            "PartToPartShearCouplingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4107": [
            "PlanetaryConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4108": [
            "PlanetaryGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4109": [
            "PlanetCarrierStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4110": [
            "PointLoadStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4111": [
            "PowerLoadStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4112": [
            "PulleyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4113": [
            "RingPinsStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4114": [
            "RingPinsToDiscConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4115": [
            "RollingRingAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4116": [
            "RollingRingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4117": [
            "RollingRingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4118": [
            "RootAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4119": [
            "ShaftHubConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4120": [
            "ShaftStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4121": [
            "ShaftToMountableComponentConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4122": [
            "SpecialisedAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4123": [
            "SpiralBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4124": [
            "SpiralBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4125": [
            "SpiralBevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4126": [
            "SpringDamperConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4127": [
            "SpringDamperHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4128": [
            "SpringDamperStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4129": [
            "StabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4130": [
            "StabilityAnalysisDrawStyle"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4131": [
            "StabilityAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4132": [
            "StraightBevelDiffGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4133": [
            "StraightBevelDiffGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4134": [
            "StraightBevelDiffGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4135": [
            "StraightBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4136": [
            "StraightBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4137": [
            "StraightBevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4138": [
            "StraightBevelPlanetGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4139": [
            "StraightBevelSunGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4140": [
            "SynchroniserHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4141": [
            "SynchroniserPartStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4142": [
            "SynchroniserSleeveStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4143": [
            "SynchroniserStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4144": [
            "TorqueConverterConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4145": [
            "TorqueConverterPumpStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4146": [
            "TorqueConverterStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4147": [
            "TorqueConverterTurbineStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4148": [
            "UnbalancedMassStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4149": [
            "VirtualComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4150": [
            "WormGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4151": [
            "WormGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4152": [
            "WormGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4153": [
            "ZerolBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4154": [
            "ZerolBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4155": [
            "ZerolBevelGearStabilityAnalysis"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractAssemblyStabilityAnalysis",
    "AbstractShaftOrHousingStabilityAnalysis",
    "AbstractShaftStabilityAnalysis",
    "AbstractShaftToMountableComponentConnectionStabilityAnalysis",
    "AGMAGleasonConicalGearMeshStabilityAnalysis",
    "AGMAGleasonConicalGearSetStabilityAnalysis",
    "AGMAGleasonConicalGearStabilityAnalysis",
    "AssemblyStabilityAnalysis",
    "BearingStabilityAnalysis",
    "BeltConnectionStabilityAnalysis",
    "BeltDriveStabilityAnalysis",
    "BevelDifferentialGearMeshStabilityAnalysis",
    "BevelDifferentialGearSetStabilityAnalysis",
    "BevelDifferentialGearStabilityAnalysis",
    "BevelDifferentialPlanetGearStabilityAnalysis",
    "BevelDifferentialSunGearStabilityAnalysis",
    "BevelGearMeshStabilityAnalysis",
    "BevelGearSetStabilityAnalysis",
    "BevelGearStabilityAnalysis",
    "BoltedJointStabilityAnalysis",
    "BoltStabilityAnalysis",
    "ClutchConnectionStabilityAnalysis",
    "ClutchHalfStabilityAnalysis",
    "ClutchStabilityAnalysis",
    "CoaxialConnectionStabilityAnalysis",
    "ComponentStabilityAnalysis",
    "ConceptCouplingConnectionStabilityAnalysis",
    "ConceptCouplingHalfStabilityAnalysis",
    "ConceptCouplingStabilityAnalysis",
    "ConceptGearMeshStabilityAnalysis",
    "ConceptGearSetStabilityAnalysis",
    "ConceptGearStabilityAnalysis",
    "ConicalGearMeshStabilityAnalysis",
    "ConicalGearSetStabilityAnalysis",
    "ConicalGearStabilityAnalysis",
    "ConnectionStabilityAnalysis",
    "ConnectorStabilityAnalysis",
    "CouplingConnectionStabilityAnalysis",
    "CouplingHalfStabilityAnalysis",
    "CouplingStabilityAnalysis",
    "CriticalSpeed",
    "CVTBeltConnectionStabilityAnalysis",
    "CVTPulleyStabilityAnalysis",
    "CVTStabilityAnalysis",
    "CycloidalAssemblyStabilityAnalysis",
    "CycloidalDiscCentralBearingConnectionStabilityAnalysis",
    "CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis",
    "CycloidalDiscStabilityAnalysis",
    "CylindricalGearMeshStabilityAnalysis",
    "CylindricalGearSetStabilityAnalysis",
    "CylindricalGearStabilityAnalysis",
    "CylindricalPlanetGearStabilityAnalysis",
    "DatumStabilityAnalysis",
    "DynamicModelForStabilityAnalysis",
    "ExternalCADModelStabilityAnalysis",
    "FaceGearMeshStabilityAnalysis",
    "FaceGearSetStabilityAnalysis",
    "FaceGearStabilityAnalysis",
    "FEPartStabilityAnalysis",
    "FlexiblePinAssemblyStabilityAnalysis",
    "GearMeshStabilityAnalysis",
    "GearSetStabilityAnalysis",
    "GearStabilityAnalysis",
    "GuideDxfModelStabilityAnalysis",
    "HypoidGearMeshStabilityAnalysis",
    "HypoidGearSetStabilityAnalysis",
    "HypoidGearStabilityAnalysis",
    "InterMountableComponentConnectionStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis",
    "MassDiscStabilityAnalysis",
    "MeasurementComponentStabilityAnalysis",
    "MicrophoneArrayStabilityAnalysis",
    "MicrophoneStabilityAnalysis",
    "MountableComponentStabilityAnalysis",
    "OilSealStabilityAnalysis",
    "PartStabilityAnalysis",
    "PartToPartShearCouplingConnectionStabilityAnalysis",
    "PartToPartShearCouplingHalfStabilityAnalysis",
    "PartToPartShearCouplingStabilityAnalysis",
    "PlanetaryConnectionStabilityAnalysis",
    "PlanetaryGearSetStabilityAnalysis",
    "PlanetCarrierStabilityAnalysis",
    "PointLoadStabilityAnalysis",
    "PowerLoadStabilityAnalysis",
    "PulleyStabilityAnalysis",
    "RingPinsStabilityAnalysis",
    "RingPinsToDiscConnectionStabilityAnalysis",
    "RollingRingAssemblyStabilityAnalysis",
    "RollingRingConnectionStabilityAnalysis",
    "RollingRingStabilityAnalysis",
    "RootAssemblyStabilityAnalysis",
    "ShaftHubConnectionStabilityAnalysis",
    "ShaftStabilityAnalysis",
    "ShaftToMountableComponentConnectionStabilityAnalysis",
    "SpecialisedAssemblyStabilityAnalysis",
    "SpiralBevelGearMeshStabilityAnalysis",
    "SpiralBevelGearSetStabilityAnalysis",
    "SpiralBevelGearStabilityAnalysis",
    "SpringDamperConnectionStabilityAnalysis",
    "SpringDamperHalfStabilityAnalysis",
    "SpringDamperStabilityAnalysis",
    "StabilityAnalysis",
    "StabilityAnalysisDrawStyle",
    "StabilityAnalysisOptions",
    "StraightBevelDiffGearMeshStabilityAnalysis",
    "StraightBevelDiffGearSetStabilityAnalysis",
    "StraightBevelDiffGearStabilityAnalysis",
    "StraightBevelGearMeshStabilityAnalysis",
    "StraightBevelGearSetStabilityAnalysis",
    "StraightBevelGearStabilityAnalysis",
    "StraightBevelPlanetGearStabilityAnalysis",
    "StraightBevelSunGearStabilityAnalysis",
    "SynchroniserHalfStabilityAnalysis",
    "SynchroniserPartStabilityAnalysis",
    "SynchroniserSleeveStabilityAnalysis",
    "SynchroniserStabilityAnalysis",
    "TorqueConverterConnectionStabilityAnalysis",
    "TorqueConverterPumpStabilityAnalysis",
    "TorqueConverterStabilityAnalysis",
    "TorqueConverterTurbineStabilityAnalysis",
    "UnbalancedMassStabilityAnalysis",
    "VirtualComponentStabilityAnalysis",
    "WormGearMeshStabilityAnalysis",
    "WormGearSetStabilityAnalysis",
    "WormGearStabilityAnalysis",
    "ZerolBevelGearMeshStabilityAnalysis",
    "ZerolBevelGearSetStabilityAnalysis",
    "ZerolBevelGearStabilityAnalysis",
)
