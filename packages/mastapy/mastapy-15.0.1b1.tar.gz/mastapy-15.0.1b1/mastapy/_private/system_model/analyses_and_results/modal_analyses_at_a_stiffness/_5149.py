"""BevelGearModalAnalysisAtAStiffness"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _5137,
)

_BEVEL_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
    "BevelGearModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5144,
        _5146,
        _5147,
        _5157,
        _5165,
        _5192,
        _5213,
        _5215,
        _5236,
        _5242,
        _5245,
        _5247,
        _5248,
        _5263,
    )
    from mastapy._private.system_model.part_model.gears import _2756

    Self = TypeVar("Self", bound="BevelGearModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearModalAnalysisAtAStiffness._Cast_BevelGearModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearModalAnalysisAtAStiffness:
    """Special nested class for casting BevelGearModalAnalysisAtAStiffness to subclasses."""

    __parent__: "BevelGearModalAnalysisAtAStiffness"

    @property
    def agma_gleason_conical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5137.AGMAGleasonConicalGearModalAnalysisAtAStiffness":
        return self.__parent__._cast(
            _5137.AGMAGleasonConicalGearModalAnalysisAtAStiffness
        )

    @property
    def conical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5165.ConicalGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5165,
        )

        return self.__parent__._cast(_5165.ConicalGearModalAnalysisAtAStiffness)

    @property
    def gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5192.GearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5192,
        )

        return self.__parent__._cast(_5192.GearModalAnalysisAtAStiffness)

    @property
    def mountable_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5213.MountableComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5213,
        )

        return self.__parent__._cast(_5213.MountableComponentModalAnalysisAtAStiffness)

    @property
    def component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5157.ComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5157,
        )

        return self.__parent__._cast(_5157.ComponentModalAnalysisAtAStiffness)

    @property
    def part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5215.PartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5215,
        )

        return self.__parent__._cast(_5215.PartModalAnalysisAtAStiffness)

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
    def bevel_differential_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5144.BevelDifferentialGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5144,
        )

        return self.__parent__._cast(
            _5144.BevelDifferentialGearModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5146.BevelDifferentialPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5146,
        )

        return self.__parent__._cast(
            _5146.BevelDifferentialPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_sun_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5147.BevelDifferentialSunGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5147,
        )

        return self.__parent__._cast(
            _5147.BevelDifferentialSunGearModalAnalysisAtAStiffness
        )

    @property
    def spiral_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5236.SpiralBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5236,
        )

        return self.__parent__._cast(_5236.SpiralBevelGearModalAnalysisAtAStiffness)

    @property
    def straight_bevel_diff_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5242.StraightBevelDiffGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5242,
        )

        return self.__parent__._cast(
            _5242.StraightBevelDiffGearModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5245.StraightBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5245,
        )

        return self.__parent__._cast(_5245.StraightBevelGearModalAnalysisAtAStiffness)

    @property
    def straight_bevel_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5247.StraightBevelPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5247,
        )

        return self.__parent__._cast(
            _5247.StraightBevelPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_sun_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5248.StraightBevelSunGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5248,
        )

        return self.__parent__._cast(
            _5248.StraightBevelSunGearModalAnalysisAtAStiffness
        )

    @property
    def zerol_bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5263.ZerolBevelGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5263,
        )

        return self.__parent__._cast(_5263.ZerolBevelGearModalAnalysisAtAStiffness)

    @property
    def bevel_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "BevelGearModalAnalysisAtAStiffness":
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
class BevelGearModalAnalysisAtAStiffness(
    _5137.AGMAGleasonConicalGearModalAnalysisAtAStiffness
):
    """BevelGearModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2756.BevelGear":
        """mastapy.system_model.part_model.gears.BevelGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_BevelGearModalAnalysisAtAStiffness
        """
        return _Cast_BevelGearModalAnalysisAtAStiffness(self)
