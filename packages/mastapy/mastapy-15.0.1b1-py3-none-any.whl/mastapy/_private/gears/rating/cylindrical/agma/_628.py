"""ThermalReductionFactorFactorsAndExponents"""

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

_THERMAL_REDUCTION_FACTOR_FACTORS_AND_EXPONENTS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.AGMA",
    "ThermalReductionFactorFactorsAndExponents",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ThermalReductionFactorFactorsAndExponents")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ThermalReductionFactorFactorsAndExponents._Cast_ThermalReductionFactorFactorsAndExponents",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThermalReductionFactorFactorsAndExponents",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalReductionFactorFactorsAndExponents:
    """Special nested class for casting ThermalReductionFactorFactorsAndExponents to subclasses."""

    __parent__: "ThermalReductionFactorFactorsAndExponents"

    @property
    def thermal_reduction_factor_factors_and_exponents(
        self: "CastSelf",
    ) -> "ThermalReductionFactorFactorsAndExponents":
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
class ThermalReductionFactorFactorsAndExponents(_0.APIBase):
    """ThermalReductionFactorFactorsAndExponents

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_REDUCTION_FACTOR_FACTORS_AND_EXPONENTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def first_exponent(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FirstExponent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def first_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FirstFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def second_exponent(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SecondExponent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def second_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SecondFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ThermalReductionFactorFactorsAndExponents":
        """Cast to another type.

        Returns:
            _Cast_ThermalReductionFactorFactorsAndExponents
        """
        return _Cast_ThermalReductionFactorFactorsAndExponents(self)
