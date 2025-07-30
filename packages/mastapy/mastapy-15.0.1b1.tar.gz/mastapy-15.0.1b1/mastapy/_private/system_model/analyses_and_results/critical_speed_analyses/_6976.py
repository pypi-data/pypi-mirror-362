"""StraightBevelSunGearCriticalSpeedAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
    _6969,
)

_STRAIGHT_BEVEL_SUN_GEAR_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "StraightBevelSunGearCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6863,
        _6875,
        _6884,
        _6891,
        _6920,
        _6941,
        _6943,
    )
    from mastapy._private.system_model.part_model.gears import _2788

    Self = TypeVar("Self", bound="StraightBevelSunGearCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelSunGearCriticalSpeedAnalysis._Cast_StraightBevelSunGearCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelSunGearCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelSunGearCriticalSpeedAnalysis:
    """Special nested class for casting StraightBevelSunGearCriticalSpeedAnalysis to subclasses."""

    __parent__: "StraightBevelSunGearCriticalSpeedAnalysis"

    @property
    def straight_bevel_diff_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6969.StraightBevelDiffGearCriticalSpeedAnalysis":
        return self.__parent__._cast(_6969.StraightBevelDiffGearCriticalSpeedAnalysis)

    @property
    def bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6875.BevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6875,
        )

        return self.__parent__._cast(_6875.BevelGearCriticalSpeedAnalysis)

    @property
    def agma_gleason_conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6863.AGMAGleasonConicalGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6863,
        )

        return self.__parent__._cast(_6863.AGMAGleasonConicalGearCriticalSpeedAnalysis)

    @property
    def conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6891.ConicalGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6891,
        )

        return self.__parent__._cast(_6891.ConicalGearCriticalSpeedAnalysis)

    @property
    def gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6920.GearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6920,
        )

        return self.__parent__._cast(_6920.GearCriticalSpeedAnalysis)

    @property
    def mountable_component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6941.MountableComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6941,
        )

        return self.__parent__._cast(_6941.MountableComponentCriticalSpeedAnalysis)

    @property
    def component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6884.ComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6884,
        )

        return self.__parent__._cast(_6884.ComponentCriticalSpeedAnalysis)

    @property
    def part_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6943.PartCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6943,
        )

        return self.__parent__._cast(_6943.PartCriticalSpeedAnalysis)

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
    def straight_bevel_sun_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "StraightBevelSunGearCriticalSpeedAnalysis":
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
class StraightBevelSunGearCriticalSpeedAnalysis(
    _6969.StraightBevelDiffGearCriticalSpeedAnalysis
):
    """StraightBevelSunGearCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_SUN_GEAR_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2788.StraightBevelSunGear":
        """mastapy.system_model.part_model.gears.StraightBevelSunGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelSunGearCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelSunGearCriticalSpeedAnalysis
        """
        return _Cast_StraightBevelSunGearCriticalSpeedAnalysis(self)
