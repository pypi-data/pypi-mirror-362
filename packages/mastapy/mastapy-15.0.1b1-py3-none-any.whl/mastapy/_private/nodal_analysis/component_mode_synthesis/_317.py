"""HarmonicCMSResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.component_mode_synthesis import _315

_HARMONIC_CMS_RESULTS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis", "HarmonicCMSResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HarmonicCMSResults")
    CastSelf = TypeVar("CastSelf", bound="HarmonicCMSResults._Cast_HarmonicCMSResults")


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicCMSResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicCMSResults:
    """Special nested class for casting HarmonicCMSResults to subclasses."""

    __parent__: "HarmonicCMSResults"

    @property
    def cms_results(self: "CastSelf") -> "_315.CMSResults":
        return self.__parent__._cast(_315.CMSResults)

    @property
    def harmonic_cms_results(self: "CastSelf") -> "HarmonicCMSResults":
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
class HarmonicCMSResults(_315.CMSResults):
    """HarmonicCMSResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_CMS_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicCMSResults":
        """Cast to another type.

        Returns:
            _Cast_HarmonicCMSResults
        """
        return _Cast_HarmonicCMSResults(self)
