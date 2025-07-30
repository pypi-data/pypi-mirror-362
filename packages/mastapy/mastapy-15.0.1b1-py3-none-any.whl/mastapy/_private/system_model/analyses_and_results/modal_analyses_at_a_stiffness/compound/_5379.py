"""StraightBevelSunGearCompoundModalAnalysisAtAStiffness"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5372,
)

_STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "StraightBevelSunGearCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5248,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5269,
        _5281,
        _5290,
        _5297,
        _5323,
        _5344,
        _5346,
    )

    Self = TypeVar(
        "Self", bound="StraightBevelSunGearCompoundModalAnalysisAtAStiffness"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelSunGearCompoundModalAnalysisAtAStiffness._Cast_StraightBevelSunGearCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelSunGearCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelSunGearCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting StraightBevelSunGearCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "StraightBevelSunGearCompoundModalAnalysisAtAStiffness"

    @property
    def straight_bevel_diff_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5372.StraightBevelDiffGearCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(
            _5372.StraightBevelDiffGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5281.BevelGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5281,
        )

        return self.__parent__._cast(_5281.BevelGearCompoundModalAnalysisAtAStiffness)

    @property
    def agma_gleason_conical_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5269.AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5269,
        )

        return self.__parent__._cast(
            _5269.AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def conical_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5297.ConicalGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5297,
        )

        return self.__parent__._cast(_5297.ConicalGearCompoundModalAnalysisAtAStiffness)

    @property
    def gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5323.GearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5323,
        )

        return self.__parent__._cast(_5323.GearCompoundModalAnalysisAtAStiffness)

    @property
    def mountable_component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5344.MountableComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5344,
        )

        return self.__parent__._cast(
            _5344.MountableComponentCompoundModalAnalysisAtAStiffness
        )

    @property
    def component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5290.ComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5290,
        )

        return self.__parent__._cast(_5290.ComponentCompoundModalAnalysisAtAStiffness)

    @property
    def part_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5346.PartCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5346,
        )

        return self.__parent__._cast(_5346.PartCompoundModalAnalysisAtAStiffness)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7888.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7888,
        )

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
    def straight_bevel_sun_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "StraightBevelSunGearCompoundModalAnalysisAtAStiffness":
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
class StraightBevelSunGearCompoundModalAnalysisAtAStiffness(
    _5372.StraightBevelDiffGearCompoundModalAnalysisAtAStiffness
):
    """StraightBevelSunGearCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5248.StraightBevelSunGearModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.StraightBevelSunGearModalAnalysisAtAStiffness]

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
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5248.StraightBevelSunGearModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.StraightBevelSunGearModalAnalysisAtAStiffness]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_StraightBevelSunGearCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelSunGearCompoundModalAnalysisAtAStiffness
        """
        return _Cast_StraightBevelSunGearCompoundModalAnalysisAtAStiffness(self)
