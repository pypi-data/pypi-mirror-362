"""HarmonicLoadDataControlExcitationOptionForElectricMachineMode"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.electric_machines.harmonic_load_data import _1565

_HARMONIC_LOAD_DATA_CONTROL_EXCITATION_OPTION_FOR_ELECTRIC_MACHINE_MODE = (
    python_net_import(
        "SMT.MastaAPI.ElectricMachines",
        "HarmonicLoadDataControlExcitationOptionForElectricMachineMode",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar(
        "Self", bound="HarmonicLoadDataControlExcitationOptionForElectricMachineMode"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicLoadDataControlExcitationOptionForElectricMachineMode._Cast_HarmonicLoadDataControlExcitationOptionForElectricMachineMode",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicLoadDataControlExcitationOptionForElectricMachineMode",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicLoadDataControlExcitationOptionForElectricMachineMode:
    """Special nested class for casting HarmonicLoadDataControlExcitationOptionForElectricMachineMode to subclasses."""

    __parent__: "HarmonicLoadDataControlExcitationOptionForElectricMachineMode"

    @property
    def harmonic_load_data_control_excitation_option_base(
        self: "CastSelf",
    ) -> "_1565.HarmonicLoadDataControlExcitationOptionBase":
        return self.__parent__._cast(_1565.HarmonicLoadDataControlExcitationOptionBase)

    @property
    def harmonic_load_data_control_excitation_option_for_electric_machine_mode(
        self: "CastSelf",
    ) -> "HarmonicLoadDataControlExcitationOptionForElectricMachineMode":
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
class HarmonicLoadDataControlExcitationOptionForElectricMachineMode(
    _1565.HarmonicLoadDataControlExcitationOptionBase
):
    """HarmonicLoadDataControlExcitationOptionForElectricMachineMode

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _HARMONIC_LOAD_DATA_CONTROL_EXCITATION_OPTION_FOR_ELECTRIC_MACHINE_MODE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_HarmonicLoadDataControlExcitationOptionForElectricMachineMode":
        """Cast to another type.

        Returns:
            _Cast_HarmonicLoadDataControlExcitationOptionForElectricMachineMode
        """
        return _Cast_HarmonicLoadDataControlExcitationOptionForElectricMachineMode(self)
