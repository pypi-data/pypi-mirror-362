"""Modification"""

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

_MODIFICATION = python_net_import("SMT.MastaAPI.Gears.MicroGeometry", "Modification")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs.conical.micro_geometry import (
        _1292,
        _1294,
        _1295,
    )
    from mastapy._private.gears.gear_designs.cylindrical import _1132
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1206,
        _1209,
        _1210,
        _1218,
        _1219,
        _1223,
    )
    from mastapy._private.gears.micro_geometry import _660, _663, _673

    Self = TypeVar("Self", bound="Modification")
    CastSelf = TypeVar("CastSelf", bound="Modification._Cast_Modification")


__docformat__ = "restructuredtext en"
__all__ = ("Modification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Modification:
    """Special nested class for casting Modification to subclasses."""

    __parent__: "Modification"

    @property
    def bias_modification(self: "CastSelf") -> "_660.BiasModification":
        from mastapy._private.gears.micro_geometry import _660

        return self.__parent__._cast(_660.BiasModification)

    @property
    def lead_modification(self: "CastSelf") -> "_663.LeadModification":
        from mastapy._private.gears.micro_geometry import _663

        return self.__parent__._cast(_663.LeadModification)

    @property
    def profile_modification(self: "CastSelf") -> "_673.ProfileModification":
        from mastapy._private.gears.micro_geometry import _673

        return self.__parent__._cast(_673.ProfileModification)

    @property
    def cylindrical_gear_bias_modification(
        self: "CastSelf",
    ) -> "_1206.CylindricalGearBiasModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1206

        return self.__parent__._cast(_1206.CylindricalGearBiasModification)

    @property
    def cylindrical_gear_lead_modification(
        self: "CastSelf",
    ) -> "_1209.CylindricalGearLeadModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1209

        return self.__parent__._cast(_1209.CylindricalGearLeadModification)

    @property
    def cylindrical_gear_lead_modification_at_profile_position(
        self: "CastSelf",
    ) -> "_1210.CylindricalGearLeadModificationAtProfilePosition":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1210

        return self.__parent__._cast(
            _1210.CylindricalGearLeadModificationAtProfilePosition
        )

    @property
    def cylindrical_gear_profile_modification(
        self: "CastSelf",
    ) -> "_1218.CylindricalGearProfileModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1218

        return self.__parent__._cast(_1218.CylindricalGearProfileModification)

    @property
    def cylindrical_gear_profile_modification_at_face_width_position(
        self: "CastSelf",
    ) -> "_1219.CylindricalGearProfileModificationAtFaceWidthPosition":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1219

        return self.__parent__._cast(
            _1219.CylindricalGearProfileModificationAtFaceWidthPosition
        )

    @property
    def cylindrical_gear_triangular_end_modification(
        self: "CastSelf",
    ) -> "_1223.CylindricalGearTriangularEndModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1223

        return self.__parent__._cast(_1223.CylindricalGearTriangularEndModification)

    @property
    def conical_gear_bias_modification(
        self: "CastSelf",
    ) -> "_1292.ConicalGearBiasModification":
        from mastapy._private.gears.gear_designs.conical.micro_geometry import _1292

        return self.__parent__._cast(_1292.ConicalGearBiasModification)

    @property
    def conical_gear_lead_modification(
        self: "CastSelf",
    ) -> "_1294.ConicalGearLeadModification":
        from mastapy._private.gears.gear_designs.conical.micro_geometry import _1294

        return self.__parent__._cast(_1294.ConicalGearLeadModification)

    @property
    def conical_gear_profile_modification(
        self: "CastSelf",
    ) -> "_1295.ConicalGearProfileModification":
        from mastapy._private.gears.gear_designs.conical.micro_geometry import _1295

        return self.__parent__._cast(_1295.ConicalGearProfileModification)

    @property
    def modification(self: "CastSelf") -> "Modification":
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
class Modification(_0.APIBase):
    """Modification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def settings(self: "Self") -> "_1132.CylindricalGearMicroGeometrySettingsItem":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMicroGeometrySettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Settings")

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
    def cast_to(self: "Self") -> "_Cast_Modification":
        """Cast to another type.

        Returns:
            _Cast_Modification
        """
        return _Cast_Modification(self)
