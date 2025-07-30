"""PermissibleContinuousAxialLoadResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_PERMISSIBLE_CONTINUOUS_AXIAL_LOAD_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "PermissibleContinuousAxialLoadResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2148

    Self = TypeVar("Self", bound="PermissibleContinuousAxialLoadResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PermissibleContinuousAxialLoadResults._Cast_PermissibleContinuousAxialLoadResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PermissibleContinuousAxialLoadResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PermissibleContinuousAxialLoadResults:
    """Special nested class for casting PermissibleContinuousAxialLoadResults to subclasses."""

    __parent__: "PermissibleContinuousAxialLoadResults"

    @property
    def permissible_continuous_axial_load_results(
        self: "CastSelf",
    ) -> "PermissibleContinuousAxialLoadResults":
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
class PermissibleContinuousAxialLoadResults(_0.APIBase):
    """PermissibleContinuousAxialLoadResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PERMISSIBLE_CONTINUOUS_AXIAL_LOAD_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_axial_load_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableAxialLoadFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def allowable_constant_axial_load_ntn(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableConstantAxialLoadNTN")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_intermittent_axial_load_ntn(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableIntermittentAxialLoadNTN")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_momentary_axial_load_ntn(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableMomentaryAxialLoadNTN")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def axial_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def calculation_method(self: "Self") -> "_2148.CylindricalRollerMaxAxialLoadMethod":
        """mastapy.bearings.bearing_results.CylindricalRollerMaxAxialLoadMethod

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Bearings.BearingResults.CylindricalRollerMaxAxialLoadMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results._2148",
            "CylindricalRollerMaxAxialLoadMethod",
        )(value)

    @property
    @exception_bridge
    def capacity_lubrication_factor_for_permissible_axial_load_grease(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CapacityLubricationFactorForPermissibleAxialLoadGrease"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def capacity_lubrication_factor_for_permissible_axial_load_oil(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CapacityLubricationFactorForPermissibleAxialLoadOil"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def diameter_exponent_factor_for_permissible_axial_load(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DiameterExponentFactorForPermissibleAxialLoad"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def diameter_scaling_factor_for_permissible_axial_load(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DiameterScalingFactorForPermissibleAxialLoad"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def maximum_permissible_axial_load_schaeffler(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPermissibleAxialLoadSchaeffler"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_axial_load_schaeffler(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleAxialLoadSchaeffler")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_axial_load_dimension_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadDimensionFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def permissible_axial_load_internal_dimension_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadInternalDimensionFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def permissible_axial_load_under_shaft_deflection_schaeffler(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadUnderShaftDeflectionSchaeffler"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_axial_load_for_brief_periods_skf(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadForBriefPeriodsSKF"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_axial_load_for_occasional_peak_loads_skf(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadForOccasionalPeakLoadsSKF"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_axial_loading_nachi(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleAxialLoadingNACHI")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_continuous_axial_load_skf(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleContinuousAxialLoadSKF")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_load_lubrication_factor_for_permissible_axial_load_grease(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RadialLoadLubricationFactorForPermissibleAxialLoadGrease"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def radial_load_lubrication_factor_for_permissible_axial_load_oil(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RadialLoadLubricationFactorForPermissibleAxialLoadOil"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_PermissibleContinuousAxialLoadResults":
        """Cast to another type.

        Returns:
            _Cast_PermissibleContinuousAxialLoadResults
        """
        return _Cast_PermissibleContinuousAxialLoadResults(self)
