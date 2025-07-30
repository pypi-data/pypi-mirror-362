"""SurfacePermanentMagnetMachine"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines import _1421

_SURFACE_PERMANENT_MAGNET_MACHINE = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "SurfacePermanentMagnetMachine"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1386, _1387, _1440

    Self = TypeVar("Self", bound="SurfacePermanentMagnetMachine")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SurfacePermanentMagnetMachine._Cast_SurfacePermanentMagnetMachine",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SurfacePermanentMagnetMachine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SurfacePermanentMagnetMachine:
    """Special nested class for casting SurfacePermanentMagnetMachine to subclasses."""

    __parent__: "SurfacePermanentMagnetMachine"

    @property
    def non_cad_electric_machine_detail(
        self: "CastSelf",
    ) -> "_1421.NonCADElectricMachineDetail":
        return self.__parent__._cast(_1421.NonCADElectricMachineDetail)

    @property
    def electric_machine_detail(self: "CastSelf") -> "_1387.ElectricMachineDetail":
        from mastapy._private.electric_machines import _1387

        return self.__parent__._cast(_1387.ElectricMachineDetail)

    @property
    def electric_machine_design_base(
        self: "CastSelf",
    ) -> "_1386.ElectricMachineDesignBase":
        from mastapy._private.electric_machines import _1386

        return self.__parent__._cast(_1386.ElectricMachineDesignBase)

    @property
    def surface_permanent_magnet_machine(
        self: "CastSelf",
    ) -> "SurfacePermanentMagnetMachine":
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
class SurfacePermanentMagnetMachine(_1421.NonCADElectricMachineDetail):
    """SurfacePermanentMagnetMachine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SURFACE_PERMANENT_MAGNET_MACHINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def rotor(self: "Self") -> "_1440.SurfacePermanentMagnetRotor":
        """mastapy.electric_machines.SurfacePermanentMagnetRotor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rotor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SurfacePermanentMagnetMachine":
        """Cast to another type.

        Returns:
            _Cast_SurfacePermanentMagnetMachine
        """
        return _Cast_SurfacePermanentMagnetMachine(self)
