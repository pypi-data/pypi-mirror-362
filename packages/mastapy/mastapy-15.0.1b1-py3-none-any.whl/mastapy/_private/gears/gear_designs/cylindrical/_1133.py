"""CylindricalGearPinionTypeCutter"""

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
from mastapy._private.gears.gear_designs.cylindrical import _1116

_CYLINDRICAL_GEAR_PINION_TYPE_CUTTER = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearPinionTypeCutter"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical import _1134

    Self = TypeVar("Self", bound="CylindricalGearPinionTypeCutter")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearPinionTypeCutter._Cast_CylindricalGearPinionTypeCutter",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearPinionTypeCutter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearPinionTypeCutter:
    """Special nested class for casting CylindricalGearPinionTypeCutter to subclasses."""

    __parent__: "CylindricalGearPinionTypeCutter"

    @property
    def cylindrical_gear_abstract_rack(
        self: "CastSelf",
    ) -> "_1116.CylindricalGearAbstractRack":
        return self.__parent__._cast(_1116.CylindricalGearAbstractRack)

    @property
    def cylindrical_gear_pinion_type_cutter(
        self: "CastSelf",
    ) -> "CylindricalGearPinionTypeCutter":
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
class CylindricalGearPinionTypeCutter(_1116.CylindricalGearAbstractRack):
    """CylindricalGearPinionTypeCutter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_PINION_TYPE_CUTTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def nominal_addendum_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NominalAddendumFactor")

        if temp is None:
            return 0.0

        return temp

    @nominal_addendum_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def nominal_addendum_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NominalAddendumFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def nominal_dedendum_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalDedendumFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def profile_shift_coefficient(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ProfileShiftCoefficient")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @profile_shift_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_shift_coefficient(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ProfileShiftCoefficient", value)

    @property
    @exception_bridge
    def left_flank(self: "Self") -> "_1134.CylindricalGearPinionTypeCutterFlank":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearPinionTypeCutterFlank

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank(self: "Self") -> "_1134.CylindricalGearPinionTypeCutterFlank":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearPinionTypeCutterFlank

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearPinionTypeCutter":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearPinionTypeCutter
        """
        return _Cast_CylindricalGearPinionTypeCutter(self)
