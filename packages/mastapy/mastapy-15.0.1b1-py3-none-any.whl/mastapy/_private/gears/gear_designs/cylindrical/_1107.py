"""CrossedAxisCylindricalGearPair"""

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

_CROSSED_AXIS_CYLINDRICAL_GEAR_PAIR = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CrossedAxisCylindricalGearPair"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs.cylindrical import _1108, _1109
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _835

    Self = TypeVar("Self", bound="CrossedAxisCylindricalGearPair")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CrossedAxisCylindricalGearPair._Cast_CrossedAxisCylindricalGearPair",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CrossedAxisCylindricalGearPair",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CrossedAxisCylindricalGearPair:
    """Special nested class for casting CrossedAxisCylindricalGearPair to subclasses."""

    __parent__: "CrossedAxisCylindricalGearPair"

    @property
    def crossed_axis_cylindrical_gear_pair_line_contact(
        self: "CastSelf",
    ) -> "_1108.CrossedAxisCylindricalGearPairLineContact":
        from mastapy._private.gears.gear_designs.cylindrical import _1108

        return self.__parent__._cast(_1108.CrossedAxisCylindricalGearPairLineContact)

    @property
    def crossed_axis_cylindrical_gear_pair_point_contact(
        self: "CastSelf",
    ) -> "_1109.CrossedAxisCylindricalGearPairPointContact":
        from mastapy._private.gears.gear_designs.cylindrical import _1109

        return self.__parent__._cast(_1109.CrossedAxisCylindricalGearPairPointContact)

    @property
    def crossed_axis_cylindrical_gear_pair(
        self: "CastSelf",
    ) -> "CrossedAxisCylindricalGearPair":
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
class CrossedAxisCylindricalGearPair(_0.APIBase):
    """CrossedAxisCylindricalGearPair

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CROSSED_AXIS_CYLINDRICAL_GEAR_PAIR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def centre_distance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CentreDistance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @centre_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def centre_distance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CentreDistance", value)

    @property
    @exception_bridge
    def contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cutter_normal_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterNormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_gear_start_of_active_profile_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EffectiveGearStartOfActiveProfileDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_end_of_active_profile_diameter(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearEndOfActiveProfileDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def gear_normal_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearNormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_operating_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearOperatingRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_start_of_active_profile_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearStartOfActiveProfileDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def operating_normal_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingNormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaft_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ShaftAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @shaft_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_angle(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ShaftAngle", value)

    @property
    @exception_bridge
    def shaver_end_of_active_profile_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaverEndOfActiveProfileDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaver_operating_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaverOperatingRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaver_required_end_of_active_profile_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaverRequiredEndOfActiveProfileDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaver_start_of_active_profile_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaverStartOfActiveProfileDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaver_tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaverTipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaver_tip_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaverTipRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaver_tip_radius_calculated_by_gear_sap(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaverTipRadiusCalculatedByGearSAP"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaver(self: "Self") -> "_835.CylindricalCutterSimulatableGear":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.CylindricalCutterSimulatableGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shaver")

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
    def cast_to(self: "Self") -> "_Cast_CrossedAxisCylindricalGearPair":
        """Cast to another type.

        Returns:
            _Cast_CrossedAxisCylindricalGearPair
        """
        return _Cast_CrossedAxisCylindricalGearPair(self)
