"""GeneralElectricMachineMaterial"""

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
from mastapy._private.materials import _358

_GENERAL_ELECTRIC_MACHINE_MATERIAL = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "GeneralElectricMachineMaterial"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="GeneralElectricMachineMaterial")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeneralElectricMachineMaterial._Cast_GeneralElectricMachineMaterial",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeneralElectricMachineMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeneralElectricMachineMaterial:
    """Special nested class for casting GeneralElectricMachineMaterial to subclasses."""

    __parent__: "GeneralElectricMachineMaterial"

    @property
    def material(self: "CastSelf") -> "_358.Material":
        return self.__parent__._cast(_358.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def general_electric_machine_material(
        self: "CastSelf",
    ) -> "GeneralElectricMachineMaterial":
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
class GeneralElectricMachineMaterial(_358.Material):
    """GeneralElectricMachineMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GENERAL_ELECTRIC_MACHINE_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def relative_permeability(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RelativePermeability")

        if temp is None:
            return 0.0

        return temp

    @relative_permeability.setter
    @exception_bridge
    @enforce_parameter_types
    def relative_permeability(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RelativePermeability",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GeneralElectricMachineMaterial":
        """Cast to another type.

        Returns:
            _Cast_GeneralElectricMachineMaterial
        """
        return _Cast_GeneralElectricMachineMaterial(self)
