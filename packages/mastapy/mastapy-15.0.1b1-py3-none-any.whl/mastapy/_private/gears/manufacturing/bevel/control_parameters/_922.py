"""ConicalManufacturingSGTControlParameters"""

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
from mastapy._private.gears.manufacturing.bevel.control_parameters import _920

_CONICAL_MANUFACTURING_SGT_CONTROL_PARAMETERS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel.ControlParameters",
    "ConicalManufacturingSGTControlParameters",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalManufacturingSGTControlParameters")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalManufacturingSGTControlParameters._Cast_ConicalManufacturingSGTControlParameters",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalManufacturingSGTControlParameters",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalManufacturingSGTControlParameters:
    """Special nested class for casting ConicalManufacturingSGTControlParameters to subclasses."""

    __parent__: "ConicalManufacturingSGTControlParameters"

    @property
    def conical_gear_manufacturing_control_parameters(
        self: "CastSelf",
    ) -> "_920.ConicalGearManufacturingControlParameters":
        return self.__parent__._cast(_920.ConicalGearManufacturingControlParameters)

    @property
    def conical_manufacturing_sgt_control_parameters(
        self: "CastSelf",
    ) -> "ConicalManufacturingSGTControlParameters":
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
class ConicalManufacturingSGTControlParameters(
    _920.ConicalGearManufacturingControlParameters
):
    """ConicalManufacturingSGTControlParameters

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MANUFACTURING_SGT_CONTROL_PARAMETERS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def delta_ax(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaAX")

        if temp is None:
            return 0.0

        return temp

    @delta_ax.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_ax(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaAX", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def delta_gamma_m(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaGammaM")

        if temp is None:
            return 0.0

        return temp

    @delta_gamma_m.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_gamma_m(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaGammaM", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def delta_gamma_x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaGammaX")

        if temp is None:
            return 0.0

        return temp

    @delta_gamma_x.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_gamma_x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaGammaX", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def root_angle_of_the_pinion(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RootAngleOfThePinion")

        if temp is None:
            return 0.0

        return temp

    @root_angle_of_the_pinion.setter
    @exception_bridge
    @enforce_parameter_types
    def root_angle_of_the_pinion(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RootAngleOfThePinion",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalManufacturingSGTControlParameters":
        """Cast to another type.

        Returns:
            _Cast_ConicalManufacturingSGTControlParameters
        """
        return _Cast_ConicalManufacturingSGTControlParameters(self)
