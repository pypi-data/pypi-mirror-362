"""SplinePitchErrorOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
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
from mastapy._private.system_model.part_model.couplings import _2844

_SPLINE_PITCH_ERROR_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SplinePitchErrorOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.part_model.couplings import _2830

    Self = TypeVar("Self", bound="SplinePitchErrorOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="SplinePitchErrorOptions._Cast_SplinePitchErrorOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SplinePitchErrorOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SplinePitchErrorOptions:
    """Special nested class for casting SplinePitchErrorOptions to subclasses."""

    __parent__: "SplinePitchErrorOptions"

    @property
    def spline_pitch_error_options(self: "CastSelf") -> "SplinePitchErrorOptions":
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
class SplinePitchErrorOptions(_0.APIBase):
    """SplinePitchErrorOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPLINE_PITCH_ERROR_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def pitch_error_input_type(
        self: "Self",
    ) -> "overridable.Overridable_SplinePitchErrorInputType":
        """Overridable[mastapy.system_model.part_model.couplings.SplinePitchErrorInputType]"""
        temp = pythonnet_property_get(self.wrapped, "PitchErrorInputType")

        if temp is None:
            return None

        value = overridable.Overridable_SplinePitchErrorInputType.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @pitch_error_input_type.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_error_input_type(
        self: "Self",
        value: "Union[_2844.SplinePitchErrorInputType, Tuple[_2844.SplinePitchErrorInputType, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_SplinePitchErrorInputType.wrapper_type()
        enclosed_type = (
            overridable.Overridable_SplinePitchErrorInputType.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PitchErrorInputType", value)

    @property
    @exception_bridge
    def pitch_error_options_left_flank(self: "Self") -> "_2830.PitchErrorFlankOptions":
        """mastapy.system_model.part_model.couplings.PitchErrorFlankOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchErrorOptionsLeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pitch_error_options_right_flank(self: "Self") -> "_2830.PitchErrorFlankOptions":
        """mastapy.system_model.part_model.couplings.PitchErrorFlankOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchErrorOptionsRightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pitch_error_flank_options(self: "Self") -> "List[_2830.PitchErrorFlankOptions]":
        """List[mastapy.system_model.part_model.couplings.PitchErrorFlankOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchErrorFlankOptions")

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
    def cast_to(self: "Self") -> "_Cast_SplinePitchErrorOptions":
        """Cast to another type.

        Returns:
            _Cast_SplinePitchErrorOptions
        """
        return _Cast_SplinePitchErrorOptions(self)
