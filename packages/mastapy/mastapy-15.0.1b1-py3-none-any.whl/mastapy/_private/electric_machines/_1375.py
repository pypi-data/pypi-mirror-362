"""CADWoundFieldSynchronousRotor"""

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
from mastapy._private.electric_machines import _1372

_CAD_WOUND_FIELD_SYNCHRONOUS_ROTOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "CADWoundFieldSynchronousRotor"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import _1369, _1399, _1429

    Self = TypeVar("Self", bound="CADWoundFieldSynchronousRotor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CADWoundFieldSynchronousRotor._Cast_CADWoundFieldSynchronousRotor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CADWoundFieldSynchronousRotor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CADWoundFieldSynchronousRotor:
    """Special nested class for casting CADWoundFieldSynchronousRotor to subclasses."""

    __parent__: "CADWoundFieldSynchronousRotor"

    @property
    def cad_rotor(self: "CastSelf") -> "_1372.CADRotor":
        return self.__parent__._cast(_1372.CADRotor)

    @property
    def rotor(self: "CastSelf") -> "_1429.Rotor":
        from mastapy._private.electric_machines import _1429

        return self.__parent__._cast(_1429.Rotor)

    @property
    def cad_wound_field_synchronous_rotor(
        self: "CastSelf",
    ) -> "CADWoundFieldSynchronousRotor":
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
class CADWoundFieldSynchronousRotor(_1372.CADRotor):
    """CADWoundFieldSynchronousRotor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAD_WOUND_FIELD_SYNCHRONOUS_ROTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_field_winding_regions(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfFieldWindingRegions")

        if temp is None:
            return 0

        return temp

    @number_of_field_winding_regions.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_field_winding_regions(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfFieldWindingRegions",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def field_winding_specification(
        self: "Self",
    ) -> "_1399.FieldWindingSpecificationBase":
        """mastapy.electric_machines.FieldWindingSpecificationBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FieldWindingSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cad_field_winding_specifications(
        self: "Self",
    ) -> "List[_1369.CADFieldWindingSpecification]":
        """List[mastapy.electric_machines.CADFieldWindingSpecification]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CADFieldWindingSpecifications")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CADWoundFieldSynchronousRotor":
        """Cast to another type.

        Returns:
            _Cast_CADWoundFieldSynchronousRotor
        """
        return _Cast_CADWoundFieldSynchronousRotor(self)
