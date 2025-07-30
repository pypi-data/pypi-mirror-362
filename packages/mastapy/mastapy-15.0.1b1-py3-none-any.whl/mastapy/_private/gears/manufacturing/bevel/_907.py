"""PinionConicalMachineSettingsSpecified"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.bevel import _909

_PINION_CONICAL_MACHINE_SETTINGS_SPECIFIED = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "PinionConicalMachineSettingsSpecified"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _409

    Self = TypeVar("Self", bound="PinionConicalMachineSettingsSpecified")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PinionConicalMachineSettingsSpecified._Cast_PinionConicalMachineSettingsSpecified",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PinionConicalMachineSettingsSpecified",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PinionConicalMachineSettingsSpecified:
    """Special nested class for casting PinionConicalMachineSettingsSpecified to subclasses."""

    __parent__: "PinionConicalMachineSettingsSpecified"

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
    def pinion_conical_machine_settings_specified(
        self: "CastSelf",
    ) -> "PinionConicalMachineSettingsSpecified":
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
class PinionConicalMachineSettingsSpecified(_909.PinionFinishMachineSettings):
    """PinionConicalMachineSettingsSpecified

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PINION_CONICAL_MACHINE_SETTINGS_SPECIFIED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PinionConicalMachineSettingsSpecified":
        """Cast to another type.

        Returns:
            _Cast_PinionConicalMachineSettingsSpecified
        """
        return _Cast_PinionConicalMachineSettingsSpecified(self)
