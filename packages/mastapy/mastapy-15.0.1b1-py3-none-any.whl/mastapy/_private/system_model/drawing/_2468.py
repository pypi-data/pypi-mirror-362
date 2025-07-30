"""CriticalSpeedAnalysisViewable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.drawing import _2476

_CRITICAL_SPEED_ANALYSIS_VIEWABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "CriticalSpeedAnalysisViewable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CriticalSpeedAnalysisViewable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CriticalSpeedAnalysisViewable._Cast_CriticalSpeedAnalysisViewable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CriticalSpeedAnalysisViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CriticalSpeedAnalysisViewable:
    """Special nested class for casting CriticalSpeedAnalysisViewable to subclasses."""

    __parent__: "CriticalSpeedAnalysisViewable"

    @property
    def rotor_dynamics_viewable(self: "CastSelf") -> "_2476.RotorDynamicsViewable":
        return self.__parent__._cast(_2476.RotorDynamicsViewable)

    @property
    def critical_speed_analysis_viewable(
        self: "CastSelf",
    ) -> "CriticalSpeedAnalysisViewable":
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
class CriticalSpeedAnalysisViewable(_2476.RotorDynamicsViewable):
    """CriticalSpeedAnalysisViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CRITICAL_SPEED_ANALYSIS_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CriticalSpeedAnalysisViewable":
        """Cast to another type.

        Returns:
            _Cast_CriticalSpeedAnalysisViewable
        """
        return _Cast_CriticalSpeedAnalysisViewable(self)
