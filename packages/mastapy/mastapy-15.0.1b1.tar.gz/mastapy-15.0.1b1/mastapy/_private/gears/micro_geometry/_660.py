"""BiasModification"""

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
from mastapy._private.gears.micro_geometry import _670

_BIAS_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.MicroGeometry", "BiasModification"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical.micro_geometry import _1292
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1206

    Self = TypeVar("Self", bound="BiasModification")
    CastSelf = TypeVar("CastSelf", bound="BiasModification._Cast_BiasModification")


__docformat__ = "restructuredtext en"
__all__ = ("BiasModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BiasModification:
    """Special nested class for casting BiasModification to subclasses."""

    __parent__: "BiasModification"

    @property
    def modification(self: "CastSelf") -> "_670.Modification":
        return self.__parent__._cast(_670.Modification)

    @property
    def cylindrical_gear_bias_modification(
        self: "CastSelf",
    ) -> "_1206.CylindricalGearBiasModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1206

        return self.__parent__._cast(_1206.CylindricalGearBiasModification)

    @property
    def conical_gear_bias_modification(
        self: "CastSelf",
    ) -> "_1292.ConicalGearBiasModification":
        from mastapy._private.gears.gear_designs.conical.micro_geometry import _1292

        return self.__parent__._cast(_1292.ConicalGearBiasModification)

    @property
    def bias_modification(self: "CastSelf") -> "BiasModification":
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
class BiasModification(_670.Modification):
    """BiasModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BIAS_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def lead_evaluation_left_limit_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LeadEvaluationLeftLimitFactor")

        if temp is None:
            return 0.0

        return temp

    @lead_evaluation_left_limit_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def lead_evaluation_left_limit_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LeadEvaluationLeftLimitFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lead_evaluation_right_limit_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LeadEvaluationRightLimitFactor")

        if temp is None:
            return 0.0

        return temp

    @lead_evaluation_right_limit_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def lead_evaluation_right_limit_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LeadEvaluationRightLimitFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_lower_limit_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationLowerLimitFactor")

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_lower_limit_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_lower_limit_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationLowerLimitFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_upper_limit_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationUpperLimitFactor")

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_upper_limit_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_upper_limit_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationUpperLimitFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_factor_for_0_bias_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileFactorFor0BiasRelief")

        if temp is None:
            return 0.0

        return temp

    @profile_factor_for_0_bias_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_factor_for_0_bias_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileFactorFor0BiasRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relief_at_left_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReliefAtLeftLimit")

        if temp is None:
            return 0.0

        return temp

    @relief_at_left_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def relief_at_left_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReliefAtLeftLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relief_at_right_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReliefAtRightLimit")

        if temp is None:
            return 0.0

        return temp

    @relief_at_right_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def relief_at_right_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReliefAtRightLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BiasModification":
        """Cast to another type.

        Returns:
            _Cast_BiasModification
        """
        return _Cast_BiasModification(self)
