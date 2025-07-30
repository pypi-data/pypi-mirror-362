"""BearingLoads"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling.skf_module import _2305

_BEARING_LOADS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "BearingLoads"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingLoads")
    CastSelf = TypeVar("CastSelf", bound="BearingLoads._Cast_BearingLoads")


__docformat__ = "restructuredtext en"
__all__ = ("BearingLoads",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingLoads:
    """Special nested class for casting BearingLoads to subclasses."""

    __parent__: "BearingLoads"

    @property
    def skf_calculation_result(self: "CastSelf") -> "_2305.SKFCalculationResult":
        return self.__parent__._cast(_2305.SKFCalculationResult)

    @property
    def bearing_loads(self: "CastSelf") -> "BearingLoads":
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
class BearingLoads(_2305.SKFCalculationResult):
    """BearingLoads

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_LOADS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def equivalent_dynamic_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EquivalentDynamicLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_BearingLoads":
        """Cast to another type.

        Returns:
            _Cast_BearingLoads
        """
        return _Cast_BearingLoads(self)
