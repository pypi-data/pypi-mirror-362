"""CompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results import _2888

_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "CompoundCriticalSpeedAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7895

    Self = TypeVar("Self", bound="CompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CompoundCriticalSpeedAnalysis._Cast_CompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CompoundCriticalSpeedAnalysis:
    """Special nested class for casting CompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "CompoundCriticalSpeedAnalysis"

    @property
    def compound_analysis(self: "CastSelf") -> "_2888.CompoundAnalysis":
        return self.__parent__._cast(_2888.CompoundAnalysis)

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7895.MarshalByRefObjectPermanent":
        from mastapy._private import _7895

        return self.__parent__._cast(_7895.MarshalByRefObjectPermanent)

    @property
    def compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "CompoundCriticalSpeedAnalysis":
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
class CompoundCriticalSpeedAnalysis(_2888.CompoundAnalysis):
    """CompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CompoundCriticalSpeedAnalysis
        """
        return _Cast_CompoundCriticalSpeedAnalysis(self)
