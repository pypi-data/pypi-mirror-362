"""PlasticSNCurveForTheSpecifiedOperatingConditions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.materials import _706

_PLASTIC_SN_CURVE_FOR_THE_SPECIFIED_OPERATING_CONDITIONS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.PlasticVDI2736",
    "PlasticSNCurveForTheSpecifiedOperatingConditions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials import _378

    Self = TypeVar("Self", bound="PlasticSNCurveForTheSpecifiedOperatingConditions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlasticSNCurveForTheSpecifiedOperatingConditions._Cast_PlasticSNCurveForTheSpecifiedOperatingConditions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlasticSNCurveForTheSpecifiedOperatingConditions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlasticSNCurveForTheSpecifiedOperatingConditions:
    """Special nested class for casting PlasticSNCurveForTheSpecifiedOperatingConditions to subclasses."""

    __parent__: "PlasticSNCurveForTheSpecifiedOperatingConditions"

    @property
    def plastic_sn_curve(self: "CastSelf") -> "_706.PlasticSNCurve":
        return self.__parent__._cast(_706.PlasticSNCurve)

    @property
    def plastic_sn_curve_for_the_specified_operating_conditions(
        self: "CastSelf",
    ) -> "PlasticSNCurveForTheSpecifiedOperatingConditions":
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
class PlasticSNCurveForTheSpecifiedOperatingConditions(_706.PlasticSNCurve):
    """PlasticSNCurveForTheSpecifiedOperatingConditions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLASTIC_SN_CURVE_FOR_THE_SPECIFIED_OPERATING_CONDITIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def flank_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FlankTemperature")

        if temp is None:
            return 0.0

        return temp

    @flank_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def flank_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FlankTemperature", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def life_cycles(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LifeCycles")

        if temp is None:
            return 0.0

        return temp

    @life_cycles.setter
    @exception_bridge
    @enforce_parameter_types
    def life_cycles(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LifeCycles", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def lubricant(self: "Self") -> "_378.VDI2736LubricantType":
        """mastapy.materials.VDI2736LubricantType"""
        temp = pythonnet_property_get(self.wrapped, "Lubricant")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.VDI2736LubricantType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._378", "VDI2736LubricantType"
        )(value)

    @lubricant.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant(self: "Self", value: "_378.VDI2736LubricantType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.VDI2736LubricantType"
        )
        pythonnet_property_set(self.wrapped, "Lubricant", value)

    @property
    @exception_bridge
    def root_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RootTemperature")

        if temp is None:
            return 0.0

        return temp

    @root_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def root_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RootTemperature", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_PlasticSNCurveForTheSpecifiedOperatingConditions":
        """Cast to another type.

        Returns:
            _Cast_PlasticSNCurveForTheSpecifiedOperatingConditions
        """
        return _Cast_PlasticSNCurveForTheSpecifiedOperatingConditions(self)
