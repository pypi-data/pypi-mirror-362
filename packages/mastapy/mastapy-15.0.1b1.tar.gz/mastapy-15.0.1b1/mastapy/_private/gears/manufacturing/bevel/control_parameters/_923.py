"""ConicalManufacturingSMTControlParameters"""

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

_CONICAL_MANUFACTURING_SMT_CONTROL_PARAMETERS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel.ControlParameters",
    "ConicalManufacturingSMTControlParameters",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalManufacturingSMTControlParameters")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalManufacturingSMTControlParameters._Cast_ConicalManufacturingSMTControlParameters",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalManufacturingSMTControlParameters",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalManufacturingSMTControlParameters:
    """Special nested class for casting ConicalManufacturingSMTControlParameters to subclasses."""

    __parent__: "ConicalManufacturingSMTControlParameters"

    @property
    def conical_gear_manufacturing_control_parameters(
        self: "CastSelf",
    ) -> "_920.ConicalGearManufacturingControlParameters":
        return self.__parent__._cast(_920.ConicalGearManufacturingControlParameters)

    @property
    def conical_manufacturing_smt_control_parameters(
        self: "CastSelf",
    ) -> "ConicalManufacturingSMTControlParameters":
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
class ConicalManufacturingSMTControlParameters(
    _920.ConicalGearManufacturingControlParameters
):
    """ConicalManufacturingSMTControlParameters

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MANUFACTURING_SMT_CONTROL_PARAMETERS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_acceleration(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngularAcceleration")

        if temp is None:
            return 0.0

        return temp

    @angular_acceleration.setter
    @exception_bridge
    @enforce_parameter_types
    def angular_acceleration(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AngularAcceleration",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def clearance_between_finish_root_and_rough_root(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ClearanceBetweenFinishRootAndRoughRoot"
        )

        if temp is None:
            return 0.0

        return temp

    @clearance_between_finish_root_and_rough_root.setter
    @exception_bridge
    @enforce_parameter_types
    def clearance_between_finish_root_and_rough_root(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ClearanceBetweenFinishRootAndRoughRoot",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def delta_e(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaE")

        if temp is None:
            return 0.0

        return temp

    @delta_e.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_e(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaE", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def delta_sigma(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaSigma")

        if temp is None:
            return 0.0

        return temp

    @delta_sigma.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_sigma(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaSigma", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def delta_xp(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaXP")

        if temp is None:
            return 0.0

        return temp

    @delta_xp.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_xp(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaXP", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def delta_xw(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaXW")

        if temp is None:
            return 0.0

        return temp

    @delta_xw.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_xw(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaXW", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def direction_angle_of_poc(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DirectionAngleOfPOC")

        if temp is None:
            return 0.0

        return temp

    @direction_angle_of_poc.setter
    @exception_bridge
    @enforce_parameter_types
    def direction_angle_of_poc(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DirectionAngleOfPOC",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def initial_workhead_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InitialWorkheadOffset")

        if temp is None:
            return 0.0

        return temp

    @initial_workhead_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def initial_workhead_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InitialWorkheadOffset",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mean_contact_point_h(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanContactPointH")

        if temp is None:
            return 0.0

        return temp

    @mean_contact_point_h.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_contact_point_h(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeanContactPointH",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mean_contact_point_v(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanContactPointV")

        if temp is None:
            return 0.0

        return temp

    @mean_contact_point_v.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_contact_point_v(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeanContactPointV",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalManufacturingSMTControlParameters":
        """Cast to another type.

        Returns:
            _Cast_ConicalManufacturingSMTControlParameters
        """
        return _Cast_ConicalManufacturingSMTControlParameters(self)
