"""DIN3967SystemOfGearFits"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DIN3967_SYSTEM_OF_GEAR_FITS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "DIN3967SystemOfGearFits",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1153, _1154

    Self = TypeVar("Self", bound="DIN3967SystemOfGearFits")
    CastSelf = TypeVar(
        "CastSelf", bound="DIN3967SystemOfGearFits._Cast_DIN3967SystemOfGearFits"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DIN3967SystemOfGearFits",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DIN3967SystemOfGearFits:
    """Special nested class for casting DIN3967SystemOfGearFits to subclasses."""

    __parent__: "DIN3967SystemOfGearFits"

    @property
    def din3967_system_of_gear_fits(self: "CastSelf") -> "DIN3967SystemOfGearFits":
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
class DIN3967SystemOfGearFits(_0.APIBase):
    """DIN3967SystemOfGearFits

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DIN3967_SYSTEM_OF_GEAR_FITS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def tooth_thickness_reduction_allowance(
        self: "Self",
    ) -> "_1153.DIN3967AllowanceSeries":
        """mastapy.gears.gear_designs.cylindrical.DIN3967AllowanceSeries"""
        temp = pythonnet_property_get(self.wrapped, "ToothThicknessReductionAllowance")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.DIN3967AllowanceSeries"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1153",
            "DIN3967AllowanceSeries",
        )(value)

    @tooth_thickness_reduction_allowance.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_thickness_reduction_allowance(
        self: "Self", value: "_1153.DIN3967AllowanceSeries"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.DIN3967AllowanceSeries"
        )
        pythonnet_property_set(self.wrapped, "ToothThicknessReductionAllowance", value)

    @property
    @exception_bridge
    def tooth_thickness_tolerance(self: "Self") -> "_1154.DIN3967ToleranceSeries":
        """mastapy.gears.gear_designs.cylindrical.DIN3967ToleranceSeries"""
        temp = pythonnet_property_get(self.wrapped, "ToothThicknessTolerance")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.DIN3967ToleranceSeries"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1154",
            "DIN3967ToleranceSeries",
        )(value)

    @tooth_thickness_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_thickness_tolerance(
        self: "Self", value: "_1154.DIN3967ToleranceSeries"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.DIN3967ToleranceSeries"
        )
        pythonnet_property_set(self.wrapped, "ToothThicknessTolerance", value)

    @property
    def cast_to(self: "Self") -> "_Cast_DIN3967SystemOfGearFits":
        """Cast to another type.

        Returns:
            _Cast_DIN3967SystemOfGearFits
        """
        return _Cast_DIN3967SystemOfGearFits(self)
