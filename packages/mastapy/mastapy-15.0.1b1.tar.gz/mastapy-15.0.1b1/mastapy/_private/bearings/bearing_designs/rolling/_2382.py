"""TaperRollerBearing"""

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
from mastapy._private.bearings.bearing_designs.rolling import _2371

_TAPER_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "TaperRollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _2079
    from mastapy._private.bearings.bearing_designs import _2340, _2341, _2344
    from mastapy._private.bearings.bearing_designs.rolling import _2372, _2375

    Self = TypeVar("Self", bound="TaperRollerBearing")
    CastSelf = TypeVar("CastSelf", bound="TaperRollerBearing._Cast_TaperRollerBearing")


__docformat__ = "restructuredtext en"
__all__ = ("TaperRollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TaperRollerBearing:
    """Special nested class for casting TaperRollerBearing to subclasses."""

    __parent__: "TaperRollerBearing"

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2371.NonBarrelRollerBearing":
        return self.__parent__._cast(_2371.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2372.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2372

        return self.__parent__._cast(_2372.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2375.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2375

        return self.__parent__._cast(_2375.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2341.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2341

        return self.__parent__._cast(_2341.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2344.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2344

        return self.__parent__._cast(_2344.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2340.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2340

        return self.__parent__._cast(_2340.BearingDesign)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "TaperRollerBearing":
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
class TaperRollerBearing(_2371.NonBarrelRollerBearing):
    """TaperRollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TAPER_ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def apex_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ApexLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def assembled_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AssembledWidth")

        if temp is None:
            return 0.0

        return temp

    @assembled_width.setter
    @exception_bridge
    @enforce_parameter_types
    def assembled_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AssembledWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def bearing_measurement_type(self: "Self") -> "_2079.BearingMeasurementType":
        """mastapy.bearings.BearingMeasurementType"""
        temp = pythonnet_property_get(self.wrapped, "BearingMeasurementType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingMeasurementType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2079", "BearingMeasurementType"
        )(value)

    @bearing_measurement_type.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_measurement_type(
        self: "Self", value: "_2079.BearingMeasurementType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingMeasurementType"
        )
        pythonnet_property_set(self.wrapped, "BearingMeasurementType", value)

    @property
    @exception_bridge
    def cone_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConeAngle")

        if temp is None:
            return 0.0

        return temp

    @cone_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def cone_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ConeAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def cup_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CupAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cup_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def cup_angle(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CupAngle", value)

    @property
    @exception_bridge
    def effective_centre_from_front_face(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EffectiveCentreFromFrontFace")

        if temp is None:
            return 0.0

        return temp

    @effective_centre_from_front_face.setter
    @exception_bridge
    @enforce_parameter_types
    def effective_centre_from_front_face(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EffectiveCentreFromFrontFace",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def effective_centre_to_front_face_set_by_changing_outer_ring_offset(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EffectiveCentreToFrontFaceSetByChangingOuterRingOffset"
        )

        if temp is None:
            return 0.0

        return temp

    @effective_centre_to_front_face_set_by_changing_outer_ring_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def effective_centre_to_front_face_set_by_changing_outer_ring_offset(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EffectiveCentreToFrontFaceSetByChangingOuterRingOffset",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def element_taper_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementTaperAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_taper_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def element_taper_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementTaperAngle", value)

    @property
    @exception_bridge
    def inner_ring_back_face_corner_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingBackFaceCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_back_face_corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_back_face_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingBackFaceCornerRadius", value)

    @property
    @exception_bridge
    def inner_ring_front_face_corner_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingFrontFaceCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_front_face_corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_front_face_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingFrontFaceCornerRadius", value)

    @property
    @exception_bridge
    def left_element_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LeftElementCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @left_element_corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def left_element_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LeftElementCornerRadius", value)

    @property
    @exception_bridge
    def mean_inner_race_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanInnerRaceDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_outer_race_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanOuterRaceDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_ring_back_face_corner_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingBackFaceCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_back_face_corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_back_face_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingBackFaceCornerRadius", value)

    @property
    @exception_bridge
    def outer_ring_front_face_corner_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingFrontFaceCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_front_face_corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_front_face_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingFrontFaceCornerRadius", value)

    @property
    @exception_bridge
    def right_element_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RightElementCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @right_element_corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def right_element_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RightElementCornerRadius", value)

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def width_setting_inner_and_outer_ring_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "WidthSettingInnerAndOuterRingWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @width_setting_inner_and_outer_ring_width.setter
    @exception_bridge
    @enforce_parameter_types
    def width_setting_inner_and_outer_ring_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WidthSettingInnerAndOuterRingWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TaperRollerBearing":
        """Cast to another type.

        Returns:
            _Cast_TaperRollerBearing
        """
        return _Cast_TaperRollerBearing(self)
