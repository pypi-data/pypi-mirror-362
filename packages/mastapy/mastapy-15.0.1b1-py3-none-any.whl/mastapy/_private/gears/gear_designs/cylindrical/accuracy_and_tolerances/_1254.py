"""Customer102AGMA2000AccuracyGrader"""

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
from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
    _1250,
)

_CUSTOMER_102AGMA2000_ACCURACY_GRADER = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "Customer102AGMA2000AccuracyGrader",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1255,
    )

    Self = TypeVar("Self", bound="Customer102AGMA2000AccuracyGrader")
    CastSelf = TypeVar(
        "CastSelf",
        bound="Customer102AGMA2000AccuracyGrader._Cast_Customer102AGMA2000AccuracyGrader",
    )


__docformat__ = "restructuredtext en"
__all__ = ("Customer102AGMA2000AccuracyGrader",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Customer102AGMA2000AccuracyGrader:
    """Special nested class for casting Customer102AGMA2000AccuracyGrader to subclasses."""

    __parent__: "Customer102AGMA2000AccuracyGrader"

    @property
    def agma2000a88_accuracy_grader(
        self: "CastSelf",
    ) -> "_1250.AGMA2000A88AccuracyGrader":
        return self.__parent__._cast(_1250.AGMA2000A88AccuracyGrader)

    @property
    def cylindrical_accuracy_grader(
        self: "CastSelf",
    ) -> "_1255.CylindricalAccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1255,
        )

        return self.__parent__._cast(_1255.CylindricalAccuracyGrader)

    @property
    def customer_102agma2000_accuracy_grader(
        self: "CastSelf",
    ) -> "Customer102AGMA2000AccuracyGrader":
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
class Customer102AGMA2000AccuracyGrader(_1250.AGMA2000A88AccuracyGrader):
    """Customer102AGMA2000AccuracyGrader

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOMER_102AGMA2000_ACCURACY_GRADER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def composite_tolerance_toothto_tooth_from_customer_102g_design(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CompositeToleranceToothtoToothFromCustomer102GDesign"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_variation_allowable_from_customer_102g_design(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PitchVariationAllowableFromCustomer102GDesign"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def runout_radial_tolerance_from_customer_102g_design(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RunoutRadialToleranceFromCustomer102GDesign"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_alignment_tolerance_from_customer_102g_design(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothAlignmentToleranceFromCustomer102GDesign"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_composite_tolerance_from_customer_102g_design(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalCompositeToleranceFromCustomer102GDesign"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_Customer102AGMA2000AccuracyGrader":
        """Cast to another type.

        Returns:
            _Cast_Customer102AGMA2000AccuracyGrader
        """
        return _Cast_Customer102AGMA2000AccuracyGrader(self)
