"""ElectricMachineHarmonicLoadFluxImportOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.static_loads import _7749

_ELECTRIC_MACHINE_HARMONIC_LOAD_FLUX_IMPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ElectricMachineHarmonicLoadFluxImportOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElectricMachineHarmonicLoadFluxImportOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineHarmonicLoadFluxImportOptions._Cast_ElectricMachineHarmonicLoadFluxImportOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineHarmonicLoadFluxImportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineHarmonicLoadFluxImportOptions:
    """Special nested class for casting ElectricMachineHarmonicLoadFluxImportOptions to subclasses."""

    __parent__: "ElectricMachineHarmonicLoadFluxImportOptions"

    @property
    def electric_machine_harmonic_load_import_options_base(
        self: "CastSelf",
    ) -> "_7749.ElectricMachineHarmonicLoadImportOptionsBase":
        return self.__parent__._cast(_7749.ElectricMachineHarmonicLoadImportOptionsBase)

    @property
    def electric_machine_harmonic_load_flux_import_options(
        self: "CastSelf",
    ) -> "ElectricMachineHarmonicLoadFluxImportOptions":
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
class ElectricMachineHarmonicLoadFluxImportOptions(
    _7749.ElectricMachineHarmonicLoadImportOptionsBase
):
    """ElectricMachineHarmonicLoadFluxImportOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_HARMONIC_LOAD_FLUX_IMPORT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineHarmonicLoadFluxImportOptions":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineHarmonicLoadFluxImportOptions
        """
        return _Cast_ElectricMachineHarmonicLoadFluxImportOptions(self)
