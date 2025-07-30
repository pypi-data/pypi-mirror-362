"""ODonoghueAndCameronCoefficientOfFrictionCalculator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.materials import _691

_O_DONOGHUE_AND_CAMERON_COEFFICIENT_OF_FRICTION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "ODonoghueAndCameronCoefficientOfFrictionCalculator"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.materials import _681

    Self = TypeVar("Self", bound="ODonoghueAndCameronCoefficientOfFrictionCalculator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ODonoghueAndCameronCoefficientOfFrictionCalculator._Cast_ODonoghueAndCameronCoefficientOfFrictionCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ODonoghueAndCameronCoefficientOfFrictionCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ODonoghueAndCameronCoefficientOfFrictionCalculator:
    """Special nested class for casting ODonoghueAndCameronCoefficientOfFrictionCalculator to subclasses."""

    __parent__: "ODonoghueAndCameronCoefficientOfFrictionCalculator"

    @property
    def instantaneous_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_691.InstantaneousCoefficientOfFrictionCalculator":
        return self.__parent__._cast(_691.InstantaneousCoefficientOfFrictionCalculator)

    @property
    def coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_681.CoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _681

        return self.__parent__._cast(_681.CoefficientOfFrictionCalculator)

    @property
    def o_donoghue_and_cameron_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "ODonoghueAndCameronCoefficientOfFrictionCalculator":
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
class ODonoghueAndCameronCoefficientOfFrictionCalculator(
    _691.InstantaneousCoefficientOfFrictionCalculator
):
    """ODonoghueAndCameronCoefficientOfFrictionCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _O_DONOGHUE_AND_CAMERON_COEFFICIENT_OF_FRICTION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ODonoghueAndCameronCoefficientOfFrictionCalculator":
        """Cast to another type.

        Returns:
            _Cast_ODonoghueAndCameronCoefficientOfFrictionCalculator
        """
        return _Cast_ODonoghueAndCameronCoefficientOfFrictionCalculator(self)
