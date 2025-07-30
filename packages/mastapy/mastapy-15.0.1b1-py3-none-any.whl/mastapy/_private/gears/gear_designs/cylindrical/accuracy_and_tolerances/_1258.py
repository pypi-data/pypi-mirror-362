"""CylindricalGearAccuracyTolerances"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CYLINDRICAL_GEAR_ACCURACY_TOLERANCES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "CylindricalGearAccuracyTolerances",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1250,
        _1251,
        _1253,
        _1260,
        _1261,
    )

    Self = TypeVar("Self", bound="CylindricalGearAccuracyTolerances")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearAccuracyTolerances._Cast_CylindricalGearAccuracyTolerances",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearAccuracyTolerances",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearAccuracyTolerances:
    """Special nested class for casting CylindricalGearAccuracyTolerances to subclasses."""

    __parent__: "CylindricalGearAccuracyTolerances"

    @property
    def cylindrical_gear_accuracy_tolerances(
        self: "CastSelf",
    ) -> "CylindricalGearAccuracyTolerances":
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
class CylindricalGearAccuracyTolerances(_0.APIBase):
    """CylindricalGearAccuracyTolerances

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_ACCURACY_TOLERANCES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def agma2000_gear_accuracy_tolerances(
        self: "Self",
    ) -> "_1250.AGMA2000A88AccuracyGrader":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.AGMA2000A88AccuracyGrader

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AGMA2000GearAccuracyTolerances")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def agma2015_gear_accuracy_tolerances(
        self: "Self",
    ) -> "_1251.AGMA20151A01AccuracyGrader":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.AGMA20151A01AccuracyGrader

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AGMA2015GearAccuracyTolerances")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def agmaiso13281_gear_accuracy_tolerances(
        self: "Self",
    ) -> "_1253.AGMAISO13281B14AccuracyGrader":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.AGMAISO13281B14AccuracyGrader

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAISO13281GearAccuracyTolerances"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def iso132811995_gear_accuracy_tolerances(
        self: "Self",
    ) -> "_1260.ISO132811995AccuracyGrader":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.ISO132811995AccuracyGrader

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO132811995GearAccuracyTolerances"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def iso132812013_gear_accuracy_tolerances(
        self: "Self",
    ) -> "_1261.ISO132812013AccuracyGrader":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.ISO132812013AccuracyGrader

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO132812013GearAccuracyTolerances"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearAccuracyTolerances":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearAccuracyTolerances
        """
        return _Cast_CylindricalGearAccuracyTolerances(self)
