"""CylindricalGearLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.load_case import _976

_CYLINDRICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase.Cylindrical", "CylindricalGearLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.analysis import _1335, _1338

    Self = TypeVar("Self", bound="CylindricalGearLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearLoadCase._Cast_CylindricalGearLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearLoadCase:
    """Special nested class for casting CylindricalGearLoadCase to subclasses."""

    __parent__: "CylindricalGearLoadCase"

    @property
    def gear_load_case_base(self: "CastSelf") -> "_976.GearLoadCaseBase":
        return self.__parent__._cast(_976.GearLoadCaseBase)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1338

        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "CylindricalGearLoadCase":
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
class CylindricalGearLoadCase(_976.GearLoadCaseBase):
    """CylindricalGearLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def reversed_bending_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ReversedBendingFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @reversed_bending_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def reversed_bending_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ReversedBendingFactor", value)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearLoadCase
        """
        return _Cast_CylindricalGearLoadCase(self)
