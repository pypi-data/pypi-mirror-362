"""AGMA20151AccuracyGrades"""

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

_AGMA20151_ACCURACY_GRADES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "AGMA20151AccuracyGrades",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _403

    Self = TypeVar("Self", bound="AGMA20151AccuracyGrades")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMA20151AccuracyGrades._Cast_AGMA20151AccuracyGrades"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMA20151AccuracyGrades",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMA20151AccuracyGrades:
    """Special nested class for casting AGMA20151AccuracyGrades to subclasses."""

    __parent__: "AGMA20151AccuracyGrades"

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
    def agma20151_accuracy_grades(self: "CastSelf") -> "AGMA20151AccuracyGrades":
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
class AGMA20151AccuracyGrades(_1257.CylindricalAccuracyGrades):
    """AGMA20151AccuracyGrades

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA20151_ACCURACY_GRADES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def helix_agma_quality_grade_new(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "HelixAGMAQualityGradeNew")

        if temp is None:
            return 0

        return temp

    @helix_agma_quality_grade_new.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_agma_quality_grade_new(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HelixAGMAQualityGradeNew",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def helix_agma_quality_grade_old(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "HelixAGMAQualityGradeOld")

        if temp is None:
            return 0

        return temp

    @helix_agma_quality_grade_old.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_agma_quality_grade_old(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HelixAGMAQualityGradeOld",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def pitch_agma_quality_grade_new(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PitchAGMAQualityGradeNew")

        if temp is None:
            return 0

        return temp

    @pitch_agma_quality_grade_new.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_agma_quality_grade_new(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PitchAGMAQualityGradeNew",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def pitch_agma_quality_grade_old(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PitchAGMAQualityGradeOld")

        if temp is None:
            return 0

        return temp

    @pitch_agma_quality_grade_old.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_agma_quality_grade_old(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PitchAGMAQualityGradeOld",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def profile_agma_quality_grade_new(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ProfileAGMAQualityGradeNew")

        if temp is None:
            return 0

        return temp

    @profile_agma_quality_grade_new.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_agma_quality_grade_new(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileAGMAQualityGradeNew",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def profile_agma_quality_grade_old(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ProfileAGMAQualityGradeOld")

        if temp is None:
            return 0

        return temp

    @profile_agma_quality_grade_old.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_agma_quality_grade_old(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileAGMAQualityGradeOld",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def radial_agma_quality_grade_new(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "RadialAGMAQualityGradeNew")

        if temp is None:
            return 0

        return temp

    @radial_agma_quality_grade_new.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_agma_quality_grade_new(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialAGMAQualityGradeNew",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def radial_agma_quality_grade_old(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "RadialAGMAQualityGradeOld")

        if temp is None:
            return 0

        return temp

    @radial_agma_quality_grade_old.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_agma_quality_grade_old(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialAGMAQualityGradeOld",
            int(value) if value is not None else 0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AGMA20151AccuracyGrades":
        """Cast to another type.

        Returns:
            _Cast_AGMA20151AccuracyGrades
        """
        return _Cast_AGMA20151AccuracyGrades(self)
