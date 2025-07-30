"""CouplingHalfAdvancedTimeSteppingAnalysisForModulation"""

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
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7209,
)

_COUPLING_HALF_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "CouplingHalfAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7152,
        _7154,
        _7157,
        _7171,
        _7211,
        _7214,
        _7220,
        _7223,
        _7236,
        _7246,
        _7247,
        _7248,
        _7251,
        _7252,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2971,
    )
    from mastapy._private.system_model.part_model.couplings import _2824

    Self = TypeVar(
        "Self", bound="CouplingHalfAdvancedTimeSteppingAnalysisForModulation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfAdvancedTimeSteppingAnalysisForModulation._Cast_CouplingHalfAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting CouplingHalfAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "CouplingHalfAdvancedTimeSteppingAnalysisForModulation"

    @property
    def mountable_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7209.MountableComponentAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7209.MountableComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7154.ComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7154,
        )

        return self.__parent__._cast(
            _7154.ComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7211.PartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7211,
        )

        return self.__parent__._cast(
            _7211.PartAdvancedTimeSteppingAnalysisForModulation
        )

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
    def clutch_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7152.ClutchHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7152,
        )

        return self.__parent__._cast(
            _7152.ClutchHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7157.ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7157,
        )

        return self.__parent__._cast(
            _7157.ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cvt_pulley_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7171.CVTPulleyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7171,
        )

        return self.__parent__._cast(
            _7171.CVTPulleyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7214.PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7214,
        )

        return self.__parent__._cast(
            _7214.PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def pulley_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7220.PulleyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7220,
        )

        return self.__parent__._cast(
            _7220.PulleyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7223.RollingRingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7223,
        )

        return self.__parent__._cast(
            _7223.RollingRingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7236.SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7236,
        )

        return self.__parent__._cast(
            _7236.SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7246.SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7246,
        )

        return self.__parent__._cast(
            _7246.SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7247.SynchroniserPartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7247,
        )

        return self.__parent__._cast(
            _7247.SynchroniserPartAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_sleeve_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7248.SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7248,
        )

        return self.__parent__._cast(
            _7248.SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_pump_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7251.TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7251,
        )

        return self.__parent__._cast(
            _7251.TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_turbine_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7252.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7252,
        )

        return self.__parent__._cast(
            _7252.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "CouplingHalfAdvancedTimeSteppingAnalysisForModulation":
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
class CouplingHalfAdvancedTimeSteppingAnalysisForModulation(
    _7209.MountableComponentAdvancedTimeSteppingAnalysisForModulation
):
    """CouplingHalfAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _COUPLING_HALF_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

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
    @exception_bridge
    def system_deflection_results(self: "Self") -> "_2971.CouplingHalfSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CouplingHalfSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_CouplingHalfAdvancedTimeSteppingAnalysisForModulation(self)
