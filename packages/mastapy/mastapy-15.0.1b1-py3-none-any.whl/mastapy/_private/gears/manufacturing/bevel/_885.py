"""ConicalMeshFlankMicroGeometryConfig"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CONICAL_MESH_FLANK_MICRO_GEOMETRY_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalMeshFlankMicroGeometryConfig"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical.micro_geometry import _1293
    from mastapy._private.gears.manufacturing.bevel import _884, _886

    Self = TypeVar("Self", bound="ConicalMeshFlankMicroGeometryConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshFlankMicroGeometryConfig._Cast_ConicalMeshFlankMicroGeometryConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshFlankMicroGeometryConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshFlankMicroGeometryConfig:
    """Special nested class for casting ConicalMeshFlankMicroGeometryConfig to subclasses."""

    __parent__: "ConicalMeshFlankMicroGeometryConfig"

    @property
    def conical_mesh_flank_manufacturing_config(
        self: "CastSelf",
    ) -> "_884.ConicalMeshFlankManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _884

        return self.__parent__._cast(_884.ConicalMeshFlankManufacturingConfig)

    @property
    def conical_mesh_flank_nurbs_micro_geometry_config(
        self: "CastSelf",
    ) -> "_886.ConicalMeshFlankNURBSMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _886

        return self.__parent__._cast(_886.ConicalMeshFlankNURBSMicroGeometryConfig)

    @property
    def conical_mesh_flank_micro_geometry_config(
        self: "CastSelf",
    ) -> "ConicalMeshFlankMicroGeometryConfig":
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
class ConicalMeshFlankMicroGeometryConfig(_0.APIBase):
    """ConicalMeshFlankMicroGeometryConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_FLANK_MICRO_GEOMETRY_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def delta_h_as_percent_of_face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaHAsPercentOfFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @delta_h_as_percent_of_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_h_as_percent_of_face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DeltaHAsPercentOfFaceWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def delta_v_as_percent_of_wheel_tip_to_fillet_flank_boundary(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DeltaVAsPercentOfWheelTipToFilletFlankBoundary"
        )

        if temp is None:
            return 0.0

        return temp

    @delta_v_as_percent_of_wheel_tip_to_fillet_flank_boundary.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_v_as_percent_of_wheel_tip_to_fillet_flank_boundary(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DeltaVAsPercentOfWheelTipToFilletFlankBoundary",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def perform_vh_check(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "PerformVHCheck")

        if temp is None:
            return False

        return temp

    @perform_vh_check.setter
    @exception_bridge
    @enforce_parameter_types
    def perform_vh_check(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "PerformVHCheck", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def specified_ease_off_surface(
        self: "Self",
    ) -> "_1293.ConicalGearFlankMicroGeometry":
        """mastapy.gears.gear_designs.conical.micro_geometry.ConicalGearFlankMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpecifiedEaseOffSurface")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshFlankMicroGeometryConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshFlankMicroGeometryConfig
        """
        return _Cast_ConicalMeshFlankMicroGeometryConfig(self)
