"""HypoidGearModalAnalysisAtASpeed"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
    _5401,
)

_HYPOID_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "HypoidGearModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5421,
        _5429,
        _5455,
        _5476,
        _5478,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7774
    from mastapy._private.system_model.part_model.gears import _2771

    Self = TypeVar("Self", bound="HypoidGearModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HypoidGearModalAnalysisAtASpeed._Cast_HypoidGearModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidGearModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidGearModalAnalysisAtASpeed:
    """Special nested class for casting HypoidGearModalAnalysisAtASpeed to subclasses."""

    __parent__: "HypoidGearModalAnalysisAtASpeed"

    @property
    def agma_gleason_conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5401.AGMAGleasonConicalGearModalAnalysisAtASpeed":
        return self.__parent__._cast(_5401.AGMAGleasonConicalGearModalAnalysisAtASpeed)

    @property
    def conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5429.ConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5429,
        )

        return self.__parent__._cast(_5429.ConicalGearModalAnalysisAtASpeed)

    @property
    def gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5455.GearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5455,
        )

        return self.__parent__._cast(_5455.GearModalAnalysisAtASpeed)

    @property
    def mountable_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5476.MountableComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5476,
        )

        return self.__parent__._cast(_5476.MountableComponentModalAnalysisAtASpeed)

    @property
    def component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5421.ComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5421,
        )

        return self.__parent__._cast(_5421.ComponentModalAnalysisAtASpeed)

    @property
    def part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5478.PartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5478,
        )

        return self.__parent__._cast(_5478.PartModalAnalysisAtASpeed)

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
    def hypoid_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "HypoidGearModalAnalysisAtASpeed":
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
class HypoidGearModalAnalysisAtASpeed(
    _5401.AGMAGleasonConicalGearModalAnalysisAtASpeed
):
    """HypoidGearModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_GEAR_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2771.HypoidGear":
        """mastapy.system_model.part_model.gears.HypoidGear

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
    def component_load_case(self: "Self") -> "_7774.HypoidGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_HypoidGearModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_HypoidGearModalAnalysisAtASpeed
        """
        return _Cast_HypoidGearModalAnalysisAtASpeed(self)
