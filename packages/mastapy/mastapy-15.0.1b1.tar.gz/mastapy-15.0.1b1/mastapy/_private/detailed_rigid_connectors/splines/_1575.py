"""CustomSplineJointDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.detailed_rigid_connectors.splines import _1600

_CUSTOM_SPLINE_JOINT_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "CustomSplineJointDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors import _1572

    Self = TypeVar("Self", bound="CustomSplineJointDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomSplineJointDesign._Cast_CustomSplineJointDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomSplineJointDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomSplineJointDesign:
    """Special nested class for casting CustomSplineJointDesign to subclasses."""

    __parent__: "CustomSplineJointDesign"

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
    def custom_spline_joint_design(self: "CastSelf") -> "CustomSplineJointDesign":
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
class CustomSplineJointDesign(_1600.SplineJointDesign):
    """CustomSplineJointDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_SPLINE_JOINT_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_CustomSplineJointDesign":
        """Cast to another type.

        Returns:
            _Cast_CustomSplineJointDesign
        """
        return _Cast_CustomSplineJointDesign(self)
