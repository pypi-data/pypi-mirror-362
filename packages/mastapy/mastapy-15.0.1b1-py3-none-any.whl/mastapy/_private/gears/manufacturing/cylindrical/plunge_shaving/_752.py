"""PlungeShaverGeneration"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_PLUNGE_SHAVER_GENERATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving",
    "PlungeShaverGeneration",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs.cylindrical import _1108
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import (
        _745,
        _759,
    )

    Self = TypeVar("Self", bound="PlungeShaverGeneration")
    CastSelf = TypeVar(
        "CastSelf", bound="PlungeShaverGeneration._Cast_PlungeShaverGeneration"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlungeShaverGeneration",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlungeShaverGeneration:
    """Special nested class for casting PlungeShaverGeneration to subclasses."""

    __parent__: "PlungeShaverGeneration"

    @property
    def plunge_shaver_generation(self: "CastSelf") -> "PlungeShaverGeneration":
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
class PlungeShaverGeneration(_0.APIBase):
    """PlungeShaverGeneration

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLUNGE_SHAVER_GENERATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def calculated_conjugate_face_width(self: "Self") -> "Tuple[float, float]":
        """Tuple[float, float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedConjugateFaceWidth")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_start_of_active_profile_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearStartOfActiveProfileDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def manufactured_end_of_active_profile_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ManufacturedEndOfActiveProfileDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def manufactured_start_of_active_profile_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ManufacturedStartOfActiveProfileDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaft_angle_unsigned(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftAngleUnsigned")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def crossed_axis_calculation_details(
        self: "Self",
    ) -> "_1108.CrossedAxisCylindricalGearPairLineContact":
        """mastapy.gears.gear_designs.cylindrical.CrossedAxisCylindricalGearPairLineContact

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrossedAxisCalculationDetails")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def calculation_errors(self: "Self") -> "List[_745.CalculationError]":
        """List[mastapy.gears.manufacturing.cylindrical.plunge_shaving.CalculationError]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculationErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def points_of_interest_on_the_shaver(
        self: "Self",
    ) -> "List[_759.ShaverPointOfInterest]":
        """List[mastapy.gears.manufacturing.cylindrical.plunge_shaving.ShaverPointOfInterest]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointsOfInterestOnTheShaver")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def cast_to(self: "Self") -> "_Cast_PlungeShaverGeneration":
        """Cast to another type.

        Returns:
            _Cast_PlungeShaverGeneration
        """
        return _Cast_PlungeShaverGeneration(self)
