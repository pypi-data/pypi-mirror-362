"""BoltGeometry"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.databases import _2028

_BOLT_GEOMETRY = python_net_import("SMT.MastaAPI.Bolts", "BoltGeometry")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bolts import _1657, _1658, _1659, _1664, _1669, _1671

    Self = TypeVar("Self", bound="BoltGeometry")
    CastSelf = TypeVar("CastSelf", bound="BoltGeometry._Cast_BoltGeometry")


__docformat__ = "restructuredtext en"
__all__ = ("BoltGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BoltGeometry:
    """Special nested class for casting BoltGeometry to subclasses."""

    __parent__: "BoltGeometry"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def bolt_geometry(self: "CastSelf") -> "BoltGeometry":
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
class BoltGeometry(_2028.NamedDatabaseItem):
    """BoltGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BOLT_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bolt_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BoltDiameter")

        if temp is None:
            return 0.0

        return temp

    @bolt_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def bolt_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BoltDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def bolt_inner_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BoltInnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @bolt_inner_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def bolt_inner_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BoltInnerDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def bolt_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BoltLength")

        if temp is None:
            return 0.0

        return temp

    @bolt_length.setter
    @exception_bridge
    @enforce_parameter_types
    def bolt_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BoltLength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def bolt_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def bolt_sections(self: "Self") -> "List[_1657.BoltSection]":
        """List[mastapy.bolts.BoltSection]"""
        temp = pythonnet_property_get(self.wrapped, "BoltSections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @bolt_sections.setter
    @exception_bridge
    @enforce_parameter_types
    def bolt_sections(self: "Self", value: "List[_1657.BoltSection]") -> None:
        value = conversion.mp_to_pn_objects_in_list(value)
        pythonnet_property_set(self.wrapped, "BoltSections", value)

    @property
    @exception_bridge
    def bolt_shank_type(self: "Self") -> "_1658.BoltShankType":
        """mastapy.bolts.BoltShankType"""
        temp = pythonnet_property_get(self.wrapped, "BoltShankType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bolts.BoltShankType")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bolts._1658", "BoltShankType"
        )(value)

    @bolt_shank_type.setter
    @exception_bridge
    @enforce_parameter_types
    def bolt_shank_type(self: "Self", value: "_1658.BoltShankType") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Bolts.BoltShankType")
        pythonnet_property_set(self.wrapped, "BoltShankType", value)

    @property
    @exception_bridge
    def bolt_thread_pitch_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BoltThreadPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @bolt_thread_pitch_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def bolt_thread_pitch_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BoltThreadPitchDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def has_cross_sections_of_different_diameters(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "HasCrossSectionsOfDifferentDiameters"
        )

        if temp is None:
            return False

        return temp

    @has_cross_sections_of_different_diameters.setter
    @exception_bridge
    @enforce_parameter_types
    def has_cross_sections_of_different_diameters(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HasCrossSectionsOfDifferentDiameters",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def hole_chamfer_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HoleChamferWidth")

        if temp is None:
            return 0.0

        return temp

    @hole_chamfer_width.setter
    @exception_bridge
    @enforce_parameter_types
    def hole_chamfer_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HoleChamferWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def hole_diameter_of_clamped_parts(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HoleDiameterOfClampedParts")

        if temp is None:
            return 0.0

        return temp

    @hole_diameter_of_clamped_parts.setter
    @exception_bridge
    @enforce_parameter_types
    def hole_diameter_of_clamped_parts(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HoleDiameterOfClampedParts",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def is_threaded_to_head(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsThreadedToHead")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def minor_diameter_of_bolt_thread(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinorDiameterOfBoltThread")

        if temp is None:
            return 0.0

        return temp

    @minor_diameter_of_bolt_thread.setter
    @exception_bridge
    @enforce_parameter_types
    def minor_diameter_of_bolt_thread(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinorDiameterOfBoltThread",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def nut_thread_minor_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NutThreadMinorDiameter")

        if temp is None:
            return 0.0

        return temp

    @nut_thread_minor_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def nut_thread_minor_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NutThreadMinorDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def nut_thread_pitch_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NutThreadPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @nut_thread_pitch_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def nut_thread_pitch_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NutThreadPitchDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def outside_diameter_of_clamped_parts(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OutsideDiameterOfClampedParts")

        if temp is None:
            return 0.0

        return temp

    @outside_diameter_of_clamped_parts.setter
    @exception_bridge
    @enforce_parameter_types
    def outside_diameter_of_clamped_parts(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OutsideDiameterOfClampedParts",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pitch_of_thread(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PitchOfThread")

        if temp is None:
            return 0.0

        return temp

    @pitch_of_thread.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_of_thread(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PitchOfThread", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def shank_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShankDiameter")

        if temp is None:
            return 0.0

        return temp

    @shank_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def shank_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShankDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def shank_inner_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShankInnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @shank_inner_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def shank_inner_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShankInnerDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shank_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShankLength")

        if temp is None:
            return 0.0

        return temp

    @shank_length.setter
    @exception_bridge
    @enforce_parameter_types
    def shank_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShankLength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def standard_size(self: "Self") -> "_1669.StandardSizes":
        """mastapy.bolts.StandardSizes"""
        temp = pythonnet_property_get(self.wrapped, "StandardSize")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bolts.StandardSizes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bolts._1669", "StandardSizes"
        )(value)

    @standard_size.setter
    @exception_bridge
    @enforce_parameter_types
    def standard_size(self: "Self", value: "_1669.StandardSizes") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Bolts.StandardSizes")
        pythonnet_property_set(self.wrapped, "StandardSize", value)

    @property
    @exception_bridge
    def tapped_thread_minor_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TappedThreadMinorDiameter")

        if temp is None:
            return 0.0

        return temp

    @tapped_thread_minor_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def tapped_thread_minor_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TappedThreadMinorDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tapped_thread_pitch_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TappedThreadPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @tapped_thread_pitch_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def tapped_thread_pitch_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TappedThreadPitchDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def type_of_bolted_joint(self: "Self") -> "_1659.BoltTypes":
        """mastapy.bolts.BoltTypes"""
        temp = pythonnet_property_get(self.wrapped, "TypeOfBoltedJoint")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bolts.BoltTypes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bolts._1659", "BoltTypes"
        )(value)

    @type_of_bolted_joint.setter
    @exception_bridge
    @enforce_parameter_types
    def type_of_bolted_joint(self: "Self", value: "_1659.BoltTypes") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Bolts.BoltTypes")
        pythonnet_property_set(self.wrapped, "TypeOfBoltedJoint", value)

    @property
    @exception_bridge
    def type_of_head_cap(self: "Self") -> "_1664.HeadCapTypes":
        """mastapy.bolts.HeadCapTypes"""
        temp = pythonnet_property_get(self.wrapped, "TypeOfHeadCap")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bolts.HeadCapTypes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bolts._1664", "HeadCapTypes"
        )(value)

    @type_of_head_cap.setter
    @exception_bridge
    @enforce_parameter_types
    def type_of_head_cap(self: "Self", value: "_1664.HeadCapTypes") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Bolts.HeadCapTypes")
        pythonnet_property_set(self.wrapped, "TypeOfHeadCap", value)

    @property
    @exception_bridge
    def type_of_thread(self: "Self") -> "_1671.ThreadTypes":
        """mastapy.bolts.ThreadTypes"""
        temp = pythonnet_property_get(self.wrapped, "TypeOfThread")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bolts.ThreadTypes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bolts._1671", "ThreadTypes"
        )(value)

    @type_of_thread.setter
    @exception_bridge
    @enforce_parameter_types
    def type_of_thread(self: "Self", value: "_1671.ThreadTypes") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Bolts.ThreadTypes")
        pythonnet_property_set(self.wrapped, "TypeOfThread", value)

    @property
    @exception_bridge
    def width_across_flats(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WidthAcrossFlats")

        if temp is None:
            return 0.0

        return temp

    @width_across_flats.setter
    @exception_bridge
    @enforce_parameter_types
    def width_across_flats(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WidthAcrossFlats", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BoltGeometry":
        """Cast to another type.

        Returns:
            _Cast_BoltGeometry
        """
        return _Cast_BoltGeometry(self)
