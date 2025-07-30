"""ConicalGearBiasModification"""

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
from mastapy._private.gears.micro_geometry import _660

_CONICAL_GEAR_BIAS_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical.MicroGeometry",
    "ConicalGearBiasModification",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.micro_geometry import _670

    Self = TypeVar("Self", bound="ConicalGearBiasModification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearBiasModification._Cast_ConicalGearBiasModification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearBiasModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearBiasModification:
    """Special nested class for casting ConicalGearBiasModification to subclasses."""

    __parent__: "ConicalGearBiasModification"

    @property
    def bias_modification(self: "CastSelf") -> "_660.BiasModification":
        return self.__parent__._cast(_660.BiasModification)

    @property
    def modification(self: "CastSelf") -> "_670.Modification":
        from mastapy._private.gears.micro_geometry import _670

        return self.__parent__._cast(_670.Modification)

    @property
    def conical_gear_bias_modification(
        self: "CastSelf",
    ) -> "ConicalGearBiasModification":
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
class ConicalGearBiasModification(_660.BiasModification):
    """ConicalGearBiasModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_BIAS_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def constant_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConstantRelief")

        if temp is None:
            return 0.0

        return temp

    @constant_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def constant_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ConstantRelief", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearBiasModification":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearBiasModification
        """
        return _Cast_ConicalGearBiasModification(self)
