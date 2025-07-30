"""ISO1328AccuracyGrades"""

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
from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
    _1257,
)

_ISO1328_ACCURACY_GRADES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "ISO1328AccuracyGrades",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _403

    Self = TypeVar("Self", bound="ISO1328AccuracyGrades")
    CastSelf = TypeVar(
        "CastSelf", bound="ISO1328AccuracyGrades._Cast_ISO1328AccuracyGrades"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO1328AccuracyGrades",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO1328AccuracyGrades:
    """Special nested class for casting ISO1328AccuracyGrades to subclasses."""

    __parent__: "ISO1328AccuracyGrades"

    @property
    def cylindrical_accuracy_grades(
        self: "CastSelf",
    ) -> "_1257.CylindricalAccuracyGrades":
        return self.__parent__._cast(_1257.CylindricalAccuracyGrades)

    @property
    def accuracy_grades(self: "CastSelf") -> "_403.AccuracyGrades":
        from mastapy._private.gears import _403

        return self.__parent__._cast(_403.AccuracyGrades)

    @property
    def iso1328_accuracy_grades(self: "CastSelf") -> "ISO1328AccuracyGrades":
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
class ISO1328AccuracyGrades(_1257.CylindricalAccuracyGrades):
    """ISO1328AccuracyGrades

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO1328_ACCURACY_GRADES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def helix_iso_quality_grade(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "HelixISOQualityGrade")

        if temp is None:
            return 0

        return temp

    @helix_iso_quality_grade.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_iso_quality_grade(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "HelixISOQualityGrade", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def pitch_iso_quality_grade(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PitchISOQualityGrade")

        if temp is None:
            return 0

        return temp

    @pitch_iso_quality_grade.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_iso_quality_grade(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PitchISOQualityGrade", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def profile_iso_quality_grade(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ProfileISOQualityGrade")

        if temp is None:
            return 0

        return temp

    @profile_iso_quality_grade.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_iso_quality_grade(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileISOQualityGrade",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def radial_iso_quality_grade(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "RadialISOQualityGrade")

        if temp is None:
            return 0

        return temp

    @radial_iso_quality_grade.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_iso_quality_grade(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialISOQualityGrade",
            int(value) if value is not None else 0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ISO1328AccuracyGrades":
        """Cast to another type.

        Returns:
            _Cast_ISO1328AccuracyGrades
        """
        return _Cast_ISO1328AccuracyGrades(self)
