"""ToothThicknessSpecificationBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
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
from mastapy._private.utility.units_and_measurements.measurements import _1860, _1881

_TOOTH_THICKNESS_SPECIFICATION_BASE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "ToothThicknessSpecificationBase"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical import (
        _1146,
        _1156,
        _1178,
        _1198,
    )

    Self = TypeVar("Self", bound="ToothThicknessSpecificationBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothThicknessSpecificationBase._Cast_ToothThicknessSpecificationBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothThicknessSpecificationBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothThicknessSpecificationBase:
    """Special nested class for casting ToothThicknessSpecificationBase to subclasses."""

    __parent__: "ToothThicknessSpecificationBase"

    @property
    def finish_tooth_thickness_design_specification(
        self: "CastSelf",
    ) -> "_1156.FinishToothThicknessDesignSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1156

        return self.__parent__._cast(_1156.FinishToothThicknessDesignSpecification)

    @property
    def readonly_tooth_thickness_specification(
        self: "CastSelf",
    ) -> "_1178.ReadonlyToothThicknessSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1178

        return self.__parent__._cast(_1178.ReadonlyToothThicknessSpecification)

    @property
    def tooth_thickness_specification(
        self: "CastSelf",
    ) -> "_1198.ToothThicknessSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1198

        return self.__parent__._cast(_1198.ToothThicknessSpecification)

    @property
    def tooth_thickness_specification_base(
        self: "CastSelf",
    ) -> "ToothThicknessSpecificationBase":
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
class ToothThicknessSpecificationBase(_0.APIBase):
    """ToothThicknessSpecificationBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_THICKNESS_SPECIFICATION_BASE

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
    def ball_diameter_at_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BallDiameterAtFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ball_diameter_at_tip_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BallDiameterAtTipFormDiameter")

        if temp is None:
            return 0.0

        return temp

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
    def maximum_number_of_teeth_for_chordal_span_test(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNumberOfTeethForChordalSpanTest"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def minimum_diameter_of_circle_in_transverse_plane_containing_centres_of_balls_pins(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MinimumDiameterOfCircleInTransversePlaneContainingCentresOfBallsPins",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_number_of_teeth_for_chordal_span_test(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumNumberOfTeethForChordalSpanTest"
        )

        if temp is None:
            return 0

        return temp

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
    @exception_bridge
    def chordal_span(
        self: "Self",
    ) -> "_1146.CylindricalGearToothThicknessSpecification[_1860.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChordalSpan")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1860.LengthShort](temp)

    @property
    @exception_bridge
    def normal_thickness(
        self: "Self",
    ) -> "_1146.CylindricalGearToothThicknessSpecification[_1860.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalThickness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1860.LengthShort](temp)

    @property
    @exception_bridge
    def normal_thickness_at_specified_diameter(
        self: "Self",
    ) -> "_1146.CylindricalGearToothThicknessSpecification[_1860.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalThicknessAtSpecifiedDiameter"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1860.LengthShort](temp)

    @property
    @exception_bridge
    def over_balls(
        self: "Self",
    ) -> "_1146.CylindricalGearToothThicknessSpecification[_1860.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverBalls")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1860.LengthShort](temp)

    @property
    @exception_bridge
    def over_two_pins_free_pin_method(
        self: "Self",
    ) -> "_1146.CylindricalGearToothThicknessSpecification[_1860.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverTwoPinsFreePinMethod")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1860.LengthShort](temp)

    @property
    @exception_bridge
    def over_two_pins_transverse_method(
        self: "Self",
    ) -> "_1146.CylindricalGearToothThicknessSpecification[_1860.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverTwoPinsTransverseMethod")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1860.LengthShort](temp)

    @property
    @exception_bridge
    def profile_shift(
        self: "Self",
    ) -> "_1146.CylindricalGearToothThicknessSpecification[_1860.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileShift")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1860.LengthShort](temp)

    @property
    @exception_bridge
    def profile_shift_coefficient(
        self: "Self",
    ) -> "_1146.CylindricalGearToothThicknessSpecification[_1881.Number]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.Number]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileShiftCoefficient")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1881.Number](temp)

    @property
    @exception_bridge
    def transverse_thickness(
        self: "Self",
    ) -> "_1146.CylindricalGearToothThicknessSpecification[_1860.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseThickness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1860.LengthShort](temp)

    @property
    @exception_bridge
    def transverse_thickness_at_specified_diameter(
        self: "Self",
    ) -> "_1146.CylindricalGearToothThicknessSpecification[_1860.LengthShort]":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseThicknessAtSpecifiedDiameter"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1860.LengthShort](temp)

    @property
    @exception_bridge
    def tooth_thickness(
        self: "Self",
    ) -> "List[_1146.CylindricalGearToothThicknessSpecification[_1860.LengthShort]]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearToothThicknessSpecification[mastapy.utility.units_and_measurements.measurements.LengthShort]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothThickness")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ToothThicknessSpecificationBase":
        """Cast to another type.

        Returns:
            _Cast_ToothThicknessSpecificationBase
        """
        return _Cast_ToothThicknessSpecificationBase(self)
