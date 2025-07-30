"""PartParametricStudyTool"""

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
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7887

_PART_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "PartParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4561,
        _4562,
        _4563,
        _4566,
        _4567,
        _4568,
        _4569,
        _4571,
        _4573,
        _4574,
        _4575,
        _4576,
        _4578,
        _4579,
        _4580,
        _4581,
        _4583,
        _4584,
        _4586,
        _4588,
        _4589,
        _4591,
        _4592,
        _4594,
        _4595,
        _4597,
        _4599,
        _4600,
        _4602,
        _4603,
        _4604,
        _4606,
        _4609,
        _4610,
        _4611,
        _4612,
        _4620,
        _4622,
        _4623,
        _4624,
        _4625,
        _4627,
        _4628,
        _4629,
        _4631,
        _4632,
        _4635,
        _4636,
        _4638,
        _4639,
        _4641,
        _4642,
        _4643,
        _4644,
        _4645,
        _4646,
        _4648,
        _4649,
        _4655,
        _4663,
        _4664,
        _4666,
        _4667,
        _4668,
        _4669,
        _4670,
        _4671,
        _4673,
        _4675,
        _4676,
        _4677,
        _4678,
        _4680,
        _4682,
        _4683,
        _4685,
        _4686,
        _4688,
        _4689,
        _4691,
        _4692,
        _4693,
        _4694,
        _4695,
        _4696,
        _4697,
        _4698,
        _4700,
        _4701,
        _4702,
        _4703,
        _4704,
        _4706,
        _4707,
        _4709,
        _4710,
    )
    from mastapy._private.system_model.part_model import _2698
    from mastapy._private.utility_gui import _2053
    from mastapy._private.utility_gui.charts import _2062, _2068, _2070

    Self = TypeVar("Self", bound="PartParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf", bound="PartParametricStudyTool._Cast_PartParametricStudyTool"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartParametricStudyTool:
    """Special nested class for casting PartParametricStudyTool to subclasses."""

    __parent__: "PartParametricStudyTool"

    @property
    def part_analysis_case(self: "CastSelf") -> "_7887.PartAnalysisCase":
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
    def abstract_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4561.AbstractAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4561,
        )

        return self.__parent__._cast(_4561.AbstractAssemblyParametricStudyTool)

    @property
    def abstract_shaft_or_housing_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4562.AbstractShaftOrHousingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4562,
        )

        return self.__parent__._cast(_4562.AbstractShaftOrHousingParametricStudyTool)

    @property
    def abstract_shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4563.AbstractShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4563,
        )

        return self.__parent__._cast(_4563.AbstractShaftParametricStudyTool)

    @property
    def agma_gleason_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4566.AGMAGleasonConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4566,
        )

        return self.__parent__._cast(_4566.AGMAGleasonConicalGearParametricStudyTool)

    @property
    def agma_gleason_conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4567.AGMAGleasonConicalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4567,
        )

        return self.__parent__._cast(_4567.AGMAGleasonConicalGearSetParametricStudyTool)

    @property
    def assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4568.AssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4568,
        )

        return self.__parent__._cast(_4568.AssemblyParametricStudyTool)

    @property
    def bearing_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4569.BearingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4569,
        )

        return self.__parent__._cast(_4569.BearingParametricStudyTool)

    @property
    def belt_drive_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4571.BeltDriveParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4571,
        )

        return self.__parent__._cast(_4571.BeltDriveParametricStudyTool)

    @property
    def bevel_differential_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4573.BevelDifferentialGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4573,
        )

        return self.__parent__._cast(_4573.BevelDifferentialGearParametricStudyTool)

    @property
    def bevel_differential_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4574.BevelDifferentialGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4574,
        )

        return self.__parent__._cast(_4574.BevelDifferentialGearSetParametricStudyTool)

    @property
    def bevel_differential_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4575.BevelDifferentialPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4575,
        )

        return self.__parent__._cast(
            _4575.BevelDifferentialPlanetGearParametricStudyTool
        )

    @property
    def bevel_differential_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4576.BevelDifferentialSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4576,
        )

        return self.__parent__._cast(_4576.BevelDifferentialSunGearParametricStudyTool)

    @property
    def bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4578.BevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4578,
        )

        return self.__parent__._cast(_4578.BevelGearParametricStudyTool)

    @property
    def bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4579.BevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4579,
        )

        return self.__parent__._cast(_4579.BevelGearSetParametricStudyTool)

    @property
    def bolted_joint_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4580.BoltedJointParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4580,
        )

        return self.__parent__._cast(_4580.BoltedJointParametricStudyTool)

    @property
    def bolt_parametric_study_tool(self: "CastSelf") -> "_4581.BoltParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4581,
        )

        return self.__parent__._cast(_4581.BoltParametricStudyTool)

    @property
    def clutch_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4583.ClutchHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4583,
        )

        return self.__parent__._cast(_4583.ClutchHalfParametricStudyTool)

    @property
    def clutch_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4584.ClutchParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4584,
        )

        return self.__parent__._cast(_4584.ClutchParametricStudyTool)

    @property
    def component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4586.ComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4586,
        )

        return self.__parent__._cast(_4586.ComponentParametricStudyTool)

    @property
    def concept_coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4588.ConceptCouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4588,
        )

        return self.__parent__._cast(_4588.ConceptCouplingHalfParametricStudyTool)

    @property
    def concept_coupling_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4589.ConceptCouplingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4589,
        )

        return self.__parent__._cast(_4589.ConceptCouplingParametricStudyTool)

    @property
    def concept_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4591.ConceptGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4591,
        )

        return self.__parent__._cast(_4591.ConceptGearParametricStudyTool)

    @property
    def concept_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4592.ConceptGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4592,
        )

        return self.__parent__._cast(_4592.ConceptGearSetParametricStudyTool)

    @property
    def conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4594.ConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4594,
        )

        return self.__parent__._cast(_4594.ConicalGearParametricStudyTool)

    @property
    def conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4595.ConicalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4595,
        )

        return self.__parent__._cast(_4595.ConicalGearSetParametricStudyTool)

    @property
    def connector_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4597.ConnectorParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4597,
        )

        return self.__parent__._cast(_4597.ConnectorParametricStudyTool)

    @property
    def coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4599.CouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4599,
        )

        return self.__parent__._cast(_4599.CouplingHalfParametricStudyTool)

    @property
    def coupling_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4600.CouplingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4600,
        )

        return self.__parent__._cast(_4600.CouplingParametricStudyTool)

    @property
    def cvt_parametric_study_tool(self: "CastSelf") -> "_4602.CVTParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4602,
        )

        return self.__parent__._cast(_4602.CVTParametricStudyTool)

    @property
    def cvt_pulley_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4603.CVTPulleyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4603,
        )

        return self.__parent__._cast(_4603.CVTPulleyParametricStudyTool)

    @property
    def cycloidal_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4604.CycloidalAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4604,
        )

        return self.__parent__._cast(_4604.CycloidalAssemblyParametricStudyTool)

    @property
    def cycloidal_disc_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4606.CycloidalDiscParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4606,
        )

        return self.__parent__._cast(_4606.CycloidalDiscParametricStudyTool)

    @property
    def cylindrical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4609.CylindricalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4609,
        )

        return self.__parent__._cast(_4609.CylindricalGearParametricStudyTool)

    @property
    def cylindrical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4610.CylindricalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4610,
        )

        return self.__parent__._cast(_4610.CylindricalGearSetParametricStudyTool)

    @property
    def cylindrical_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4611.CylindricalPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4611,
        )

        return self.__parent__._cast(_4611.CylindricalPlanetGearParametricStudyTool)

    @property
    def datum_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4612.DatumParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4612,
        )

        return self.__parent__._cast(_4612.DatumParametricStudyTool)

    @property
    def external_cad_model_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4620.ExternalCADModelParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4620,
        )

        return self.__parent__._cast(_4620.ExternalCADModelParametricStudyTool)

    @property
    def face_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4622.FaceGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4622,
        )

        return self.__parent__._cast(_4622.FaceGearParametricStudyTool)

    @property
    def face_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4623.FaceGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4623,
        )

        return self.__parent__._cast(_4623.FaceGearSetParametricStudyTool)

    @property
    def fe_part_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4624.FEPartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4624,
        )

        return self.__parent__._cast(_4624.FEPartParametricStudyTool)

    @property
    def flexible_pin_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4625.FlexiblePinAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4625,
        )

        return self.__parent__._cast(_4625.FlexiblePinAssemblyParametricStudyTool)

    @property
    def gear_parametric_study_tool(self: "CastSelf") -> "_4627.GearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4627,
        )

        return self.__parent__._cast(_4627.GearParametricStudyTool)

    @property
    def gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4628.GearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4628,
        )

        return self.__parent__._cast(_4628.GearSetParametricStudyTool)

    @property
    def guide_dxf_model_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4629.GuideDxfModelParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4629,
        )

        return self.__parent__._cast(_4629.GuideDxfModelParametricStudyTool)

    @property
    def hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4631.HypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4631,
        )

        return self.__parent__._cast(_4631.HypoidGearParametricStudyTool)

    @property
    def hypoid_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4632.HypoidGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4632,
        )

        return self.__parent__._cast(_4632.HypoidGearSetParametricStudyTool)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4635.KlingelnbergCycloPalloidConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4635,
        )

        return self.__parent__._cast(
            _4635.KlingelnbergCycloPalloidConicalGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4636.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4636,
        )

        return self.__parent__._cast(
            _4636.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4638.KlingelnbergCycloPalloidHypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4638,
        )

        return self.__parent__._cast(
            _4638.KlingelnbergCycloPalloidHypoidGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4639.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4639,
        )

        return self.__parent__._cast(
            _4639.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4641.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4641,
        )

        return self.__parent__._cast(
            _4641.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4642.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4642,
        )

        return self.__parent__._cast(
            _4642.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool
        )

    @property
    def mass_disc_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4643.MassDiscParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4643,
        )

        return self.__parent__._cast(_4643.MassDiscParametricStudyTool)

    @property
    def measurement_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4644.MeasurementComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4644,
        )

        return self.__parent__._cast(_4644.MeasurementComponentParametricStudyTool)

    @property
    def microphone_array_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4645.MicrophoneArrayParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4645,
        )

        return self.__parent__._cast(_4645.MicrophoneArrayParametricStudyTool)

    @property
    def microphone_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4646.MicrophoneParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4646,
        )

        return self.__parent__._cast(_4646.MicrophoneParametricStudyTool)

    @property
    def mountable_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4648.MountableComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4648,
        )

        return self.__parent__._cast(_4648.MountableComponentParametricStudyTool)

    @property
    def oil_seal_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4649.OilSealParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4649,
        )

        return self.__parent__._cast(_4649.OilSealParametricStudyTool)

    @property
    def part_to_part_shear_coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4663.PartToPartShearCouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4663,
        )

        return self.__parent__._cast(
            _4663.PartToPartShearCouplingHalfParametricStudyTool
        )

    @property
    def part_to_part_shear_coupling_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4664.PartToPartShearCouplingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4664,
        )

        return self.__parent__._cast(_4664.PartToPartShearCouplingParametricStudyTool)

    @property
    def planetary_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4666.PlanetaryGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4666,
        )

        return self.__parent__._cast(_4666.PlanetaryGearSetParametricStudyTool)

    @property
    def planet_carrier_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4667.PlanetCarrierParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4667,
        )

        return self.__parent__._cast(_4667.PlanetCarrierParametricStudyTool)

    @property
    def point_load_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4668.PointLoadParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4668,
        )

        return self.__parent__._cast(_4668.PointLoadParametricStudyTool)

    @property
    def power_load_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4669.PowerLoadParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4669,
        )

        return self.__parent__._cast(_4669.PowerLoadParametricStudyTool)

    @property
    def pulley_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4670.PulleyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4670,
        )

        return self.__parent__._cast(_4670.PulleyParametricStudyTool)

    @property
    def ring_pins_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4671.RingPinsParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4671,
        )

        return self.__parent__._cast(_4671.RingPinsParametricStudyTool)

    @property
    def rolling_ring_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4673.RollingRingAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4673,
        )

        return self.__parent__._cast(_4673.RollingRingAssemblyParametricStudyTool)

    @property
    def rolling_ring_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4675.RollingRingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4675,
        )

        return self.__parent__._cast(_4675.RollingRingParametricStudyTool)

    @property
    def root_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4676.RootAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4676,
        )

        return self.__parent__._cast(_4676.RootAssemblyParametricStudyTool)

    @property
    def shaft_hub_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4677.ShaftHubConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4677,
        )

        return self.__parent__._cast(_4677.ShaftHubConnectionParametricStudyTool)

    @property
    def shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4678.ShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4678,
        )

        return self.__parent__._cast(_4678.ShaftParametricStudyTool)

    @property
    def specialised_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4680.SpecialisedAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4680,
        )

        return self.__parent__._cast(_4680.SpecialisedAssemblyParametricStudyTool)

    @property
    def spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4682.SpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4682,
        )

        return self.__parent__._cast(_4682.SpiralBevelGearParametricStudyTool)

    @property
    def spiral_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4683.SpiralBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4683,
        )

        return self.__parent__._cast(_4683.SpiralBevelGearSetParametricStudyTool)

    @property
    def spring_damper_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4685.SpringDamperHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4685,
        )

        return self.__parent__._cast(_4685.SpringDamperHalfParametricStudyTool)

    @property
    def spring_damper_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4686.SpringDamperParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4686,
        )

        return self.__parent__._cast(_4686.SpringDamperParametricStudyTool)

    @property
    def straight_bevel_diff_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4688.StraightBevelDiffGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4688,
        )

        return self.__parent__._cast(_4688.StraightBevelDiffGearParametricStudyTool)

    @property
    def straight_bevel_diff_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4689.StraightBevelDiffGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4689,
        )

        return self.__parent__._cast(_4689.StraightBevelDiffGearSetParametricStudyTool)

    @property
    def straight_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4691.StraightBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4691,
        )

        return self.__parent__._cast(_4691.StraightBevelGearParametricStudyTool)

    @property
    def straight_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4692.StraightBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4692,
        )

        return self.__parent__._cast(_4692.StraightBevelGearSetParametricStudyTool)

    @property
    def straight_bevel_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4693.StraightBevelPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4693,
        )

        return self.__parent__._cast(_4693.StraightBevelPlanetGearParametricStudyTool)

    @property
    def straight_bevel_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4694.StraightBevelSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4694,
        )

        return self.__parent__._cast(_4694.StraightBevelSunGearParametricStudyTool)

    @property
    def synchroniser_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4695.SynchroniserHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4695,
        )

        return self.__parent__._cast(_4695.SynchroniserHalfParametricStudyTool)

    @property
    def synchroniser_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4696.SynchroniserParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4696,
        )

        return self.__parent__._cast(_4696.SynchroniserParametricStudyTool)

    @property
    def synchroniser_part_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4697.SynchroniserPartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4697,
        )

        return self.__parent__._cast(_4697.SynchroniserPartParametricStudyTool)

    @property
    def synchroniser_sleeve_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4698.SynchroniserSleeveParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4698,
        )

        return self.__parent__._cast(_4698.SynchroniserSleeveParametricStudyTool)

    @property
    def torque_converter_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4700.TorqueConverterParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4700,
        )

        return self.__parent__._cast(_4700.TorqueConverterParametricStudyTool)

    @property
    def torque_converter_pump_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4701.TorqueConverterPumpParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4701,
        )

        return self.__parent__._cast(_4701.TorqueConverterPumpParametricStudyTool)

    @property
    def torque_converter_turbine_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4702.TorqueConverterTurbineParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4702,
        )

        return self.__parent__._cast(_4702.TorqueConverterTurbineParametricStudyTool)

    @property
    def unbalanced_mass_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4703.UnbalancedMassParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4703,
        )

        return self.__parent__._cast(_4703.UnbalancedMassParametricStudyTool)

    @property
    def virtual_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4704.VirtualComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4704,
        )

        return self.__parent__._cast(_4704.VirtualComponentParametricStudyTool)

    @property
    def worm_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4706.WormGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4706,
        )

        return self.__parent__._cast(_4706.WormGearParametricStudyTool)

    @property
    def worm_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4707.WormGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4707,
        )

        return self.__parent__._cast(_4707.WormGearSetParametricStudyTool)

    @property
    def zerol_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4709.ZerolBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4709,
        )

        return self.__parent__._cast(_4709.ZerolBevelGearParametricStudyTool)

    @property
    def zerol_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4710.ZerolBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4710,
        )

        return self.__parent__._cast(_4710.ZerolBevelGearSetParametricStudyTool)

    @property
    def part_parametric_study_tool(self: "CastSelf") -> "PartParametricStudyTool":
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
class PartParametricStudyTool(_7887.PartAnalysisCase):
    """PartParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def design_of_experiments_chart(self: "Self") -> "_2062.NDChartDefinition":
        """mastapy.utility_gui.charts.NDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignOfExperimentsChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def linear_sweep_chart_2d(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearSweepChart2D")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def linear_sweep_chart_3d(self: "Self") -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearSweepChart3D")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def data_logger(self: "Self") -> "_2053.DataLoggerWithCharts":
        """mastapy.utility_gui.DataLoggerWithCharts

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DataLogger")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def parametric_study_tool(self: "Self") -> "_4655.ParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyTool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParametricStudyTool")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PartParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_PartParametricStudyTool
        """
        return _Cast_PartParametricStudyTool(self)
