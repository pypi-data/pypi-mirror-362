"""SAESplineHalfRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.detailed_rigid_connectors.splines.ratings import _1616

_SAE_SPLINE_HALF_RATING = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings", "SAESplineHalfRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SAESplineHalfRating")
    CastSelf = TypeVar(
        "CastSelf", bound="SAESplineHalfRating._Cast_SAESplineHalfRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SAESplineHalfRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SAESplineHalfRating:
    """Special nested class for casting SAESplineHalfRating to subclasses."""

    __parent__: "SAESplineHalfRating"

    @property
    def spline_half_rating(self: "CastSelf") -> "_1616.SplineHalfRating":
        return self.__parent__._cast(_1616.SplineHalfRating)

    @property
    def sae_spline_half_rating(self: "CastSelf") -> "SAESplineHalfRating":
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
class SAESplineHalfRating(_1616.SplineHalfRating):
    """SAESplineHalfRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SAE_SPLINE_HALF_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_compressive_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableCompressiveStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_shear_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableShearStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_tensile_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableTensileStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def equivalent_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EquivalentStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_damage_for_compressive_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueDamageForCompressiveStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_damage_for_equivalent_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FatigueDamageForEquivalentRootStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_damage_for_tooth_shearing_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FatigueDamageForToothShearingStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_allowable_compressive_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumAllowableCompressiveStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_allowable_shear_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumAllowableShearStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_compressive_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForCompressiveStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_equivalent_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SafetyFactorForEquivalentRootStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_tooth_shearing_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SafetyFactorForToothShearingStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_concentration_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressConcentrationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torsional_shear_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorsionalShearStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SAESplineHalfRating":
        """Cast to another type.

        Returns:
            _Cast_SAESplineHalfRating
        """
        return _Cast_SAESplineHalfRating(self)
