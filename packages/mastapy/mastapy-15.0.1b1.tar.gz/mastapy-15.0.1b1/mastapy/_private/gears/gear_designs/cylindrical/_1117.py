"""CylindricalGearAbstractRackFlank"""

from __future__ import annotations

from enum import Enum
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

_CYLINDRICAL_GEAR_ABSTRACT_RACK_FLANK = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearAbstractRackFlank"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1116,
        _1119,
        _1122,
        _1134,
        _1190,
    )

    Self = TypeVar("Self", bound="CylindricalGearAbstractRackFlank")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearAbstractRackFlank._Cast_CylindricalGearAbstractRackFlank",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearAbstractRackFlank",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearAbstractRackFlank:
    """Special nested class for casting CylindricalGearAbstractRackFlank to subclasses."""

    __parent__: "CylindricalGearAbstractRackFlank"

    @property
    def cylindrical_gear_basic_rack_flank(
        self: "CastSelf",
    ) -> "_1119.CylindricalGearBasicRackFlank":
        from mastapy._private.gears.gear_designs.cylindrical import _1119

        return self.__parent__._cast(_1119.CylindricalGearBasicRackFlank)

    @property
    def cylindrical_gear_pinion_type_cutter_flank(
        self: "CastSelf",
    ) -> "_1134.CylindricalGearPinionTypeCutterFlank":
        from mastapy._private.gears.gear_designs.cylindrical import _1134

        return self.__parent__._cast(_1134.CylindricalGearPinionTypeCutterFlank)

    @property
    def standard_rack_flank(self: "CastSelf") -> "_1190.StandardRackFlank":
        from mastapy._private.gears.gear_designs.cylindrical import _1190

        return self.__parent__._cast(_1190.StandardRackFlank)

    @property
    def cylindrical_gear_abstract_rack_flank(
        self: "CastSelf",
    ) -> "CylindricalGearAbstractRackFlank":
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
class CylindricalGearAbstractRackFlank(_0.APIBase):
    """CylindricalGearAbstractRackFlank

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_ABSTRACT_RACK_FLANK

    class ProtuberanceSpecificationMethod(Enum):
        """ProtuberanceSpecificationMethod is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _CYLINDRICAL_GEAR_ABSTRACT_RACK_FLANK.ProtuberanceSpecificationMethod

        PROTUBERANCE_HEIGHT_AND_ANGLE = 0
        RESIDUAL_FILLET_UNDERCUT = 1

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    ProtuberanceSpecificationMethod.__setattr__ = __enum_setattr
    ProtuberanceSpecificationMethod.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def chamfer_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ChamferAngle")

        if temp is None:
            return 0.0

        return temp

    @chamfer_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def chamfer_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ChamferAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def chamfer_angle_in_transverse_plane(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ChamferAngleInTransversePlane")

        if temp is None:
            return 0.0

        return temp

    @chamfer_angle_in_transverse_plane.setter
    @exception_bridge
    @enforce_parameter_types
    def chamfer_angle_in_transverse_plane(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ChamferAngleInTransversePlane",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def diameter_chamfer_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DiameterChamferHeight")

        if temp is None:
            return 0.0

        return temp

    @diameter_chamfer_height.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter_chamfer_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DiameterChamferHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def edge_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EdgeRadius")

        if temp is None:
            return 0.0

        return temp

    @edge_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def edge_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EdgeRadius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def edge_radius_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "EdgeRadiusFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @edge_radius_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def edge_radius_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EdgeRadiusFactor", value)

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
    def protuberance_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceAngle")

        if temp is None:
            return 0.0

        return temp

    @protuberance_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def protuberance_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceHeight")

        if temp is None:
            return 0.0

        return temp

    @protuberance_height.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def protuberance_height_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceHeightFactor")

        if temp is None:
            return 0.0

        return temp

    @protuberance_height_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_height_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceHeightFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def protuberance_specification(
        self: "Self",
    ) -> "CylindricalGearAbstractRackFlank.ProtuberanceSpecificationMethod":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearAbstractRackFlank.ProtuberanceSpecificationMethod"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceSpecification")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CylindricalGearAbstractRackFlank+ProtuberanceSpecificationMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical.CylindricalGearAbstractRackFlank.CylindricalGearAbstractRackFlank",
            "ProtuberanceSpecificationMethod",
        )(value)

    @protuberance_specification.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_specification(
        self: "Self",
        value: "CylindricalGearAbstractRackFlank.ProtuberanceSpecificationMethod",
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CylindricalGearAbstractRackFlank+ProtuberanceSpecificationMethod",
        )
        pythonnet_property_set(self.wrapped, "ProtuberanceSpecification", value)

    @property
    @exception_bridge
    def rack_undercut_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RackUndercutClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rack_undercut_clearance_normal_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RackUndercutClearanceNormalModule")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_chamfer_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialChamferHeight")

        if temp is None:
            return 0.0

        return temp

    @radial_chamfer_height.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_chamfer_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialChamferHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def radial_chamfer_height_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialChamferHeightFactor")

        if temp is None:
            return 0.0

        return temp

    @radial_chamfer_height_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_chamfer_height_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialChamferHeightFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def residual_fillet_undercut(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ResidualFilletUndercut")

        if temp is None:
            return 0.0

        return temp

    @residual_fillet_undercut.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_fillet_undercut(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualFilletUndercut",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def residual_fillet_undercut_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ResidualFilletUndercutFactor")

        if temp is None:
            return 0.0

        return temp

    @residual_fillet_undercut_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_fillet_undercut_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualFilletUndercutFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rough_protuberance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RoughProtuberance")

        if temp is None:
            return 0.0

        return temp

    @rough_protuberance.setter
    @exception_bridge
    @enforce_parameter_types
    def rough_protuberance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RoughProtuberance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rough_protuberance_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RoughProtuberanceFactor")

        if temp is None:
            return 0.0

        return temp

    @rough_protuberance_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def rough_protuberance_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RoughProtuberanceFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def cutter(self: "Self") -> "_1116.CylindricalGearAbstractRack":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearAbstractRack

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cutter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear(self: "Self") -> "_1122.CylindricalGearDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gear")

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
    def cast_to(self: "Self") -> "_Cast_CylindricalGearAbstractRackFlank":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearAbstractRackFlank
        """
        return _Cast_CylindricalGearAbstractRackFlank(self)
