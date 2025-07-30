"""SAESplineTolerances"""

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
)

_SAE_SPLINE_TOLERANCES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.TolerancesAndDeviations",
    "SAESplineTolerances",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SAESplineTolerances")
    CastSelf = TypeVar(
        "CastSelf", bound="SAESplineTolerances._Cast_SAESplineTolerances"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SAESplineTolerances",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SAESplineTolerances:
    """Special nested class for casting SAESplineTolerances to subclasses."""

    __parent__: "SAESplineTolerances"

    @property
    def sae_spline_tolerances(self: "CastSelf") -> "SAESplineTolerances":
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
class SAESplineTolerances(_0.APIBase):
    """SAESplineTolerances

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SAE_SPLINE_TOLERANCES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def internal_major_diameter_tolerance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InternalMajorDiameterTolerance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lead_variation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadVariation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def machining_variation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MachiningVariation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def major_diameter_tolerance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MajorDiameterTolerance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minor_diameter_tolerance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinorDiameterTolerance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def multiplier_f(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MultiplierF")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def profile_variation_f_fm(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileVariationF_fm")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def profile_variation_f_fp(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileVariationF_fp")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_index_variation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalIndexVariation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def variation_tolerance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VariationTolerance")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SAESplineTolerances":
        """Cast to another type.

        Returns:
            _Cast_SAESplineTolerances
        """
        return _Cast_SAESplineTolerances(self)
