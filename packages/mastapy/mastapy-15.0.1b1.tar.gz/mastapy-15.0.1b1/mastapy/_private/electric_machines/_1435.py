"""Stator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.electric_machines import _1365

_STATOR = python_net_import("SMT.MastaAPI.ElectricMachines", "Stator")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import _1436, _1442

    Self = TypeVar("Self", bound="Stator")
    CastSelf = TypeVar("CastSelf", bound="Stator._Cast_Stator")


__docformat__ = "restructuredtext en"
__all__ = ("Stator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Stator:
    """Special nested class for casting Stator to subclasses."""

    __parent__: "Stator"

    @property
    def abstract_stator(self: "CastSelf") -> "_1365.AbstractStator":
        return self.__parent__._cast(_1365.AbstractStator)

    @property
    def stator(self: "CastSelf") -> "Stator":
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
class Stator(_1365.AbstractStator):
    """Stator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_stator_cutout_specifications(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfStatorCutoutSpecifications"
        )

        if temp is None:
            return 0

        return temp

    @number_of_stator_cutout_specifications.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_stator_cutout_specifications(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfStatorCutoutSpecifications",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def radius_at_mid_coil_height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadiusAtMidCoilHeight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stator_cutout_specifications(
        self: "Self",
    ) -> "List[_1436.StatorCutoutSpecification]":
        """List[mastapy.electric_machines.StatorCutoutSpecification]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorCutoutSpecifications")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def tooth_and_slot(self: "Self") -> "_1442.ToothAndSlot":
        """mastapy.electric_machines.ToothAndSlot

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothAndSlot")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_Stator":
        """Cast to another type.

        Returns:
            _Cast_Stator
        """
        return _Cast_Stator(self)
