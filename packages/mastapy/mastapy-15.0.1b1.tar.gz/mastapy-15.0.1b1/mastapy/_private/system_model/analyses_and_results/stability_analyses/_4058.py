"""CouplingHalfStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses import _4101

_COUPLING_HALF_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "CouplingHalfStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4042,
        _4045,
        _4047,
        _4062,
        _4103,
        _4105,
        _4112,
        _4117,
        _4127,
        _4140,
        _4141,
        _4142,
        _4145,
        _4147,
    )
    from mastapy._private.system_model.part_model.couplings import _2824

    Self = TypeVar("Self", bound="CouplingHalfStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfStabilityAnalysis._Cast_CouplingHalfStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfStabilityAnalysis:
    """Special nested class for casting CouplingHalfStabilityAnalysis to subclasses."""

    __parent__: "CouplingHalfStabilityAnalysis"

    @property
    def mountable_component_stability_analysis(
        self: "CastSelf",
    ) -> "_4101.MountableComponentStabilityAnalysis":
        return self.__parent__._cast(_4101.MountableComponentStabilityAnalysis)

    @property
    def component_stability_analysis(
        self: "CastSelf",
    ) -> "_4045.ComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4045,
        )

        return self.__parent__._cast(_4045.ComponentStabilityAnalysis)

    @property
    def part_stability_analysis(self: "CastSelf") -> "_4103.PartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4103,
        )

        return self.__parent__._cast(_4103.PartStabilityAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7890.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7890,
        )

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
    def clutch_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4042.ClutchHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4042,
        )

        return self.__parent__._cast(_4042.ClutchHalfStabilityAnalysis)

    @property
    def concept_coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4047.ConceptCouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4047,
        )

        return self.__parent__._cast(_4047.ConceptCouplingHalfStabilityAnalysis)

    @property
    def cvt_pulley_stability_analysis(
        self: "CastSelf",
    ) -> "_4062.CVTPulleyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4062,
        )

        return self.__parent__._cast(_4062.CVTPulleyStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4105.PartToPartShearCouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4105,
        )

        return self.__parent__._cast(_4105.PartToPartShearCouplingHalfStabilityAnalysis)

    @property
    def pulley_stability_analysis(self: "CastSelf") -> "_4112.PulleyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4112,
        )

        return self.__parent__._cast(_4112.PulleyStabilityAnalysis)

    @property
    def rolling_ring_stability_analysis(
        self: "CastSelf",
    ) -> "_4117.RollingRingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4117,
        )

        return self.__parent__._cast(_4117.RollingRingStabilityAnalysis)

    @property
    def spring_damper_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4127.SpringDamperHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4127,
        )

        return self.__parent__._cast(_4127.SpringDamperHalfStabilityAnalysis)

    @property
    def synchroniser_half_stability_analysis(
        self: "CastSelf",
    ) -> "_4140.SynchroniserHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4140,
        )

        return self.__parent__._cast(_4140.SynchroniserHalfStabilityAnalysis)

    @property
    def synchroniser_part_stability_analysis(
        self: "CastSelf",
    ) -> "_4141.SynchroniserPartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4141,
        )

        return self.__parent__._cast(_4141.SynchroniserPartStabilityAnalysis)

    @property
    def synchroniser_sleeve_stability_analysis(
        self: "CastSelf",
    ) -> "_4142.SynchroniserSleeveStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4142,
        )

        return self.__parent__._cast(_4142.SynchroniserSleeveStabilityAnalysis)

    @property
    def torque_converter_pump_stability_analysis(
        self: "CastSelf",
    ) -> "_4145.TorqueConverterPumpStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4145,
        )

        return self.__parent__._cast(_4145.TorqueConverterPumpStabilityAnalysis)

    @property
    def torque_converter_turbine_stability_analysis(
        self: "CastSelf",
    ) -> "_4147.TorqueConverterTurbineStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4147,
        )

        return self.__parent__._cast(_4147.TorqueConverterTurbineStabilityAnalysis)

    @property
    def coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "CouplingHalfStabilityAnalysis":
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
class CouplingHalfStabilityAnalysis(_4101.MountableComponentStabilityAnalysis):
    """CouplingHalfStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2824.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalfStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfStabilityAnalysis
        """
        return _Cast_CouplingHalfStabilityAnalysis(self)
