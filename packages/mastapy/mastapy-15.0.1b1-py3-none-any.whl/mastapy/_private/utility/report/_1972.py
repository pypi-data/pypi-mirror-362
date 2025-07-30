"""CustomReportText"""

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
from mastapy._private.utility.report import _1955

_CUSTOM_REPORT_TEXT = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportText"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.html import _393
    from mastapy._private.utility.report import _1958, _1966

    Self = TypeVar("Self", bound="CustomReportText")
    CastSelf = TypeVar("CastSelf", bound="CustomReportText._Cast_CustomReportText")


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportText",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportText:
    """Special nested class for casting CustomReportText to subclasses."""

    __parent__: "CustomReportText"

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1955.CustomReportDefinitionItem":
        return self.__parent__._cast(_1955.CustomReportDefinitionItem)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1966.CustomReportNameableItem":
        from mastapy._private.utility.report import _1966

        return self.__parent__._cast(_1966.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def custom_report_text(self: "CastSelf") -> "CustomReportText":
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
class CustomReportText(_1955.CustomReportDefinitionItem):
    """CustomReportText

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_TEXT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bold(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Bold")

        if temp is None:
            return False

        return temp

    @bold.setter
    @exception_bridge
    @enforce_parameter_types
    def bold(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Bold", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def cad_text_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CADTextSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cad_text_size.setter
    @exception_bridge
    @enforce_parameter_types
    def cad_text_size(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CADTextSize", value)

    @property
    @exception_bridge
    def heading_type(self: "Self") -> "_393.HeadingType":
        """mastapy.html.HeadingType"""
        temp = pythonnet_property_get(self.wrapped, "HeadingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.HTML.HeadingType")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.html._393", "HeadingType"
        )(value)

    @heading_type.setter
    @exception_bridge
    @enforce_parameter_types
    def heading_type(self: "Self", value: "_393.HeadingType") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.HTML.HeadingType")
        pythonnet_property_set(self.wrapped, "HeadingType", value)

    @property
    @exception_bridge
    def is_heading(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsHeading")

        if temp is None:
            return False

        return temp

    @is_heading.setter
    @exception_bridge
    @enforce_parameter_types
    def is_heading(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsHeading", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_symbol(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowSymbol")

        if temp is None:
            return False

        return temp

    @show_symbol.setter
    @exception_bridge
    @enforce_parameter_types
    def show_symbol(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowSymbol", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_unit(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowUnit")

        if temp is None:
            return False

        return temp

    @show_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def show_unit(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowUnit", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def text(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Text")

        if temp is None:
            return ""

        return temp

    @text.setter
    @exception_bridge
    @enforce_parameter_types
    def text(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Text", str(value) if value is not None else ""
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportText":
        """Cast to another type.

        Returns:
            _Cast_CustomReportText
        """
        return _Cast_CustomReportText(self)
