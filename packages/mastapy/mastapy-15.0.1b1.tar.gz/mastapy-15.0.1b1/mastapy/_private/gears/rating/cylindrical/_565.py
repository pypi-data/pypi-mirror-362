"""ISOScuffingResultsRow"""

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
from mastapy._private.gears.rating.cylindrical import _575

_ISO_SCUFFING_RESULTS_ROW = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "ISOScuffingResultsRow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ISOScuffingResultsRow")
    CastSelf = TypeVar(
        "CastSelf", bound="ISOScuffingResultsRow._Cast_ISOScuffingResultsRow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISOScuffingResultsRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISOScuffingResultsRow:
    """Special nested class for casting ISOScuffingResultsRow to subclasses."""

    __parent__: "ISOScuffingResultsRow"

    @property
    def scuffing_results_row(self: "CastSelf") -> "_575.ScuffingResultsRow":
        return self.__parent__._cast(_575.ScuffingResultsRow)

    @property
    def iso_scuffing_results_row(self: "CastSelf") -> "ISOScuffingResultsRow":
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
class ISOScuffingResultsRow(_575.ScuffingResultsRow):
    """ISOScuffingResultsRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO_SCUFFING_RESULTS_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def approach_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ApproachFactor")

        if temp is None:
            return 0.0

        return temp

    @approach_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def approach_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ApproachFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def contact_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactTemperature")

        if temp is None:
            return 0.0

        return temp

    @contact_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ContactTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def flash_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @flash_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def flash_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FlashTemperature", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def geometry_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GeometryFactor")

        if temp is None:
            return 0.0

        return temp

    @geometry_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def geometry_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "GeometryFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def pinion_rolling_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionRollingVelocity")

        if temp is None:
            return 0.0

        return temp

    @pinion_rolling_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def pinion_rolling_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinionRollingVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def sliding_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocity")

        if temp is None:
            return 0.0

        return temp

    @sliding_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def sliding_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SlidingVelocity", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def thermo_elastic_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ThermoElasticFactor")

        if temp is None:
            return 0.0

        return temp

    @thermo_elastic_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def thermo_elastic_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ThermoElasticFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def wheel_rolling_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelRollingVelocity")

        if temp is None:
            return 0.0

        return temp

    @wheel_rolling_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_rolling_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelRollingVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ISOScuffingResultsRow":
        """Cast to another type.

        Returns:
            _Cast_ISOScuffingResultsRow
        """
        return _Cast_ISOScuffingResultsRow(self)
