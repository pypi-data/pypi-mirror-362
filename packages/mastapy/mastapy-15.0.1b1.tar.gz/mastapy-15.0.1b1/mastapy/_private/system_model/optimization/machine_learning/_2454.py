"""CylindricalGearFlankOptimisationParameter"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private.math_utility.optimisation import _1728

_CYLINDRICAL_GEAR_FLANK_OPTIMISATION_PARAMETER = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization.MachineLearning",
    "CylindricalGearFlankOptimisationParameter",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearFlankOptimisationParameter")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearFlankOptimisationParameter._Cast_CylindricalGearFlankOptimisationParameter",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFlankOptimisationParameter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFlankOptimisationParameter:
    """Special nested class for casting CylindricalGearFlankOptimisationParameter to subclasses."""

    __parent__: "CylindricalGearFlankOptimisationParameter"

    @property
    def optimization_property(self: "CastSelf") -> "_1728.OptimizationProperty":
        return self.__parent__._cast(_1728.OptimizationProperty)

    @property
    def cylindrical_gear_flank_optimisation_parameter(
        self: "CastSelf",
    ) -> "CylindricalGearFlankOptimisationParameter":
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
class CylindricalGearFlankOptimisationParameter(_1728.OptimizationProperty):
    """CylindricalGearFlankOptimisationParameter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FLANK_OPTIMISATION_PARAMETER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFlankOptimisationParameter":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFlankOptimisationParameter
        """
        return _Cast_CylindricalGearFlankOptimisationParameter(self)
