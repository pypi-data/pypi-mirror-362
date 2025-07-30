"""StandardSplineJointDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.detailed_rigid_connectors.splines import _1588, _1589, _1600

_STANDARD_SPLINE_JOINT_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "StandardSplineJointDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors import _1572
    from mastapy._private.detailed_rigid_connectors.splines import (
        _1578,
        _1582,
        _1585,
        _1586,
        _1590,
        _1593,
    )

    Self = TypeVar("Self", bound="StandardSplineJointDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="StandardSplineJointDesign._Cast_StandardSplineJointDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StandardSplineJointDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StandardSplineJointDesign:
    """Special nested class for casting StandardSplineJointDesign to subclasses."""

    __parent__: "StandardSplineJointDesign"

    @property
    def spline_joint_design(self: "CastSelf") -> "_1600.SplineJointDesign":
        return self.__parent__._cast(_1600.SplineJointDesign)

    @property
    def detailed_rigid_connector_design(
        self: "CastSelf",
    ) -> "_1572.DetailedRigidConnectorDesign":
        from mastapy._private.detailed_rigid_connectors import _1572

        return self.__parent__._cast(_1572.DetailedRigidConnectorDesign)

    @property
    def din5480_spline_joint_design(
        self: "CastSelf",
    ) -> "_1578.DIN5480SplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1578

        return self.__parent__._cast(_1578.DIN5480SplineJointDesign)

    @property
    def gbt3478_spline_joint_design(
        self: "CastSelf",
    ) -> "_1582.GBT3478SplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1582

        return self.__parent__._cast(_1582.GBT3478SplineJointDesign)

    @property
    def iso4156_spline_joint_design(
        self: "CastSelf",
    ) -> "_1585.ISO4156SplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1585

        return self.__parent__._cast(_1585.ISO4156SplineJointDesign)

    @property
    def jisb1603_spline_joint_design(
        self: "CastSelf",
    ) -> "_1586.JISB1603SplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1586

        return self.__parent__._cast(_1586.JISB1603SplineJointDesign)

    @property
    def sae_spline_joint_design(self: "CastSelf") -> "_1593.SAESplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1593

        return self.__parent__._cast(_1593.SAESplineJointDesign)

    @property
    def standard_spline_joint_design(self: "CastSelf") -> "StandardSplineJointDesign":
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
class StandardSplineJointDesign(_1600.SplineJointDesign):
    """StandardSplineJointDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STANDARD_SPLINE_JOINT_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def diametral_pitch(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DiametralPitch")

        if temp is None:
            return 0.0

        return temp

    @diametral_pitch.setter
    @exception_bridge
    @enforce_parameter_types
    def diametral_pitch(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DiametralPitch", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Module")

        if temp is None:
            return 0.0

        return temp

    @module.setter
    @exception_bridge
    @enforce_parameter_types
    def module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Module", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def module_preferred(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_Modules":
        """EnumWithSelectedValue[mastapy.detailed_rigid_connectors.splines.Modules]"""
        temp = pythonnet_property_get(self.wrapped, "ModulePreferred")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_Modules.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @module_preferred.setter
    @exception_bridge
    @enforce_parameter_types
    def module_preferred(self: "Self", value: "_1588.Modules") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_Modules.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ModulePreferred", value)

    @property
    @exception_bridge
    def module_from_preferred_series(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ModuleFromPreferredSeries")

        if temp is None:
            return False

        return temp

    @module_from_preferred_series.setter
    @exception_bridge
    @enforce_parameter_types
    def module_from_preferred_series(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModuleFromPreferredSeries",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureAngle")

        if temp is None:
            return 0.0

        return temp

    @pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PressureAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def pressure_angle_preferred(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_PressureAngleTypes":
        """EnumWithSelectedValue[mastapy.detailed_rigid_connectors.splines.PressureAngleTypes]"""
        temp = pythonnet_property_get(self.wrapped, "PressureAnglePreferred")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_PressureAngleTypes.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @pressure_angle_preferred.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_angle_preferred(
        self: "Self", value: "_1589.PressureAngleTypes"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PressureAngleTypes.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "PressureAnglePreferred", value)

    @property
    @exception_bridge
    def root_type(self: "Self") -> "_1590.RootTypes":
        """mastapy.detailed_rigid_connectors.splines.RootTypes"""
        temp = pythonnet_property_get(self.wrapped, "RootType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.DetailedRigidConnectors.Splines.RootTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.splines._1590", "RootTypes"
        )(value)

    @root_type.setter
    @exception_bridge
    @enforce_parameter_types
    def root_type(self: "Self", value: "_1590.RootTypes") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.DetailedRigidConnectors.Splines.RootTypes"
        )
        pythonnet_property_set(self.wrapped, "RootType", value)

    @property
    def cast_to(self: "Self") -> "_Cast_StandardSplineJointDesign":
        """Cast to another type.

        Returns:
            _Cast_StandardSplineJointDesign
        """
        return _Cast_StandardSplineJointDesign(self)
