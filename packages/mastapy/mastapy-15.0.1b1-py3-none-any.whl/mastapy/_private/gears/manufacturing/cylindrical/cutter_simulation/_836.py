"""CylindricalGearSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CYLINDRICAL_GEAR_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "CylindricalGearSpecification",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1199

    Self = TypeVar("Self", bound="CylindricalGearSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSpecification._Cast_CylindricalGearSpecification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSpecification:
    """Special nested class for casting CylindricalGearSpecification to subclasses."""

    __parent__: "CylindricalGearSpecification"

    @property
    def cylindrical_gear_specification(
        self: "CastSelf",
    ) -> "CylindricalGearSpecification":
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
class CylindricalGearSpecification(_0.APIBase):
    """CylindricalGearSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def helix_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngle")

        if temp is None:
            return 0.0

        return temp

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
    def normal_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalModule")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_teeth_unsigned(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethUnsigned")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_thickness_specification(
        self: "Self",
    ) -> "_1199.ToothThicknessSpecificationBase":
        """mastapy.gears.gear_designs.cylindrical.ToothThicknessSpecificationBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothThicknessSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSpecification":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSpecification
        """
        return _Cast_CylindricalGearSpecification(self)
