"""DetailedSplineJointSettings"""

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

_DETAILED_SPLINE_JOINT_SETTINGS = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "DetailedSplineJointSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DetailedSplineJointSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DetailedSplineJointSettings._Cast_DetailedSplineJointSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DetailedSplineJointSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DetailedSplineJointSettings:
    """Special nested class for casting DetailedSplineJointSettings to subclasses."""

    __parent__: "DetailedSplineJointSettings"

    @property
    def detailed_spline_joint_settings(
        self: "CastSelf",
    ) -> "DetailedSplineJointSettings":
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
class DetailedSplineJointSettings(_0.APIBase):
    """DetailedSplineJointSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DETAILED_SPLINE_JOINT_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def required_safety_factor_for_compressive_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForCompressiveStress"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_compressive_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def required_safety_factor_for_compressive_stress(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForCompressiveStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def required_safety_factor_for_ring_bursting(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForRingBursting"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_ring_bursting.setter
    @exception_bridge
    @enforce_parameter_types
    def required_safety_factor_for_ring_bursting(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForRingBursting",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def required_safety_factor_for_root_bending_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForRootBendingStress"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_root_bending_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def required_safety_factor_for_root_bending_stress(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForRootBendingStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def required_safety_factor_for_tooth_shearing_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForToothShearingStress"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_tooth_shearing_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def required_safety_factor_for_tooth_shearing_stress(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForToothShearingStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def required_safety_factor_for_torsional_failure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForTorsionalFailure"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_torsional_failure.setter
    @exception_bridge
    @enforce_parameter_types
    def required_safety_factor_for_torsional_failure(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForTorsionalFailure",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def required_safety_factor_for_wear_and_fretting(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForWearAndFretting"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_wear_and_fretting.setter
    @exception_bridge
    @enforce_parameter_types
    def required_safety_factor_for_wear_and_fretting(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForWearAndFretting",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_DetailedSplineJointSettings":
        """Cast to another type.

        Returns:
            _Cast_DetailedSplineJointSettings
        """
        return _Cast_DetailedSplineJointSettings(self)
