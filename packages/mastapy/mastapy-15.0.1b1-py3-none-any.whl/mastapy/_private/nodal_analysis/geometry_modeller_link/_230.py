"""GearTipRadiusClashTest"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D

_GEAR_TIP_RADIUS_CLASH_TEST = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "GearTipRadiusClashTest"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearTipRadiusClashTest")
    CastSelf = TypeVar(
        "CastSelf", bound="GearTipRadiusClashTest._Cast_GearTipRadiusClashTest"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearTipRadiusClashTest",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearTipRadiusClashTest:
    """Special nested class for casting GearTipRadiusClashTest to subclasses."""

    __parent__: "GearTipRadiusClashTest"

    @property
    def gear_tip_radius_clash_test(self: "CastSelf") -> "GearTipRadiusClashTest":
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
class GearTipRadiusClashTest(_0.APIBase):
    """GearTipRadiusClashTest

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_TIP_RADIUS_CLASH_TEST

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def body_moniker(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "BodyMoniker")

        if temp is None:
            return ""

        return temp

    @body_moniker.setter
    @exception_bridge
    @enforce_parameter_types
    def body_moniker(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "BodyMoniker", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def error_message(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "ErrorMessage")

        if temp is None:
            return ""

        return temp

    @error_message.setter
    @exception_bridge
    @enforce_parameter_types
    def error_message(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "ErrorMessage", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def gear_axis(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

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
    def position(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Position")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def radial_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialLimit")

        if temp is None:
            return 0.0

        return temp

    @radial_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialLimit", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearTipRadiusClashTest":
        """Cast to another type.

        Returns:
            _Cast_GearTipRadiusClashTest
        """
        return _Cast_GearTipRadiusClashTest(self)
