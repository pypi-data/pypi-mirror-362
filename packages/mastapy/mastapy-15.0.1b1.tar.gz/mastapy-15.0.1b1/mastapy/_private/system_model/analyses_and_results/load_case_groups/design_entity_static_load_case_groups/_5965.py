"""DesignEntityStaticLoadCaseGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DESIGN_ENTITY_STATIC_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups",
    "DesignEntityStaticLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
        _5962,
        _5963,
        _5964,
        _5966,
        _5967,
    )

    Self = TypeVar("Self", bound="DesignEntityStaticLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DesignEntityStaticLoadCaseGroup._Cast_DesignEntityStaticLoadCaseGroup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DesignEntityStaticLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignEntityStaticLoadCaseGroup:
    """Special nested class for casting DesignEntityStaticLoadCaseGroup to subclasses."""

    __parent__: "DesignEntityStaticLoadCaseGroup"

    @property
    def abstract_assembly_static_load_case_group(
        self: "CastSelf",
    ) -> "_5962.AbstractAssemblyStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5962,
        )

        return self.__parent__._cast(_5962.AbstractAssemblyStaticLoadCaseGroup)

    @property
    def component_static_load_case_group(
        self: "CastSelf",
    ) -> "_5963.ComponentStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5963,
        )

        return self.__parent__._cast(_5963.ComponentStaticLoadCaseGroup)

    @property
    def connection_static_load_case_group(
        self: "CastSelf",
    ) -> "_5964.ConnectionStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5964,
        )

        return self.__parent__._cast(_5964.ConnectionStaticLoadCaseGroup)

    @property
    def gear_set_static_load_case_group(
        self: "CastSelf",
    ) -> "_5966.GearSetStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5966,
        )

        return self.__parent__._cast(_5966.GearSetStaticLoadCaseGroup)

    @property
    def part_static_load_case_group(
        self: "CastSelf",
    ) -> "_5967.PartStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5967,
        )

        return self.__parent__._cast(_5967.PartStaticLoadCaseGroup)

    @property
    def design_entity_static_load_case_group(
        self: "CastSelf",
    ) -> "DesignEntityStaticLoadCaseGroup":
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
class DesignEntityStaticLoadCaseGroup(_0.APIBase):
    """DesignEntityStaticLoadCaseGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_ENTITY_STATIC_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_DesignEntityStaticLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_DesignEntityStaticLoadCaseGroup
        """
        return _Cast_DesignEntityStaticLoadCaseGroup(self)
