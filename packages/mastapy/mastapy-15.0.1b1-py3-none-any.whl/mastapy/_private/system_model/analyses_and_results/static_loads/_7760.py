"""GearManufactureError"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEAR_MANUFACTURE_ERROR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearManufactureError"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7714,
        _7731,
    )

    Self = TypeVar("Self", bound="GearManufactureError")
    CastSelf = TypeVar(
        "CastSelf", bound="GearManufactureError._Cast_GearManufactureError"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearManufactureError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearManufactureError:
    """Special nested class for casting GearManufactureError to subclasses."""

    __parent__: "GearManufactureError"

    @property
    def conical_gear_manufacture_error(
        self: "CastSelf",
    ) -> "_7714.ConicalGearManufactureError":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7714,
        )

        return self.__parent__._cast(_7714.ConicalGearManufactureError)

    @property
    def cylindrical_gear_manufacture_error(
        self: "CastSelf",
    ) -> "_7731.CylindricalGearManufactureError":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7731,
        )

        return self.__parent__._cast(_7731.CylindricalGearManufactureError)

    @property
    def gear_manufacture_error(self: "CastSelf") -> "GearManufactureError":
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
class GearManufactureError(_0.APIBase):
    """GearManufactureError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MANUFACTURE_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def use_custom_pitch_errors(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseCustomPitchErrors")

        if temp is None:
            return False

        return temp

    @use_custom_pitch_errors.setter
    @exception_bridge
    @enforce_parameter_types
    def use_custom_pitch_errors(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseCustomPitchErrors",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearManufactureError":
        """Cast to another type.

        Returns:
            _Cast_GearManufactureError
        """
        return _Cast_GearManufactureError(self)
