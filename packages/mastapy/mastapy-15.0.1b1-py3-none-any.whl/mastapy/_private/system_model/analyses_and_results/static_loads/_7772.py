"""HarmonicLoadDataJMAGImport"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7750, _7767

_HARMONIC_LOAD_DATA_JMAG_IMPORT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "HarmonicLoadDataJMAGImport",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7770,
        _7771,
    )

    Self = TypeVar("Self", bound="HarmonicLoadDataJMAGImport")
    CastSelf = TypeVar(
        "CastSelf", bound="HarmonicLoadDataJMAGImport._Cast_HarmonicLoadDataJMAGImport"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicLoadDataJMAGImport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicLoadDataJMAGImport:
    """Special nested class for casting HarmonicLoadDataJMAGImport to subclasses."""

    __parent__: "HarmonicLoadDataJMAGImport"

    @property
    def harmonic_load_data_csv_import(
        self: "CastSelf",
    ) -> "_7767.HarmonicLoadDataCSVImport":
        return self.__parent__._cast(_7767.HarmonicLoadDataCSVImport)

    @property
    def harmonic_load_data_import_from_motor_packages(
        self: "CastSelf",
    ) -> "_7771.HarmonicLoadDataImportFromMotorPackages":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7771,
        )

        return self.__parent__._cast(_7771.HarmonicLoadDataImportFromMotorPackages)

    @property
    def harmonic_load_data_import_base(
        self: "CastSelf",
    ) -> "_7770.HarmonicLoadDataImportBase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7770,
        )

        return self.__parent__._cast(_7770.HarmonicLoadDataImportBase)

    @property
    def harmonic_load_data_jmag_import(
        self: "CastSelf",
    ) -> "HarmonicLoadDataJMAGImport":
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
class HarmonicLoadDataJMAGImport(
    _7767.HarmonicLoadDataCSVImport[_7750.ElectricMachineHarmonicLoadJMAGImportOptions]
):
    """HarmonicLoadDataJMAGImport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_LOAD_DATA_JMAG_IMPORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    def select_jmag_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectJMAGFile")

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicLoadDataJMAGImport":
        """Cast to another type.

        Returns:
            _Cast_HarmonicLoadDataJMAGImport
        """
        return _Cast_HarmonicLoadDataJMAGImport(self)
