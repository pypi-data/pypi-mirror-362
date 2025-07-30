"""CylindricalGearMeshMisalignmentValue"""

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

_CYLINDRICAL_GEAR_MESH_MISALIGNMENT_VALUE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting",
    "CylindricalGearMeshMisalignmentValue",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearMeshMisalignmentValue")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshMisalignmentValue._Cast_CylindricalGearMeshMisalignmentValue",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshMisalignmentValue",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshMisalignmentValue:
    """Special nested class for casting CylindricalGearMeshMisalignmentValue to subclasses."""

    __parent__: "CylindricalGearMeshMisalignmentValue"

    @property
    def cylindrical_gear_mesh_misalignment_value(
        self: "CastSelf",
    ) -> "CylindricalGearMeshMisalignmentValue":
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
class CylindricalGearMeshMisalignmentValue(_0.APIBase):
    """CylindricalGearMeshMisalignmentValue

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_MISALIGNMENT_VALUE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "GearName")

        if temp is None:
            return ""

        return temp

    @gear_name.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "GearName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def misalignment(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Misalignment")

        if temp is None:
            return 0.0

        return temp

    @misalignment.setter
    @exception_bridge
    @enforce_parameter_types
    def misalignment(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Misalignment", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def misalignment_due_to_tilt(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MisalignmentDueToTilt")

        if temp is None:
            return 0.0

        return temp

    @misalignment_due_to_tilt.setter
    @exception_bridge
    @enforce_parameter_types
    def misalignment_due_to_tilt(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MisalignmentDueToTilt",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def misalignment_due_to_twist(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MisalignmentDueToTwist")

        if temp is None:
            return 0.0

        return temp

    @misalignment_due_to_twist.setter
    @exception_bridge
    @enforce_parameter_types
    def misalignment_due_to_twist(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MisalignmentDueToTwist",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tilt_x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltX")

        if temp is None:
            return 0.0

        return temp

    @tilt_x.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltX", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tilt_y(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltY")

        if temp is None:
            return 0.0

        return temp

    @tilt_y.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_y(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltY", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshMisalignmentValue":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshMisalignmentValue
        """
        return _Cast_CylindricalGearMeshMisalignmentValue(self)
