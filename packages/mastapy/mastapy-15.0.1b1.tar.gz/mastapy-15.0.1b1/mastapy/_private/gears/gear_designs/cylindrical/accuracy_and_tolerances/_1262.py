"""ISO1328AccuracyGraderCommon"""

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
    _1256,
)

_ISO1328_ACCURACY_GRADER_COMMON = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "ISO1328AccuracyGraderCommon",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1253,
        _1255,
        _1260,
        _1261,
        _1264,
    )

    Self = TypeVar("Self", bound="ISO1328AccuracyGraderCommon")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO1328AccuracyGraderCommon._Cast_ISO1328AccuracyGraderCommon",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO1328AccuracyGraderCommon",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO1328AccuracyGraderCommon:
    """Special nested class for casting ISO1328AccuracyGraderCommon to subclasses."""

    __parent__: "ISO1328AccuracyGraderCommon"

    @property
    def cylindrical_accuracy_grader_with_profile_form_and_slope(
        self: "CastSelf",
    ) -> "_1256.CylindricalAccuracyGraderWithProfileFormAndSlope":
        return self.__parent__._cast(
            _1256.CylindricalAccuracyGraderWithProfileFormAndSlope
        )

    @property
    def cylindrical_accuracy_grader(
        self: "CastSelf",
    ) -> "_1255.CylindricalAccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1255,
        )

        return self.__parent__._cast(_1255.CylindricalAccuracyGrader)

    @property
    def agmaiso13281b14_accuracy_grader(
        self: "CastSelf",
    ) -> "_1253.AGMAISO13281B14AccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1253,
        )

        return self.__parent__._cast(_1253.AGMAISO13281B14AccuracyGrader)

    @property
    def iso132811995_accuracy_grader(
        self: "CastSelf",
    ) -> "_1260.ISO132811995AccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1260,
        )

        return self.__parent__._cast(_1260.ISO132811995AccuracyGrader)

    @property
    def iso132812013_accuracy_grader(
        self: "CastSelf",
    ) -> "_1261.ISO132812013AccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1261,
        )

        return self.__parent__._cast(_1261.ISO132812013AccuracyGrader)

    @property
    def iso1328_accuracy_grader_common(
        self: "CastSelf",
    ) -> "ISO1328AccuracyGraderCommon":
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
class ISO1328AccuracyGraderCommon(
    _1256.CylindricalAccuracyGraderWithProfileFormAndSlope
):
    """ISO1328AccuracyGraderCommon

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO1328_ACCURACY_GRADER_COMMON

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def base_pitch_deviation(self: "Self") -> "_1264.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasePitchDeviation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def toothto_tooth_radial_composite_deviation(
        self: "Self",
    ) -> "_1264.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothtoToothRadialCompositeDeviation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def total_radial_composite_deviation(self: "Self") -> "_1264.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalRadialCompositeDeviation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ISO1328AccuracyGraderCommon":
        """Cast to another type.

        Returns:
            _Cast_ISO1328AccuracyGraderCommon
        """
        return _Cast_ISO1328AccuracyGraderCommon(self)
