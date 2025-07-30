"""CycloidalAssemblyDesign"""

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

_CYCLOIDAL_ASSEMBLY_DESIGN = python_net_import(
    "SMT.MastaAPI.Cycloidal", "CycloidalAssemblyDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.cycloidal import _1639, _1646, _1647

    Self = TypeVar("Self", bound="CycloidalAssemblyDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="CycloidalAssemblyDesign._Cast_CycloidalAssemblyDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalAssemblyDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalAssemblyDesign:
    """Special nested class for casting CycloidalAssemblyDesign to subclasses."""

    __parent__: "CycloidalAssemblyDesign"

    @property
    def cycloidal_assembly_design(self: "CastSelf") -> "CycloidalAssemblyDesign":
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
class CycloidalAssemblyDesign(_0.APIBase):
    """CycloidalAssemblyDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_ASSEMBLY_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def eccentricity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Eccentricity")

        if temp is None:
            return 0.0

        return temp

    @eccentricity.setter
    @exception_bridge
    @enforce_parameter_types
    def eccentricity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Eccentricity", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def first_disc_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstDiscAngle")

        if temp is None:
            return 0.0

        return temp

    @first_disc_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def first_disc_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FirstDiscAngle", float(value) if value is not None else 0.0
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
    def number_of_lobes(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfLobes")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_lobes.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_lobes(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfLobes", value)

    @property
    @exception_bridge
    def ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Ratio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_symmetry_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothSymmetryAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ring_pins(self: "Self") -> "_1647.RingPinsDesign":
        """mastapy.cycloidal.RingPinsDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPins")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def disc_phases(self: "Self") -> "List[_1646.NamedDiscPhase]":
        """List[mastapy.cycloidal.NamedDiscPhase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiscPhases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def discs(self: "Self") -> "List[_1639.CycloidalDiscDesign]":
        """List[mastapy.cycloidal.CycloidalDiscDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Discs")

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
    def duplicate(self: "Self") -> "CycloidalAssemblyDesign":
        """mastapy.cycloidal.CycloidalAssemblyDesign"""
        method_result = pythonnet_method_call(self.wrapped, "Duplicate")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

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
    def cast_to(self: "Self") -> "_Cast_CycloidalAssemblyDesign":
        """Cast to another type.

        Returns:
            _Cast_CycloidalAssemblyDesign
        """
        return _Cast_CycloidalAssemblyDesign(self)
