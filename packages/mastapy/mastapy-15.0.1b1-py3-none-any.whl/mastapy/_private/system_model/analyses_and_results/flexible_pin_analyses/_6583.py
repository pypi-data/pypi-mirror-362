"""FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
    _6581,
)

_FLEXIBLE_PIN_ANALYSIS_DETAIL_LEVEL_AND_PIN_FATIGUE_ONE_TOOTH_PASS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses",
    "FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
        _6580,
    )

    Self = TypeVar(
        "Self", bound="FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass._Cast_FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass:
    """Special nested class for casting FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass to subclasses."""

    __parent__: "FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass"

    @property
    def flexible_pin_analysis(self: "CastSelf") -> "_6581.FlexiblePinAnalysis":
        return self.__parent__._cast(_6581.FlexiblePinAnalysis)

    @property
    def combination_analysis(self: "CastSelf") -> "_6580.CombinationAnalysis":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6580,
        )

        return self.__parent__._cast(_6580.CombinationAnalysis)

    @property
    def flexible_pin_analysis_detail_level_and_pin_fatigue_one_tooth_pass(
        self: "CastSelf",
    ) -> "FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass":
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
class FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass(
    _6581.FlexiblePinAnalysis
):
    """FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _FLEXIBLE_PIN_ANALYSIS_DETAIL_LEVEL_AND_PIN_FATIGUE_ONE_TOOTH_PASS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass":
        """Cast to another type.

        Returns:
            _Cast_FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass
        """
        return _Cast_FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass(self)
