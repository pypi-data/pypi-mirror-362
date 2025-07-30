"""ContactChartPerToothPass"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CONTACT_CHART_PER_TOOTH_PASS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "ContactChartPerToothPass",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ContactChartPerToothPass")
    CastSelf = TypeVar(
        "CastSelf", bound="ContactChartPerToothPass._Cast_ContactChartPerToothPass"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ContactChartPerToothPass",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ContactChartPerToothPass:
    """Special nested class for casting ContactChartPerToothPass to subclasses."""

    __parent__: "ContactChartPerToothPass"

    @property
    def contact_chart_per_tooth_pass(self: "CastSelf") -> "ContactChartPerToothPass":
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
class ContactChartPerToothPass(_0.APIBase):
    """ContactChartPerToothPass

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONTACT_CHART_PER_TOOTH_PASS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def max_pressure(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaxPressure")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ContactChartPerToothPass":
        """Cast to another type.

        Returns:
            _Cast_ContactChartPerToothPass
        """
        return _Cast_ContactChartPerToothPass(self)
