"""FaceGearWheelDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.gears.gear_designs.face import _1093

_FACE_GEAR_WHEEL_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Face", "FaceGearWheelDesign"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs import _1051, _1052
    from mastapy._private.gears.gear_designs.face import _1094

    Self = TypeVar("Self", bound="FaceGearWheelDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="FaceGearWheelDesign._Cast_FaceGearWheelDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearWheelDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearWheelDesign:
    """Special nested class for casting FaceGearWheelDesign to subclasses."""

    __parent__: "FaceGearWheelDesign"

    @property
    def face_gear_design(self: "CastSelf") -> "_1093.FaceGearDesign":
        return self.__parent__._cast(_1093.FaceGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "_1051.GearDesign":
        from mastapy._private.gears.gear_designs import _1051

        return self.__parent__._cast(_1051.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def face_gear_wheel_design(self: "CastSelf") -> "FaceGearWheelDesign":
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
class FaceGearWheelDesign(_1093.FaceGearDesign):
    """FaceGearWheelDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_WHEEL_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def addendum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Addendum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @addendum.setter
    @exception_bridge
    @enforce_parameter_types
    def addendum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Addendum", value)

    @property
    @exception_bridge
    def addendum_from_pitch_line_at_inner_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AddendumFromPitchLineAtInnerEnd")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def addendum_from_pitch_line_at_mid_face(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AddendumFromPitchLineAtMidFace")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def addendum_from_pitch_line_at_outer_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AddendumFromPitchLineAtOuterEnd")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dedendum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Dedendum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dedendum.setter
    @exception_bridge
    @enforce_parameter_types
    def dedendum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Dedendum", value)

    @property
    @exception_bridge
    def dedendum_from_pitch_line_at_inner_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DedendumFromPitchLineAtInnerEnd")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dedendum_from_pitch_line_at_mid_face(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DedendumFromPitchLineAtMidFace")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dedendum_from_pitch_line_at_outer_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DedendumFromPitchLineAtOuterEnd")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_width_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidthOffset")

        if temp is None:
            return 0.0

        return temp

    @face_width_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidthOffset", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def face_width_and_diameters_specification_method(
        self: "Self",
    ) -> "_1094.FaceGearDiameterFaceWidthSpecificationMethod":
        """mastapy.gears.gear_designs.face.FaceGearDiameterFaceWidthSpecificationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "FaceWidthAndDiametersSpecificationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Face.FaceGearDiameterFaceWidthSpecificationMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.face._1094",
            "FaceGearDiameterFaceWidthSpecificationMethod",
        )(value)

    @face_width_and_diameters_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width_and_diameters_specification_method(
        self: "Self", value: "_1094.FaceGearDiameterFaceWidthSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Face.FaceGearDiameterFaceWidthSpecificationMethod",
        )
        pythonnet_property_set(
            self.wrapped, "FaceWidthAndDiametersSpecificationMethod", value
        )

    @property
    @exception_bridge
    def fillet_radius_at_reference_section(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FilletRadiusAtReferenceSection")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @fillet_radius_at_reference_section.setter
    @exception_bridge
    @enforce_parameter_types
    def fillet_radius_at_reference_section(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FilletRadiusAtReferenceSection", value)

    @property
    @exception_bridge
    def inner_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @inner_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "InnerDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def mean_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_pitch_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanPitchRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pressure_angle_at_inner_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngleAtInnerEnd")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pressure_angle_at_mid_face(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngleAtMidFace")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pressure_angle_at_outer_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngleAtOuterEnd")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_thickness_at_reference_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalThicknessAtReferenceSection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def profile_shift_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileShiftCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius_at_inner_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadiusAtInnerEnd")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius_at_mid_face(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadiusAtMidFace")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius_at_outer_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadiusAtOuterEnd")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reference_pitch_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferencePitchRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rim_thickness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RimThickness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rim_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def rim_thickness(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RimThickness", value)

    @property
    @exception_bridge
    def whole_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WholeDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearWheelDesign":
        """Cast to another type.

        Returns:
            _Cast_FaceGearWheelDesign
        """
        return _Cast_FaceGearWheelDesign(self)
