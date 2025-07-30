"""ReadonlyToothThicknessSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1198

_READONLY_TOOTH_THICKNESS_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "ReadonlyToothThicknessSpecification"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical import _1199

    Self = TypeVar("Self", bound="ReadonlyToothThicknessSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ReadonlyToothThicknessSpecification._Cast_ReadonlyToothThicknessSpecification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ReadonlyToothThicknessSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ReadonlyToothThicknessSpecification:
    """Special nested class for casting ReadonlyToothThicknessSpecification to subclasses."""

    __parent__: "ReadonlyToothThicknessSpecification"

    @property
    def tooth_thickness_specification(
        self: "CastSelf",
    ) -> "_1198.ToothThicknessSpecification":
        return self.__parent__._cast(_1198.ToothThicknessSpecification)

    @property
    def tooth_thickness_specification_base(
        self: "CastSelf",
    ) -> "_1199.ToothThicknessSpecificationBase":
        from mastapy._private.gears.gear_designs.cylindrical import _1199

        return self.__parent__._cast(_1199.ToothThicknessSpecificationBase)

    @property
    def readonly_tooth_thickness_specification(
        self: "CastSelf",
    ) -> "ReadonlyToothThicknessSpecification":
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
class ReadonlyToothThicknessSpecification(_1198.ToothThicknessSpecification):
    """ReadonlyToothThicknessSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _READONLY_TOOTH_THICKNESS_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ball_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "BallDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @ball_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def ball_diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BallDiameter", value)

    @property
    @exception_bridge
    def diameter_at_thickness_measurement(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DiameterAtThicknessMeasurement")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter_at_thickness_measurement.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter_at_thickness_measurement(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DiameterAtThicknessMeasurement", value)

    @property
    @exception_bridge
    def number_of_teeth_for_chordal_span_test(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethForChordalSpanTest")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_teeth_for_chordal_span_test.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_teeth_for_chordal_span_test(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfTeethForChordalSpanTest", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ReadonlyToothThicknessSpecification":
        """Cast to another type.

        Returns:
            _Cast_ReadonlyToothThicknessSpecification
        """
        return _Cast_ReadonlyToothThicknessSpecification(self)
