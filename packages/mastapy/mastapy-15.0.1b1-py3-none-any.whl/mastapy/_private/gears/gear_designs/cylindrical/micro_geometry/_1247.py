"""SingleCylindricalGearTriangularEndModification"""

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
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_SINGLE_CYLINDRICAL_GEAR_TRIANGULAR_END_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "SingleCylindricalGearTriangularEndModification",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs.cylindrical import _1135
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1232,
        _1240,
    )

    Self = TypeVar("Self", bound="SingleCylindricalGearTriangularEndModification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SingleCylindricalGearTriangularEndModification._Cast_SingleCylindricalGearTriangularEndModification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SingleCylindricalGearTriangularEndModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SingleCylindricalGearTriangularEndModification:
    """Special nested class for casting SingleCylindricalGearTriangularEndModification to subclasses."""

    __parent__: "SingleCylindricalGearTriangularEndModification"

    @property
    def linear_cylindrical_gear_triangular_end_modification(
        self: "CastSelf",
    ) -> "_1232.LinearCylindricalGearTriangularEndModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1232

        return self.__parent__._cast(
            _1232.LinearCylindricalGearTriangularEndModification
        )

    @property
    def parabolic_cylindrical_gear_triangular_end_modification(
        self: "CastSelf",
    ) -> "_1240.ParabolicCylindricalGearTriangularEndModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1240

        return self.__parent__._cast(
            _1240.ParabolicCylindricalGearTriangularEndModification
        )

    @property
    def single_cylindrical_gear_triangular_end_modification(
        self: "CastSelf",
    ) -> "SingleCylindricalGearTriangularEndModification":
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
class SingleCylindricalGearTriangularEndModification(_0.APIBase):
    """SingleCylindricalGearTriangularEndModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SINGLE_CYLINDRICAL_GEAR_TRIANGULAR_END_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Angle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @angle.setter
    @exception_bridge
    @enforce_parameter_types
    def angle(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Angle", value)

    @property
    @exception_bridge
    def face_width_position(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidthPosition")

        if temp is None:
            return 0.0

        return temp

    @face_width_position.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width_position(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FaceWidthPosition",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def face_width_position_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidthPositionFactor")

        if temp is None:
            return 0.0

        return temp

    @face_width_position_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width_position_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FaceWidthPositionFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationDiameter")

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationFactor")

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationRadius")

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationRollAngle")

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationRollDistance")

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_roll_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_start_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileStartDiameter")

        if temp is None:
            return 0.0

        return temp

    @profile_start_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_start_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileStartDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_start_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileStartFactor")

        if temp is None:
            return 0.0

        return temp

    @profile_start_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_start_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileStartFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_start_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileStartRadius")

        if temp is None:
            return 0.0

        return temp

    @profile_start_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_start_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileStartRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_start_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileStartRollAngle")

        if temp is None:
            return 0.0

        return temp

    @profile_start_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_start_roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileStartRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_start_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileStartRollDistance")

        if temp is None:
            return 0.0

        return temp

    @profile_start_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_start_roll_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileStartRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Relief")

        if temp is None:
            return 0.0

        return temp

    @relief.setter
    @exception_bridge
    @enforce_parameter_types
    def relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Relief", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def profile_evaluation(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def profile_start(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileStart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_SingleCylindricalGearTriangularEndModification":
        """Cast to another type.

        Returns:
            _Cast_SingleCylindricalGearTriangularEndModification
        """
        return _Cast_SingleCylindricalGearTriangularEndModification(self)
