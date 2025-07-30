"""ElectricMachineHarmonicLoadDataFromExcel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.static_loads import _7740

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_EXCEL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ElectricMachineHarmonicLoadDataFromExcel",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import (
        _1562,
        _1564,
        _1568,
    )

    Self = TypeVar("Self", bound="ElectricMachineHarmonicLoadDataFromExcel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineHarmonicLoadDataFromExcel._Cast_ElectricMachineHarmonicLoadDataFromExcel",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineHarmonicLoadDataFromExcel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineHarmonicLoadDataFromExcel:
    """Special nested class for casting ElectricMachineHarmonicLoadDataFromExcel to subclasses."""

    __parent__: "ElectricMachineHarmonicLoadDataFromExcel"

    @property
    def electric_machine_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7740.ElectricMachineHarmonicLoadData":
        return self.__parent__._cast(_7740.ElectricMachineHarmonicLoadData)

    @property
    def electric_machine_harmonic_load_data_base(
        self: "CastSelf",
    ) -> "_1562.ElectricMachineHarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1562

        return self.__parent__._cast(_1562.ElectricMachineHarmonicLoadDataBase)

    @property
    def speed_dependent_harmonic_load_data(
        self: "CastSelf",
    ) -> "_1568.SpeedDependentHarmonicLoadData":
        from mastapy._private.electric_machines.harmonic_load_data import _1568

        return self.__parent__._cast(_1568.SpeedDependentHarmonicLoadData)

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "_1564.HarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1564

        return self.__parent__._cast(_1564.HarmonicLoadDataBase)

    @property
    def electric_machine_harmonic_load_data_from_excel(
        self: "CastSelf",
    ) -> "ElectricMachineHarmonicLoadDataFromExcel":
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
class ElectricMachineHarmonicLoadDataFromExcel(_7740.ElectricMachineHarmonicLoadData):
    """ElectricMachineHarmonicLoadDataFromExcel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_EXCEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineHarmonicLoadDataFromExcel":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineHarmonicLoadDataFromExcel
        """
        return _Cast_ElectricMachineHarmonicLoadDataFromExcel(self)
