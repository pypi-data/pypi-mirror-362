"""CADToothAndSlot"""

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
from mastapy._private.electric_machines import _1366

_CAD_TOOTH_AND_SLOT = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "CADToothAndSlot"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import _1408, _1450

    Self = TypeVar("Self", bound="CADToothAndSlot")
    CastSelf = TypeVar("CastSelf", bound="CADToothAndSlot._Cast_CADToothAndSlot")


__docformat__ = "restructuredtext en"
__all__ = ("CADToothAndSlot",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CADToothAndSlot:
    """Special nested class for casting CADToothAndSlot to subclasses."""

    __parent__: "CADToothAndSlot"

    @property
    def abstract_tooth_and_slot(self: "CastSelf") -> "_1366.AbstractToothAndSlot":
        return self.__parent__._cast(_1366.AbstractToothAndSlot)

    @property
    def cad_tooth_and_slot(self: "CastSelf") -> "CADToothAndSlot":
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
class CADToothAndSlot(_1366.AbstractToothAndSlot):
    """CADToothAndSlot

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAD_TOOTH_AND_SLOT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def individual_conductor_specification_source(
        self: "Self",
    ) -> "_1408.IndividualConductorSpecificationSource":
        """mastapy.electric_machines.IndividualConductorSpecificationSource"""
        temp = pythonnet_property_get(
            self.wrapped, "IndividualConductorSpecificationSource"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.IndividualConductorSpecificationSource"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1408",
            "IndividualConductorSpecificationSource",
        )(value)

    @individual_conductor_specification_source.setter
    @exception_bridge
    @enforce_parameter_types
    def individual_conductor_specification_source(
        self: "Self", value: "_1408.IndividualConductorSpecificationSource"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.IndividualConductorSpecificationSource",
        )
        pythonnet_property_set(
            self.wrapped, "IndividualConductorSpecificationSource", value
        )

    @property
    @exception_bridge
    def conductors(self: "Self") -> "List[_1450.WindingConductor]":
        """List[mastapy.electric_machines.WindingConductor]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Conductors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CADToothAndSlot":
        """Cast to another type.

        Returns:
            _Cast_CADToothAndSlot
        """
        return _Cast_CADToothAndSlot(self)
