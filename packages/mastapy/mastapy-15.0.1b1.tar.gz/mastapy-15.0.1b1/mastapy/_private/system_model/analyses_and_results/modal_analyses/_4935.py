"""PartModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7890

_PART_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses", "PartModalAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7887
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4842,
        _4843,
        _4844,
        _4847,
        _4848,
        _4849,
        _4850,
        _4852,
        _4854,
        _4855,
        _4856,
        _4857,
        _4859,
        _4860,
        _4861,
        _4862,
        _4864,
        _4865,
        _4867,
        _4869,
        _4870,
        _4872,
        _4873,
        _4875,
        _4876,
        _4878,
        _4881,
        _4882,
        _4884,
        _4885,
        _4886,
        _4888,
        _4891,
        _4892,
        _4893,
        _4894,
        _4898,
        _4900,
        _4901,
        _4902,
        _4903,
        _4906,
        _4907,
        _4908,
        _4910,
        _4911,
        _4914,
        _4915,
        _4917,
        _4918,
        _4920,
        _4921,
        _4922,
        _4923,
        _4924,
        _4925,
        _4926,
        _4931,
        _4933,
        _4937,
        _4938,
        _4940,
        _4941,
        _4942,
        _4943,
        _4944,
        _4945,
        _4947,
        _4949,
        _4950,
        _4951,
        _4952,
        _4955,
        _4957,
        _4958,
        _4960,
        _4961,
        _4963,
        _4964,
        _4966,
        _4967,
        _4968,
        _4969,
        _4970,
        _4971,
        _4972,
        _4973,
        _4975,
        _4976,
        _4977,
        _4978,
        _4979,
        _4984,
        _4985,
        _4987,
        _4988,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4997,
        _4999,
        _5000,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3028,
    )
    from mastapy._private.system_model.drawing import _2472
    from mastapy._private.system_model.part_model import _2698

    Self = TypeVar("Self", bound="PartModalAnalysis")
    CastSelf = TypeVar("CastSelf", bound="PartModalAnalysis._Cast_PartModalAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("PartModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartModalAnalysis:
    """Special nested class for casting PartModalAnalysis to subclasses."""

    __parent__: "PartModalAnalysis"

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
    def abstract_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4842.AbstractAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4842,
        )

        return self.__parent__._cast(_4842.AbstractAssemblyModalAnalysis)

    @property
    def abstract_shaft_modal_analysis(
        self: "CastSelf",
    ) -> "_4843.AbstractShaftModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4843,
        )

        return self.__parent__._cast(_4843.AbstractShaftModalAnalysis)

    @property
    def abstract_shaft_or_housing_modal_analysis(
        self: "CastSelf",
    ) -> "_4844.AbstractShaftOrHousingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4844,
        )

        return self.__parent__._cast(_4844.AbstractShaftOrHousingModalAnalysis)

    @property
    def agma_gleason_conical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4847.AGMAGleasonConicalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4847,
        )

        return self.__parent__._cast(_4847.AGMAGleasonConicalGearModalAnalysis)

    @property
    def agma_gleason_conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4848.AGMAGleasonConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4848,
        )

        return self.__parent__._cast(_4848.AGMAGleasonConicalGearSetModalAnalysis)

    @property
    def assembly_modal_analysis(self: "CastSelf") -> "_4849.AssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4849,
        )

        return self.__parent__._cast(_4849.AssemblyModalAnalysis)

    @property
    def bearing_modal_analysis(self: "CastSelf") -> "_4850.BearingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4850,
        )

        return self.__parent__._cast(_4850.BearingModalAnalysis)

    @property
    def belt_drive_modal_analysis(self: "CastSelf") -> "_4852.BeltDriveModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4852,
        )

        return self.__parent__._cast(_4852.BeltDriveModalAnalysis)

    @property
    def bevel_differential_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4854.BevelDifferentialGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4854,
        )

        return self.__parent__._cast(_4854.BevelDifferentialGearModalAnalysis)

    @property
    def bevel_differential_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4855.BevelDifferentialGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4855,
        )

        return self.__parent__._cast(_4855.BevelDifferentialGearSetModalAnalysis)

    @property
    def bevel_differential_planet_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4856.BevelDifferentialPlanetGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4856,
        )

        return self.__parent__._cast(_4856.BevelDifferentialPlanetGearModalAnalysis)

    @property
    def bevel_differential_sun_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4857.BevelDifferentialSunGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4857,
        )

        return self.__parent__._cast(_4857.BevelDifferentialSunGearModalAnalysis)

    @property
    def bevel_gear_modal_analysis(self: "CastSelf") -> "_4859.BevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4859,
        )

        return self.__parent__._cast(_4859.BevelGearModalAnalysis)

    @property
    def bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4860.BevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4860,
        )

        return self.__parent__._cast(_4860.BevelGearSetModalAnalysis)

    @property
    def bolted_joint_modal_analysis(
        self: "CastSelf",
    ) -> "_4861.BoltedJointModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4861,
        )

        return self.__parent__._cast(_4861.BoltedJointModalAnalysis)

    @property
    def bolt_modal_analysis(self: "CastSelf") -> "_4862.BoltModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4862,
        )

        return self.__parent__._cast(_4862.BoltModalAnalysis)

    @property
    def clutch_half_modal_analysis(self: "CastSelf") -> "_4864.ClutchHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4864,
        )

        return self.__parent__._cast(_4864.ClutchHalfModalAnalysis)

    @property
    def clutch_modal_analysis(self: "CastSelf") -> "_4865.ClutchModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4865,
        )

        return self.__parent__._cast(_4865.ClutchModalAnalysis)

    @property
    def component_modal_analysis(self: "CastSelf") -> "_4867.ComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4867,
        )

        return self.__parent__._cast(_4867.ComponentModalAnalysis)

    @property
    def concept_coupling_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4869.ConceptCouplingHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4869,
        )

        return self.__parent__._cast(_4869.ConceptCouplingHalfModalAnalysis)

    @property
    def concept_coupling_modal_analysis(
        self: "CastSelf",
    ) -> "_4870.ConceptCouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4870,
        )

        return self.__parent__._cast(_4870.ConceptCouplingModalAnalysis)

    @property
    def concept_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4872.ConceptGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4872,
        )

        return self.__parent__._cast(_4872.ConceptGearModalAnalysis)

    @property
    def concept_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4873.ConceptGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4873,
        )

        return self.__parent__._cast(_4873.ConceptGearSetModalAnalysis)

    @property
    def conical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4875.ConicalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4875,
        )

        return self.__parent__._cast(_4875.ConicalGearModalAnalysis)

    @property
    def conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4876.ConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4876,
        )

        return self.__parent__._cast(_4876.ConicalGearSetModalAnalysis)

    @property
    def connector_modal_analysis(self: "CastSelf") -> "_4878.ConnectorModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4878,
        )

        return self.__parent__._cast(_4878.ConnectorModalAnalysis)

    @property
    def coupling_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4881.CouplingHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4881,
        )

        return self.__parent__._cast(_4881.CouplingHalfModalAnalysis)

    @property
    def coupling_modal_analysis(self: "CastSelf") -> "_4882.CouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4882,
        )

        return self.__parent__._cast(_4882.CouplingModalAnalysis)

    @property
    def cvt_modal_analysis(self: "CastSelf") -> "_4884.CVTModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4884,
        )

        return self.__parent__._cast(_4884.CVTModalAnalysis)

    @property
    def cvt_pulley_modal_analysis(self: "CastSelf") -> "_4885.CVTPulleyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4885,
        )

        return self.__parent__._cast(_4885.CVTPulleyModalAnalysis)

    @property
    def cycloidal_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4886.CycloidalAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4886,
        )

        return self.__parent__._cast(_4886.CycloidalAssemblyModalAnalysis)

    @property
    def cycloidal_disc_modal_analysis(
        self: "CastSelf",
    ) -> "_4888.CycloidalDiscModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4888,
        )

        return self.__parent__._cast(_4888.CycloidalDiscModalAnalysis)

    @property
    def cylindrical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4891.CylindricalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4891,
        )

        return self.__parent__._cast(_4891.CylindricalGearModalAnalysis)

    @property
    def cylindrical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4892.CylindricalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4892,
        )

        return self.__parent__._cast(_4892.CylindricalGearSetModalAnalysis)

    @property
    def cylindrical_planet_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4893.CylindricalPlanetGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4893,
        )

        return self.__parent__._cast(_4893.CylindricalPlanetGearModalAnalysis)

    @property
    def datum_modal_analysis(self: "CastSelf") -> "_4894.DatumModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4894,
        )

        return self.__parent__._cast(_4894.DatumModalAnalysis)

    @property
    def external_cad_model_modal_analysis(
        self: "CastSelf",
    ) -> "_4898.ExternalCADModelModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4898,
        )

        return self.__parent__._cast(_4898.ExternalCADModelModalAnalysis)

    @property
    def face_gear_modal_analysis(self: "CastSelf") -> "_4900.FaceGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4900,
        )

        return self.__parent__._cast(_4900.FaceGearModalAnalysis)

    @property
    def face_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4901.FaceGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4901,
        )

        return self.__parent__._cast(_4901.FaceGearSetModalAnalysis)

    @property
    def fe_part_modal_analysis(self: "CastSelf") -> "_4902.FEPartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4902,
        )

        return self.__parent__._cast(_4902.FEPartModalAnalysis)

    @property
    def flexible_pin_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4903.FlexiblePinAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4903,
        )

        return self.__parent__._cast(_4903.FlexiblePinAssemblyModalAnalysis)

    @property
    def gear_modal_analysis(self: "CastSelf") -> "_4906.GearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4906,
        )

        return self.__parent__._cast(_4906.GearModalAnalysis)

    @property
    def gear_set_modal_analysis(self: "CastSelf") -> "_4907.GearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4907,
        )

        return self.__parent__._cast(_4907.GearSetModalAnalysis)

    @property
    def guide_dxf_model_modal_analysis(
        self: "CastSelf",
    ) -> "_4908.GuideDxfModelModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4908,
        )

        return self.__parent__._cast(_4908.GuideDxfModelModalAnalysis)

    @property
    def hypoid_gear_modal_analysis(self: "CastSelf") -> "_4910.HypoidGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4910,
        )

        return self.__parent__._cast(_4910.HypoidGearModalAnalysis)

    @property
    def hypoid_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4911.HypoidGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4911,
        )

        return self.__parent__._cast(_4911.HypoidGearSetModalAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4914.KlingelnbergCycloPalloidConicalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4914,
        )

        return self.__parent__._cast(
            _4914.KlingelnbergCycloPalloidConicalGearModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4915.KlingelnbergCycloPalloidConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4915,
        )

        return self.__parent__._cast(
            _4915.KlingelnbergCycloPalloidConicalGearSetModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4917.KlingelnbergCycloPalloidHypoidGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4917,
        )

        return self.__parent__._cast(
            _4917.KlingelnbergCycloPalloidHypoidGearModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4918.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4918,
        )

        return self.__parent__._cast(
            _4918.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4920.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4920,
        )

        return self.__parent__._cast(
            _4920.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4921.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4921,
        )

        return self.__parent__._cast(
            _4921.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis
        )

    @property
    def mass_disc_modal_analysis(self: "CastSelf") -> "_4922.MassDiscModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4922,
        )

        return self.__parent__._cast(_4922.MassDiscModalAnalysis)

    @property
    def measurement_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4923.MeasurementComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4923,
        )

        return self.__parent__._cast(_4923.MeasurementComponentModalAnalysis)

    @property
    def microphone_array_modal_analysis(
        self: "CastSelf",
    ) -> "_4924.MicrophoneArrayModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4924,
        )

        return self.__parent__._cast(_4924.MicrophoneArrayModalAnalysis)

    @property
    def microphone_modal_analysis(self: "CastSelf") -> "_4925.MicrophoneModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4925,
        )

        return self.__parent__._cast(_4925.MicrophoneModalAnalysis)

    @property
    def mountable_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4931.MountableComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4931,
        )

        return self.__parent__._cast(_4931.MountableComponentModalAnalysis)

    @property
    def oil_seal_modal_analysis(self: "CastSelf") -> "_4933.OilSealModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4933,
        )

        return self.__parent__._cast(_4933.OilSealModalAnalysis)

    @property
    def part_to_part_shear_coupling_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4937.PartToPartShearCouplingHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4937,
        )

        return self.__parent__._cast(_4937.PartToPartShearCouplingHalfModalAnalysis)

    @property
    def part_to_part_shear_coupling_modal_analysis(
        self: "CastSelf",
    ) -> "_4938.PartToPartShearCouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4938,
        )

        return self.__parent__._cast(_4938.PartToPartShearCouplingModalAnalysis)

    @property
    def planetary_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4940.PlanetaryGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4940,
        )

        return self.__parent__._cast(_4940.PlanetaryGearSetModalAnalysis)

    @property
    def planet_carrier_modal_analysis(
        self: "CastSelf",
    ) -> "_4941.PlanetCarrierModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4941,
        )

        return self.__parent__._cast(_4941.PlanetCarrierModalAnalysis)

    @property
    def point_load_modal_analysis(self: "CastSelf") -> "_4942.PointLoadModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4942,
        )

        return self.__parent__._cast(_4942.PointLoadModalAnalysis)

    @property
    def power_load_modal_analysis(self: "CastSelf") -> "_4943.PowerLoadModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4943,
        )

        return self.__parent__._cast(_4943.PowerLoadModalAnalysis)

    @property
    def pulley_modal_analysis(self: "CastSelf") -> "_4944.PulleyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4944,
        )

        return self.__parent__._cast(_4944.PulleyModalAnalysis)

    @property
    def ring_pins_modal_analysis(self: "CastSelf") -> "_4945.RingPinsModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4945,
        )

        return self.__parent__._cast(_4945.RingPinsModalAnalysis)

    @property
    def rolling_ring_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4947.RollingRingAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4947,
        )

        return self.__parent__._cast(_4947.RollingRingAssemblyModalAnalysis)

    @property
    def rolling_ring_modal_analysis(
        self: "CastSelf",
    ) -> "_4949.RollingRingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4949,
        )

        return self.__parent__._cast(_4949.RollingRingModalAnalysis)

    @property
    def root_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4950.RootAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4950,
        )

        return self.__parent__._cast(_4950.RootAssemblyModalAnalysis)

    @property
    def shaft_hub_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4951.ShaftHubConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4951,
        )

        return self.__parent__._cast(_4951.ShaftHubConnectionModalAnalysis)

    @property
    def shaft_modal_analysis(self: "CastSelf") -> "_4952.ShaftModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4952,
        )

        return self.__parent__._cast(_4952.ShaftModalAnalysis)

    @property
    def specialised_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4955.SpecialisedAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4955,
        )

        return self.__parent__._cast(_4955.SpecialisedAssemblyModalAnalysis)

    @property
    def spiral_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4957.SpiralBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4957,
        )

        return self.__parent__._cast(_4957.SpiralBevelGearModalAnalysis)

    @property
    def spiral_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4958.SpiralBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4958,
        )

        return self.__parent__._cast(_4958.SpiralBevelGearSetModalAnalysis)

    @property
    def spring_damper_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4960.SpringDamperHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4960,
        )

        return self.__parent__._cast(_4960.SpringDamperHalfModalAnalysis)

    @property
    def spring_damper_modal_analysis(
        self: "CastSelf",
    ) -> "_4961.SpringDamperModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4961,
        )

        return self.__parent__._cast(_4961.SpringDamperModalAnalysis)

    @property
    def straight_bevel_diff_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4963.StraightBevelDiffGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4963,
        )

        return self.__parent__._cast(_4963.StraightBevelDiffGearModalAnalysis)

    @property
    def straight_bevel_diff_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4964.StraightBevelDiffGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4964,
        )

        return self.__parent__._cast(_4964.StraightBevelDiffGearSetModalAnalysis)

    @property
    def straight_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4966.StraightBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4966,
        )

        return self.__parent__._cast(_4966.StraightBevelGearModalAnalysis)

    @property
    def straight_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4967.StraightBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4967,
        )

        return self.__parent__._cast(_4967.StraightBevelGearSetModalAnalysis)

    @property
    def straight_bevel_planet_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4968.StraightBevelPlanetGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4968,
        )

        return self.__parent__._cast(_4968.StraightBevelPlanetGearModalAnalysis)

    @property
    def straight_bevel_sun_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4969.StraightBevelSunGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4969,
        )

        return self.__parent__._cast(_4969.StraightBevelSunGearModalAnalysis)

    @property
    def synchroniser_half_modal_analysis(
        self: "CastSelf",
    ) -> "_4970.SynchroniserHalfModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4970,
        )

        return self.__parent__._cast(_4970.SynchroniserHalfModalAnalysis)

    @property
    def synchroniser_modal_analysis(
        self: "CastSelf",
    ) -> "_4971.SynchroniserModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4971,
        )

        return self.__parent__._cast(_4971.SynchroniserModalAnalysis)

    @property
    def synchroniser_part_modal_analysis(
        self: "CastSelf",
    ) -> "_4972.SynchroniserPartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4972,
        )

        return self.__parent__._cast(_4972.SynchroniserPartModalAnalysis)

    @property
    def synchroniser_sleeve_modal_analysis(
        self: "CastSelf",
    ) -> "_4973.SynchroniserSleeveModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4973,
        )

        return self.__parent__._cast(_4973.SynchroniserSleeveModalAnalysis)

    @property
    def torque_converter_modal_analysis(
        self: "CastSelf",
    ) -> "_4975.TorqueConverterModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4975,
        )

        return self.__parent__._cast(_4975.TorqueConverterModalAnalysis)

    @property
    def torque_converter_pump_modal_analysis(
        self: "CastSelf",
    ) -> "_4976.TorqueConverterPumpModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4976,
        )

        return self.__parent__._cast(_4976.TorqueConverterPumpModalAnalysis)

    @property
    def torque_converter_turbine_modal_analysis(
        self: "CastSelf",
    ) -> "_4977.TorqueConverterTurbineModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4977,
        )

        return self.__parent__._cast(_4977.TorqueConverterTurbineModalAnalysis)

    @property
    def unbalanced_mass_modal_analysis(
        self: "CastSelf",
    ) -> "_4978.UnbalancedMassModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4978,
        )

        return self.__parent__._cast(_4978.UnbalancedMassModalAnalysis)

    @property
    def virtual_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4979.VirtualComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4979,
        )

        return self.__parent__._cast(_4979.VirtualComponentModalAnalysis)

    @property
    def worm_gear_modal_analysis(self: "CastSelf") -> "_4984.WormGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4984,
        )

        return self.__parent__._cast(_4984.WormGearModalAnalysis)

    @property
    def worm_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4985.WormGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4985,
        )

        return self.__parent__._cast(_4985.WormGearSetModalAnalysis)

    @property
    def zerol_bevel_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4987.ZerolBevelGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4987,
        )

        return self.__parent__._cast(_4987.ZerolBevelGearModalAnalysis)

    @property
    def zerol_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4988.ZerolBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4988,
        )

        return self.__parent__._cast(_4988.ZerolBevelGearSetModalAnalysis)

    @property
    def part_modal_analysis(self: "CastSelf") -> "PartModalAnalysis":
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
class PartModalAnalysis(_7890.PartStaticLoadAnalysisCase):
    """PartModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_MODAL_ANALYSIS

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
    def modal_analysis(self: "Self") -> "_4926.ModalAnalysis":
        """mastapy.system_model.analyses_and_results.modal_analyses.ModalAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def excited_modes_summary(
        self: "Self",
    ) -> "List[_4999.SingleExcitationResultsModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.reporting.SingleExcitationResultsModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitedModesSummary")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_mesh_excitation_details(
        self: "Self",
    ) -> "List[_4997.RigidlyConnectedDesignEntityGroupModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.reporting.RigidlyConnectedDesignEntityGroupModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshExcitationDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def results_for_modes(self: "Self") -> "List[_5000.SingleModeResults]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.reporting.SingleModeResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForModes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shaft_excitation_details(
        self: "Self",
    ) -> "List[_4997.RigidlyConnectedDesignEntityGroupModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.reporting.RigidlyConnectedDesignEntityGroupModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftExcitationDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def system_deflection_results(self: "Self") -> "_3028.PartSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.PartSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def create_viewable(self: "Self") -> "_2472.ModalAnalysisViewable":
        """mastapy.system_model.drawing.ModalAnalysisViewable"""
        method_result = pythonnet_method_call(self.wrapped, "CreateViewable")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartModalAnalysis
        """
        return _Cast_PartModalAnalysis(self)
