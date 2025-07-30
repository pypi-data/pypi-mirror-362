"""CylindricalGearAbstractRack"""

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

_CYLINDRICAL_GEAR_ABSTRACT_RACK = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearAbstractRack"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1117,
        _1118,
        _1122,
        _1133,
        _1189,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters import _817

    Self = TypeVar("Self", bound="CylindricalGearAbstractRack")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearAbstractRack._Cast_CylindricalGearAbstractRack",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearAbstractRack",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearAbstractRack:
    """Special nested class for casting CylindricalGearAbstractRack to subclasses."""

    __parent__: "CylindricalGearAbstractRack"

    @property
    def cylindrical_gear_basic_rack(
        self: "CastSelf",
    ) -> "_1118.CylindricalGearBasicRack":
        from mastapy._private.gears.gear_designs.cylindrical import _1118

        return self.__parent__._cast(_1118.CylindricalGearBasicRack)

    @property
    def cylindrical_gear_pinion_type_cutter(
        self: "CastSelf",
    ) -> "_1133.CylindricalGearPinionTypeCutter":
        from mastapy._private.gears.gear_designs.cylindrical import _1133

        return self.__parent__._cast(_1133.CylindricalGearPinionTypeCutter)

    @property
    def standard_rack(self: "CastSelf") -> "_1189.StandardRack":
        from mastapy._private.gears.gear_designs.cylindrical import _1189

        return self.__parent__._cast(_1189.StandardRack)

    @property
    def cylindrical_gear_abstract_rack(
        self: "CastSelf",
    ) -> "CylindricalGearAbstractRack":
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
class CylindricalGearAbstractRack(_0.APIBase):
    """CylindricalGearAbstractRack

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_ABSTRACT_RACK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def basic_rack_addendum_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "BasicRackAddendumFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @basic_rack_addendum_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def basic_rack_addendum_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BasicRackAddendumFactor", value)

    @property
    @exception_bridge
    def basic_rack_dedendum_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "BasicRackDedendumFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @basic_rack_dedendum_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def basic_rack_dedendum_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BasicRackDedendumFactor", value)

    @property
    @exception_bridge
    def basic_rack_tip_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRackTipThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rack_tooth_depth_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRackToothDepthFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cutter_tip_width_normal_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterTipWidthNormalModule")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_possible_cutter_edge_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPossibleCutterEdgeRadius")

        if temp is None:
            return 0.0

        return temp

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
    def use_maximum_edge_radius(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseMaximumEdgeRadius")

        if temp is None:
            return False

        return temp

    @use_maximum_edge_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def use_maximum_edge_radius(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseMaximumEdgeRadius",
            bool(value) if value is not None else False,
        )

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
    def left_flank(self: "Self") -> "_1117.CylindricalGearAbstractRackFlank":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearAbstractRackFlank

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank(self: "Self") -> "_1117.CylindricalGearAbstractRackFlank":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearAbstractRackFlank

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaper_for_agma_rating(self: "Self") -> "_817.CylindricalGearShaper":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaper

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaperForAGMARating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def flanks(self: "Self") -> "List[_1117.CylindricalGearAbstractRackFlank]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearAbstractRackFlank]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Flanks")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def both_flanks(self: "Self") -> "_1117.CylindricalGearAbstractRackFlank":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearAbstractRackFlank

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BothFlanks")

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
    def cast_to(self: "Self") -> "_Cast_CylindricalGearAbstractRack":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearAbstractRack
        """
        return _Cast_CylindricalGearAbstractRack(self)
