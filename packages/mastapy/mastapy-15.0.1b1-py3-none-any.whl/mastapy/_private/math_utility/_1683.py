"""CoordinateSystem3D"""

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
from mastapy._private._math.matrix_4x4 import Matrix4x4
from mastapy._private._math.vector_3d import Vector3D

_COORDINATE_SYSTEM_3D = python_net_import(
    "SMT.MastaAPI.MathUtility", "CoordinateSystem3D"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1688

    Self = TypeVar("Self", bound="CoordinateSystem3D")
    CastSelf = TypeVar("CastSelf", bound="CoordinateSystem3D._Cast_CoordinateSystem3D")


__docformat__ = "restructuredtext en"
__all__ = ("CoordinateSystem3D",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoordinateSystem3D:
    """Special nested class for casting CoordinateSystem3D to subclasses."""

    __parent__: "CoordinateSystem3D"

    @property
    def coordinate_system_3d(self: "CastSelf") -> "CoordinateSystem3D":
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
class CoordinateSystem3D(_0.APIBase):
    """CoordinateSystem3D

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COORDINATE_SYSTEM_3D

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def origin(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Origin")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def x_axis(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def y_axis(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def z_axis(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def axis(self: "Self", degree_of_freedom: "_1688.DegreeOfFreedom") -> "Vector3D":
        """Vector3D

        Args:
            degree_of_freedom (mastapy.math_utility.DegreeOfFreedom)
        """
        degree_of_freedom = conversion.mp_to_pn_enum(
            degree_of_freedom, "SMT.MastaAPI.MathUtility.DegreeOfFreedom"
        )
        return conversion.pn_to_mp_vector3d(
            pythonnet_method_call(self.wrapped, "Axis", degree_of_freedom)
        )

    @exception_bridge
    @enforce_parameter_types
    def rotated_about_axis(
        self: "Self", axis: "Vector3D", angle: "float"
    ) -> "CoordinateSystem3D":
        """mastapy.math_utility.CoordinateSystem3D

        Args:
            axis (Vector3D)
            angle (float)
        """
        axis = conversion.mp_to_pn_vector3d(axis)
        angle = float(angle)
        method_result = pythonnet_method_call(
            self.wrapped, "RotatedAboutAxis", axis, angle if angle else 0.0
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def transform_from_world_to_this(self: "Self") -> "Matrix4x4":
        """Matrix4x4"""
        return conversion.pn_to_mp_matrix4x4(
            pythonnet_method_call(self.wrapped, "TransformFromWorldToThis")
        )

    @exception_bridge
    def transform_to_world_from_this(self: "Self") -> "Matrix4x4":
        """Matrix4x4"""
        return conversion.pn_to_mp_matrix4x4(
            pythonnet_method_call(self.wrapped, "TransformToWorldFromThis")
        )

    @exception_bridge
    @enforce_parameter_types
    def transformed_by(self: "Self", transform: "Matrix4x4") -> "CoordinateSystem3D":
        """mastapy.math_utility.CoordinateSystem3D

        Args:
            transform (Matrix4x4)
        """
        transform = conversion.mp_to_pn_matrix4x4(transform)
        method_result = pythonnet_method_call(self.wrapped, "TransformedBy", transform)
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def without_translation(self: "Self") -> "CoordinateSystem3D":
        """mastapy.math_utility.CoordinateSystem3D"""
        method_result = pythonnet_method_call(self.wrapped, "WithoutTranslation")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CoordinateSystem3D":
        """Cast to another type.

        Returns:
            _Cast_CoordinateSystem3D
        """
        return _Cast_CoordinateSystem3D(self)
