"""ISO14179Part2CoefficientOfFrictionCalculatorBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.materials import _681

_ISO14179_PART_2_COEFFICIENT_OF_FRICTION_CALCULATOR_BASE = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "ISO14179Part2CoefficientOfFrictionCalculatorBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.materials import _693, _695

    Self = TypeVar("Self", bound="ISO14179Part2CoefficientOfFrictionCalculatorBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO14179Part2CoefficientOfFrictionCalculatorBase._Cast_ISO14179Part2CoefficientOfFrictionCalculatorBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO14179Part2CoefficientOfFrictionCalculatorBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO14179Part2CoefficientOfFrictionCalculatorBase:
    """Special nested class for casting ISO14179Part2CoefficientOfFrictionCalculatorBase to subclasses."""

    __parent__: "ISO14179Part2CoefficientOfFrictionCalculatorBase"

    @property
    def coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_681.CoefficientOfFrictionCalculator":
        return self.__parent__._cast(_681.CoefficientOfFrictionCalculator)

    @property
    def iso14179_part_2_coefficient_of_friction_calculator(
        self: "CastSelf",
    ) -> "_693.ISO14179Part2CoefficientOfFrictionCalculator":
        from mastapy._private.gears.materials import _693

        return self.__parent__._cast(_693.ISO14179Part2CoefficientOfFrictionCalculator)

    @property
    def iso14179_part_2_coefficient_of_friction_calculator_with_martins_modification(
        self: "CastSelf",
    ) -> "_695.ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification":
        from mastapy._private.gears.materials import _695

        return self.__parent__._cast(
            _695.ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification
        )

    @property
    def iso14179_part_2_coefficient_of_friction_calculator_base(
        self: "CastSelf",
    ) -> "ISO14179Part2CoefficientOfFrictionCalculatorBase":
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
class ISO14179Part2CoefficientOfFrictionCalculatorBase(
    _681.CoefficientOfFrictionCalculator
):
    """ISO14179Part2CoefficientOfFrictionCalculatorBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO14179_PART_2_COEFFICIENT_OF_FRICTION_CALCULATOR_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ISO14179Part2CoefficientOfFrictionCalculatorBase":
        """Cast to another type.

        Returns:
            _Cast_ISO14179Part2CoefficientOfFrictionCalculatorBase
        """
        return _Cast_ISO14179Part2CoefficientOfFrictionCalculatorBase(self)
