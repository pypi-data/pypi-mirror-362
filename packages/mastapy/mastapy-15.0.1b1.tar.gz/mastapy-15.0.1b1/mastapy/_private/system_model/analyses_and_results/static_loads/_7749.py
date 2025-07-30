"""ElectricMachineHarmonicLoadImportOptionsBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_ELECTRIC_MACHINE_HARMONIC_LOAD_IMPORT_OPTIONS_BASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ElectricMachineHarmonicLoadImportOptionsBase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7747,
        _7748,
        _7750,
        _7751,
    )

    Self = TypeVar("Self", bound="ElectricMachineHarmonicLoadImportOptionsBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineHarmonicLoadImportOptionsBase._Cast_ElectricMachineHarmonicLoadImportOptionsBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineHarmonicLoadImportOptionsBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineHarmonicLoadImportOptionsBase:
    """Special nested class for casting ElectricMachineHarmonicLoadImportOptionsBase to subclasses."""

    __parent__: "ElectricMachineHarmonicLoadImportOptionsBase"

    @property
    def electric_machine_harmonic_load_excel_import_options(
        self: "CastSelf",
    ) -> "_7747.ElectricMachineHarmonicLoadExcelImportOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7747,
        )

        return self.__parent__._cast(
            _7747.ElectricMachineHarmonicLoadExcelImportOptions
        )

    @property
    def electric_machine_harmonic_load_flux_import_options(
        self: "CastSelf",
    ) -> "_7748.ElectricMachineHarmonicLoadFluxImportOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7748,
        )

        return self.__parent__._cast(_7748.ElectricMachineHarmonicLoadFluxImportOptions)

    @property
    def electric_machine_harmonic_load_jmag_import_options(
        self: "CastSelf",
    ) -> "_7750.ElectricMachineHarmonicLoadJMAGImportOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7750,
        )

        return self.__parent__._cast(_7750.ElectricMachineHarmonicLoadJMAGImportOptions)

    @property
    def electric_machine_harmonic_load_motor_cad_import_options(
        self: "CastSelf",
    ) -> "_7751.ElectricMachineHarmonicLoadMotorCADImportOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7751,
        )

        return self.__parent__._cast(
            _7751.ElectricMachineHarmonicLoadMotorCADImportOptions
        )

    @property
    def electric_machine_harmonic_load_import_options_base(
        self: "CastSelf",
    ) -> "ElectricMachineHarmonicLoadImportOptionsBase":
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
class ElectricMachineHarmonicLoadImportOptionsBase(_0.APIBase):
    """ElectricMachineHarmonicLoadImportOptionsBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_HARMONIC_LOAD_IMPORT_OPTIONS_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineHarmonicLoadImportOptionsBase":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineHarmonicLoadImportOptionsBase
        """
        return _Cast_ElectricMachineHarmonicLoadImportOptionsBase(self)
