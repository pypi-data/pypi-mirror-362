"""MotorRotorSideFaceDetail"""

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

_MOTOR_ROTOR_SIDE_FACE_DETAIL = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "MotorRotorSideFaceDetail"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MotorRotorSideFaceDetail")
    CastSelf = TypeVar(
        "CastSelf", bound="MotorRotorSideFaceDetail._Cast_MotorRotorSideFaceDetail"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MotorRotorSideFaceDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MotorRotorSideFaceDetail:
    """Special nested class for casting MotorRotorSideFaceDetail to subclasses."""

    __parent__: "MotorRotorSideFaceDetail"

    @property
    def motor_rotor_side_face_detail(self: "CastSelf") -> "MotorRotorSideFaceDetail":
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
class MotorRotorSideFaceDetail(_0.APIBase):
    """MotorRotorSideFaceDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOTOR_ROTOR_SIDE_FACE_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_air_gap(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialAirGap")

        if temp is None:
            return 0.0

        return temp

    @axial_air_gap.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_air_gap(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AxialAirGap", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def inner_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerRadius")

        if temp is None:
            return 0.0

        return temp

    @inner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "InnerRadius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def outer_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterRadius")

        if temp is None:
            return 0.0

        return temp

    @outer_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterRadius", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MotorRotorSideFaceDetail":
        """Cast to another type.

        Returns:
            _Cast_MotorRotorSideFaceDetail
        """
        return _Cast_MotorRotorSideFaceDetail(self)
