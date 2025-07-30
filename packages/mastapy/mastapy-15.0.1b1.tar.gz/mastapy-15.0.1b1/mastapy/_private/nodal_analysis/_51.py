"""AnalysisSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_ANALYSIS_SETTINGS = python_net_import("SMT.MastaAPI.NodalAnalysis", "AnalysisSettings")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AnalysisSettings")
    CastSelf = TypeVar("CastSelf", bound="AnalysisSettings._Cast_AnalysisSettings")


__docformat__ = "restructuredtext en"
__all__ = ("AnalysisSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AnalysisSettings:
    """Special nested class for casting AnalysisSettings to subclasses."""

    __parent__: "AnalysisSettings"

    @property
    def analysis_settings(self: "CastSelf") -> "AnalysisSettings":
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
class AnalysisSettings(_0.APIBase):
    """AnalysisSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ANALYSIS_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AnalysisSettings":
        """Cast to another type.

        Returns:
            _Cast_AnalysisSettings
        """
        return _Cast_AnalysisSettings(self)
