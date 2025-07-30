"""KIMoSBevelHypoidSingleRotationAngleResult"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_KI_MO_S_BEVEL_HYPOID_SINGLE_ROTATION_ANGLE_RESULT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical",
    "KIMoSBevelHypoidSingleRotationAngleResult",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="KIMoSBevelHypoidSingleRotationAngleResult")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KIMoSBevelHypoidSingleRotationAngleResult._Cast_KIMoSBevelHypoidSingleRotationAngleResult",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KIMoSBevelHypoidSingleRotationAngleResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KIMoSBevelHypoidSingleRotationAngleResult:
    """Special nested class for casting KIMoSBevelHypoidSingleRotationAngleResult to subclasses."""

    __parent__: "KIMoSBevelHypoidSingleRotationAngleResult"

    @property
    def ki_mo_s_bevel_hypoid_single_rotation_angle_result(
        self: "CastSelf",
    ) -> "KIMoSBevelHypoidSingleRotationAngleResult":
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
class KIMoSBevelHypoidSingleRotationAngleResult(_0.APIBase):
    """KIMoSBevelHypoidSingleRotationAngleResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KI_MO_S_BEVEL_HYPOID_SINGLE_ROTATION_ANGLE_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def linear_transmission_error_loaded(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearTransmissionErrorLoaded")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def linear_transmission_error_unloaded(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearTransmissionErrorUnloaded")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_pinion_root_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumPinionRootStress")

        if temp is None:
            return 0.0

        return temp

    @maximum_pinion_root_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_pinion_root_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumPinionRootStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_wheel_root_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumWheelRootStress")

        if temp is None:
            return 0.0

        return temp

    @maximum_wheel_root_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_wheel_root_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumWheelRootStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mesh_stiffness_per_unit_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshStiffnessPerUnitFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_rotation_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionRotationAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_KIMoSBevelHypoidSingleRotationAngleResult":
        """Cast to another type.

        Returns:
            _Cast_KIMoSBevelHypoidSingleRotationAngleResult
        """
        return _Cast_KIMoSBevelHypoidSingleRotationAngleResult(self)
