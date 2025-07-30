"""AdjustmentFactors"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ADJUSTMENT_FACTORS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "AdjustmentFactors"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AdjustmentFactors")
    CastSelf = TypeVar("CastSelf", bound="AdjustmentFactors._Cast_AdjustmentFactors")


__docformat__ = "restructuredtext en"
__all__ = ("AdjustmentFactors",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AdjustmentFactors:
    """Special nested class for casting AdjustmentFactors to subclasses."""

    __parent__: "AdjustmentFactors"

    @property
    def adjustment_factors(self: "CastSelf") -> "AdjustmentFactors":
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
class AdjustmentFactors(_0.APIBase):
    """AdjustmentFactors

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ADJUSTMENT_FACTORS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def for_bearing_load_p(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForBearingLoadP")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def oil_viscosity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilViscosity")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AdjustmentFactors":
        """Cast to another type.

        Returns:
            _Cast_AdjustmentFactors
        """
        return _Cast_AdjustmentFactors(self)
