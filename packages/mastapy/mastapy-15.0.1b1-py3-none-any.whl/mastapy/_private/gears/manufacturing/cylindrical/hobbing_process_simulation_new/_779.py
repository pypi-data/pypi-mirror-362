"""HobManufactureError"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _792,
)

_HOB_MANUFACTURE_ERROR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "HobManufactureError",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HobManufactureError")
    CastSelf = TypeVar(
        "CastSelf", bound="HobManufactureError._Cast_HobManufactureError"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HobManufactureError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HobManufactureError:
    """Special nested class for casting HobManufactureError to subclasses."""

    __parent__: "HobManufactureError"

    @property
    def rack_manufacture_error(self: "CastSelf") -> "_792.RackManufactureError":
        return self.__parent__._cast(_792.RackManufactureError)

    @property
    def hob_manufacture_error(self: "CastSelf") -> "HobManufactureError":
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
class HobManufactureError(_792.RackManufactureError):
    """HobManufactureError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HOB_MANUFACTURE_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def total_relief_variation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TotalReliefVariation")

        if temp is None:
            return 0.0

        return temp

    @total_relief_variation.setter
    @exception_bridge
    @enforce_parameter_types
    def total_relief_variation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TotalReliefVariation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_sin_curve_for_top_relief(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSinCurveForTopRelief")

        if temp is None:
            return False

        return temp

    @use_sin_curve_for_top_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def use_sin_curve_for_top_relief(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSinCurveForTopRelief",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_HobManufactureError":
        """Cast to another type.

        Returns:
            _Cast_HobManufactureError
        """
        return _Cast_HobManufactureError(self)
