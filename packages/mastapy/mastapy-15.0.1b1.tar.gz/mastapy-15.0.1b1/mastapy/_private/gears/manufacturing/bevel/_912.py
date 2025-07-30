"""PinionMachineSettingsSMT"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.bevel import _909

_PINION_MACHINE_SETTINGS_SMT = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "PinionMachineSettingsSMT"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _409

    Self = TypeVar("Self", bound="PinionMachineSettingsSMT")
    CastSelf = TypeVar(
        "CastSelf", bound="PinionMachineSettingsSMT._Cast_PinionMachineSettingsSMT"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PinionMachineSettingsSMT",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PinionMachineSettingsSMT:
    """Special nested class for casting PinionMachineSettingsSMT to subclasses."""

    __parent__: "PinionMachineSettingsSMT"

    @property
    def pinion_finish_machine_settings(
        self: "CastSelf",
    ) -> "_909.PinionFinishMachineSettings":
        return self.__parent__._cast(_909.PinionFinishMachineSettings)

    @property
    def conical_gear_tooth_surface(self: "CastSelf") -> "_409.ConicalGearToothSurface":
        from mastapy._private.gears import _409

        return self.__parent__._cast(_409.ConicalGearToothSurface)

    @property
    def pinion_machine_settings_smt(self: "CastSelf") -> "PinionMachineSettingsSMT":
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
class PinionMachineSettingsSMT(_909.PinionFinishMachineSettings):
    """PinionMachineSettingsSMT

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PINION_MACHINE_SETTINGS_SMT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PinionMachineSettingsSMT":
        """Cast to another type.

        Returns:
            _Cast_PinionMachineSettingsSMT
        """
        return _Cast_PinionMachineSettingsSMT(self)
