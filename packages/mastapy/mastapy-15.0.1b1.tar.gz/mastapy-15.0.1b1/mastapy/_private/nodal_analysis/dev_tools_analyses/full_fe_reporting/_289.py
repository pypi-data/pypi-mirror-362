"""ContactPairReporting"""

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

_CONTACT_PAIR_REPORTING = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ContactPairReporting",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.fe_tools.vis_tools_global.vis_tools_global_enums import (
        _1356,
        _1357,
    )

    Self = TypeVar("Self", bound="ContactPairReporting")
    CastSelf = TypeVar(
        "CastSelf", bound="ContactPairReporting._Cast_ContactPairReporting"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ContactPairReporting",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ContactPairReporting:
    """Special nested class for casting ContactPairReporting to subclasses."""

    __parent__: "ContactPairReporting"

    @property
    def contact_pair_reporting(self: "CastSelf") -> "ContactPairReporting":
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
class ContactPairReporting(_0.APIBase):
    """ContactPairReporting

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONTACT_PAIR_REPORTING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def adjust_distance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AdjustDistance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @adjust_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def adjust_distance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AdjustDistance", value)

    @property
    @exception_bridge
    def constrained_surface_type(
        self: "Self",
    ) -> "_1356.ContactPairConstrainedSurfaceType":
        """mastapy.fe_tools.vis_tools_global.vis_tools_global_enums.ContactPairConstrainedSurfaceType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConstrainedSurfaceType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums.ContactPairConstrainedSurfaceType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.fe_tools.vis_tools_global.vis_tools_global_enums._1356",
            "ContactPairConstrainedSurfaceType",
        )(value)

    @property
    @exception_bridge
    def id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def position_tolerance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PositionTolerance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @position_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def position_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PositionTolerance", value)

    @property
    @exception_bridge
    def property_id(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PropertyID")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @property
    @exception_bridge
    def reference_surface_type(self: "Self") -> "_1357.ContactPairReferenceSurfaceType":
        """mastapy.fe_tools.vis_tools_global.vis_tools_global_enums.ContactPairReferenceSurfaceType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceSurfaceType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums.ContactPairReferenceSurfaceType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.fe_tools.vis_tools_global.vis_tools_global_enums._1357",
            "ContactPairReferenceSurfaceType",
        )(value)

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
    def swap_reference_and_constrained_surfaces(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SwapReferenceAndConstrainedSurfaces")

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
    def cast_to(self: "Self") -> "_Cast_ContactPairReporting":
        """Cast to another type.

        Returns:
            _Cast_ContactPairReporting
        """
        return _Cast_ContactPairReporting(self)
