"""AGMA2000A88AccuracyGrader"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
    _1255,
)

_AGMA2000A88_ACCURACY_GRADER = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "AGMA2000A88AccuracyGrader",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1254,
        _1264,
    )

    Self = TypeVar("Self", bound="AGMA2000A88AccuracyGrader")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMA2000A88AccuracyGrader._Cast_AGMA2000A88AccuracyGrader"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMA2000A88AccuracyGrader",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMA2000A88AccuracyGrader:
    """Special nested class for casting AGMA2000A88AccuracyGrader to subclasses."""

    __parent__: "AGMA2000A88AccuracyGrader"

    @property
    def cylindrical_accuracy_grader(
        self: "CastSelf",
    ) -> "_1255.CylindricalAccuracyGrader":
        return self.__parent__._cast(_1255.CylindricalAccuracyGrader)

    @property
    def customer_102agma2000_accuracy_grader(
        self: "CastSelf",
    ) -> "_1254.Customer102AGMA2000AccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1254,
        )

        return self.__parent__._cast(_1254.Customer102AGMA2000AccuracyGrader)

    @property
    def agma2000a88_accuracy_grader(self: "CastSelf") -> "AGMA2000A88AccuracyGrader":
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
class AGMA2000A88AccuracyGrader(_1255.CylindricalAccuracyGrader):
    """AGMA2000A88AccuracyGrader

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA2000A88_ACCURACY_GRADER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def adjusted_number_of_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedNumberOfTeeth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_pitch_variation(self: "Self") -> "_1264.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowablePitchVariation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def profile_tolerance(self: "Self") -> "_1264.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def radial_runout_tolerance(self: "Self") -> "_1264.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialRunoutTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def tooth_alignment_tolerance(self: "Self") -> "_1264.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothAlignmentTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def toothto_tooth_composite_tolerance(self: "Self") -> "_1264.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothtoToothCompositeTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def total_composite_tolerance(self: "Self") -> "_1264.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalCompositeTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AGMA2000A88AccuracyGrader":
        """Cast to another type.

        Returns:
            _Cast_AGMA2000A88AccuracyGrader
        """
        return _Cast_AGMA2000A88AccuracyGrader(self)
