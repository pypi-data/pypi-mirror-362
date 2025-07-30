"""KlingelnbergCycloPalloidHypoidGearModalAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4914

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "KlingelnbergCycloPalloidHypoidGearModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4867,
        _4875,
        _4906,
        _4931,
        _4935,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7784
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3014,
    )
    from mastapy._private.system_model.part_model.gears import _2775

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidHypoidGearModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearModalAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearModalAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearModalAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearModalAnalysis"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4914.KlingelnbergCycloPalloidConicalGearModalAnalysis":
        return self.__parent__._cast(
            _4914.KlingelnbergCycloPalloidConicalGearModalAnalysis
        )

    @property
    def conical_gear_modal_analysis(
        self: "CastSelf",
    ) -> "_4875.ConicalGearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4875,
        )

        return self.__parent__._cast(_4875.ConicalGearModalAnalysis)

    @property
    def gear_modal_analysis(self: "CastSelf") -> "_4906.GearModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4906,
        )

        return self.__parent__._cast(_4906.GearModalAnalysis)

    @property
    def mountable_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4931.MountableComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4931,
        )

        return self.__parent__._cast(_4931.MountableComponentModalAnalysis)

    @property
    def component_modal_analysis(self: "CastSelf") -> "_4867.ComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4867,
        )

        return self.__parent__._cast(_4867.ComponentModalAnalysis)

    @property
    def part_modal_analysis(self: "CastSelf") -> "_4935.PartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4935,
        )

        return self.__parent__._cast(_4935.PartModalAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearModalAnalysis":
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
class KlingelnbergCycloPalloidHypoidGearModalAnalysis(
    _4914.KlingelnbergCycloPalloidConicalGearModalAnalysis
):
    """KlingelnbergCycloPalloidHypoidGearModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2775.KlingelnbergCycloPalloidHypoidGear":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear

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
    def component_load_case(
        self: "Self",
    ) -> "_7784.KlingelnbergCycloPalloidHypoidGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_deflection_results(
        self: "Self",
    ) -> "_3014.KlingelnbergCycloPalloidHypoidGearSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidHypoidGearSystemDeflection

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
    ) -> "_Cast_KlingelnbergCycloPalloidHypoidGearModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearModalAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearModalAnalysis(self)
