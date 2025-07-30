"""ElectricMachineStatorToothAxialLoadsExcitationDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6031

_ELECTRIC_MACHINE_STATOR_TOOTH_AXIAL_LOADS_EXCITATION_DETAIL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "ElectricMachineStatorToothAxialLoadsExcitationDetail",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5969,
        _6024,
        _6088,
    )

    Self = TypeVar("Self", bound="ElectricMachineStatorToothAxialLoadsExcitationDetail")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineStatorToothAxialLoadsExcitationDetail._Cast_ElectricMachineStatorToothAxialLoadsExcitationDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineStatorToothAxialLoadsExcitationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineStatorToothAxialLoadsExcitationDetail:
    """Special nested class for casting ElectricMachineStatorToothAxialLoadsExcitationDetail to subclasses."""

    __parent__: "ElectricMachineStatorToothAxialLoadsExcitationDetail"

    @property
    def electric_machine_stator_tooth_loads_excitation_detail(
        self: "CastSelf",
    ) -> "_6031.ElectricMachineStatorToothLoadsExcitationDetail":
        return self.__parent__._cast(
            _6031.ElectricMachineStatorToothLoadsExcitationDetail
        )

    @property
    def electric_machine_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_6024.ElectricMachinePeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6024,
        )

        return self.__parent__._cast(_6024.ElectricMachinePeriodicExcitationDetail)

    @property
    def periodic_excitation_with_reference_shaft(
        self: "CastSelf",
    ) -> "_6088.PeriodicExcitationWithReferenceShaft":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6088,
        )

        return self.__parent__._cast(_6088.PeriodicExcitationWithReferenceShaft)

    @property
    def abstract_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5969.AbstractPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5969,
        )

        return self.__parent__._cast(_5969.AbstractPeriodicExcitationDetail)

    @property
    def electric_machine_stator_tooth_axial_loads_excitation_detail(
        self: "CastSelf",
    ) -> "ElectricMachineStatorToothAxialLoadsExcitationDetail":
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
class ElectricMachineStatorToothAxialLoadsExcitationDetail(
    _6031.ElectricMachineStatorToothLoadsExcitationDetail
):
    """ElectricMachineStatorToothAxialLoadsExcitationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ELECTRIC_MACHINE_STATOR_TOOTH_AXIAL_LOADS_EXCITATION_DETAIL
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
    ) -> "_Cast_ElectricMachineStatorToothAxialLoadsExcitationDetail":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineStatorToothAxialLoadsExcitationDetail
        """
        return _Cast_ElectricMachineStatorToothAxialLoadsExcitationDetail(self)
