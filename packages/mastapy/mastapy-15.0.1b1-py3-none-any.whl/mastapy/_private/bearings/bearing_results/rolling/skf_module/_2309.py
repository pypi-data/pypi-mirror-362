"""Viscosities"""

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
from mastapy._private.bearings.bearing_results.rolling.skf_module import _2305

_VISCOSITIES = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "Viscosities"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.skf_module import _2301

    Self = TypeVar("Self", bound="Viscosities")
    CastSelf = TypeVar("CastSelf", bound="Viscosities._Cast_Viscosities")


__docformat__ = "restructuredtext en"
__all__ = ("Viscosities",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Viscosities:
    """Special nested class for casting Viscosities to subclasses."""

    __parent__: "Viscosities"

    @property
    def skf_calculation_result(self: "CastSelf") -> "_2305.SKFCalculationResult":
        return self.__parent__._cast(_2305.SKFCalculationResult)

    @property
    def viscosities(self: "CastSelf") -> "Viscosities":
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
class Viscosities(_2305.SKFCalculationResult):
    """Viscosities

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VISCOSITIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def viscosity_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ViscosityRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def operating_viscosity(self: "Self") -> "_2301.OperatingViscosity":
        """mastapy.bearings.bearing_results.rolling.skf_module.OperatingViscosity

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingViscosity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_Viscosities":
        """Cast to another type.

        Returns:
            _Cast_Viscosities
        """
        return _Cast_Viscosities(self)
