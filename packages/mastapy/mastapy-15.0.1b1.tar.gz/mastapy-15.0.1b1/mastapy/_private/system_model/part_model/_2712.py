"""WindTurbineBladeModeDetails"""

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

_WIND_TURBINE_BLADE_MODE_DETAILS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "WindTurbineBladeModeDetails"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WindTurbineBladeModeDetails")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WindTurbineBladeModeDetails._Cast_WindTurbineBladeModeDetails",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WindTurbineBladeModeDetails",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WindTurbineBladeModeDetails:
    """Special nested class for casting WindTurbineBladeModeDetails to subclasses."""

    __parent__: "WindTurbineBladeModeDetails"

    @property
    def wind_turbine_blade_mode_details(
        self: "CastSelf",
    ) -> "WindTurbineBladeModeDetails":
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
class WindTurbineBladeModeDetails(_0.APIBase):
    """WindTurbineBladeModeDetails

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WIND_TURBINE_BLADE_MODE_DETAILS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def first_mode_frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstModeFrequency")

        if temp is None:
            return 0.0

        return temp

    @first_mode_frequency.setter
    @exception_bridge
    @enforce_parameter_types
    def first_mode_frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FirstModeFrequency",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def include_mode(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeMode")

        if temp is None:
            return False

        return temp

    @include_mode.setter
    @exception_bridge
    @enforce_parameter_types
    def include_mode(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IncludeMode", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def inertia_of_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InertiaOfCentre")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inertia_of_hub(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InertiaOfHub")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inertia_of_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InertiaOfTip")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def second_mode_frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SecondModeFrequency")

        if temp is None:
            return 0.0

        return temp

    @second_mode_frequency.setter
    @exception_bridge
    @enforce_parameter_types
    def second_mode_frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SecondModeFrequency",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def stiffness_centre_to_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessCentreToTip")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_hub_to_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessHubToCentre")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_WindTurbineBladeModeDetails":
        """Cast to another type.

        Returns:
            _Cast_WindTurbineBladeModeDetails
        """
        return _Cast_WindTurbineBladeModeDetails(self)
