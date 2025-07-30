"""GearMeshingElementOptions"""

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

_GEAR_MESHING_ELEMENT_OPTIONS = python_net_import(
    "SMT.MastaAPI.Gears.FEModel", "GearMeshingElementOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="GearMeshingElementOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshingElementOptions._Cast_GearMeshingElementOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshingElementOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshingElementOptions:
    """Special nested class for casting GearMeshingElementOptions to subclasses."""

    __parent__: "GearMeshingElementOptions"

    @property
    def gear_meshing_element_options(self: "CastSelf") -> "GearMeshingElementOptions":
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
class GearMeshingElementOptions(_0.APIBase):
    """GearMeshingElementOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESHING_ELEMENT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def body_elements(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "BodyElements")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @body_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def body_elements(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BodyElements", value)

    @property
    @exception_bridge
    def face_elements(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "FaceElements")

        if temp is None:
            return 0

        return temp

    @face_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def face_elements(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceElements", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def fillet_elements(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "FilletElements")

        if temp is None:
            return 0

        return temp

    @fillet_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def fillet_elements(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "FilletElements", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def profile_elements(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ProfileElements")

        if temp is None:
            return 0

        return temp

    @profile_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_elements(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ProfileElements", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def radial_elements(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "RadialElements")

        if temp is None:
            return 0

        return temp

    @radial_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_elements(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialElements", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def rim_elements(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "RimElements")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @rim_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def rim_elements(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RimElements", value)

    @property
    @exception_bridge
    def tip_elements(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "TipElements")

        if temp is None:
            return 0

        return temp

    @tip_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def tip_elements(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "TipElements", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def web_elements(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "WebElements")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @web_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def web_elements(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "WebElements", value)

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
    def cast_to(self: "Self") -> "_Cast_GearMeshingElementOptions":
        """Cast to another type.

        Returns:
            _Cast_GearMeshingElementOptions
        """
        return _Cast_GearMeshingElementOptions(self)
