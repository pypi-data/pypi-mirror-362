"""ElementPropertiesBase"""

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

_ELEMENT_PROPERTIES_BASE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ElementPropertiesBase",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.fe_tools.enums import _1363
    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _295,
        _296,
        _297,
        _298,
        _299,
        _300,
        _301,
        _302,
    )

    Self = TypeVar("Self", bound="ElementPropertiesBase")
    CastSelf = TypeVar(
        "CastSelf", bound="ElementPropertiesBase._Cast_ElementPropertiesBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementPropertiesBase:
    """Special nested class for casting ElementPropertiesBase to subclasses."""

    __parent__: "ElementPropertiesBase"

    @property
    def element_properties_beam(self: "CastSelf") -> "_295.ElementPropertiesBeam":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _295,
        )

        return self.__parent__._cast(_295.ElementPropertiesBeam)

    @property
    def element_properties_interface(
        self: "CastSelf",
    ) -> "_296.ElementPropertiesInterface":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _296,
        )

        return self.__parent__._cast(_296.ElementPropertiesInterface)

    @property
    def element_properties_mass(self: "CastSelf") -> "_297.ElementPropertiesMass":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _297,
        )

        return self.__parent__._cast(_297.ElementPropertiesMass)

    @property
    def element_properties_rigid(self: "CastSelf") -> "_298.ElementPropertiesRigid":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _298,
        )

        return self.__parent__._cast(_298.ElementPropertiesRigid)

    @property
    def element_properties_shell(self: "CastSelf") -> "_299.ElementPropertiesShell":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _299,
        )

        return self.__parent__._cast(_299.ElementPropertiesShell)

    @property
    def element_properties_solid(self: "CastSelf") -> "_300.ElementPropertiesSolid":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _300,
        )

        return self.__parent__._cast(_300.ElementPropertiesSolid)

    @property
    def element_properties_spring_dashpot(
        self: "CastSelf",
    ) -> "_301.ElementPropertiesSpringDashpot":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _301,
        )

        return self.__parent__._cast(_301.ElementPropertiesSpringDashpot)

    @property
    def element_properties_with_material(
        self: "CastSelf",
    ) -> "_302.ElementPropertiesWithMaterial":
        from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
            _302,
        )

        return self.__parent__._cast(_302.ElementPropertiesWithMaterial)

    @property
    def element_properties_base(self: "CastSelf") -> "ElementPropertiesBase":
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
class ElementPropertiesBase(_0.APIBase):
    """ElementPropertiesBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_PROPERTIES_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def class_(self: "Self") -> "_1363.ElementPropertyClass":
        """mastapy.fe_tools.enums.ElementPropertyClass

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Class")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.FETools.Enums.ElementPropertyClass"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.fe_tools.enums._1363", "ElementPropertyClass"
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
    def cast_to(self: "Self") -> "_Cast_ElementPropertiesBase":
        """Cast to another type.

        Returns:
            _Cast_ElementPropertiesBase
        """
        return _Cast_ElementPropertiesBase(self)
