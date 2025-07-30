"""HarmonicLoadDataMotorCADImport"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7751, _7771

_HARMONIC_LOAD_DATA_MOTOR_CAD_IMPORT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "HarmonicLoadDataMotorCADImport",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.static_loads import _7770

    Self = TypeVar("Self", bound="HarmonicLoadDataMotorCADImport")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicLoadDataMotorCADImport._Cast_HarmonicLoadDataMotorCADImport",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicLoadDataMotorCADImport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicLoadDataMotorCADImport:
    """Special nested class for casting HarmonicLoadDataMotorCADImport to subclasses."""

    __parent__: "HarmonicLoadDataMotorCADImport"

    @property
    def harmonic_load_data_import_from_motor_packages(
        self: "CastSelf",
    ) -> "_7771.HarmonicLoadDataImportFromMotorPackages":
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
    def harmonic_load_data_motor_cad_import(
        self: "CastSelf",
    ) -> "HarmonicLoadDataMotorCADImport":
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
class HarmonicLoadDataMotorCADImport(
    _7771.HarmonicLoadDataImportFromMotorPackages[
        _7751.ElectricMachineHarmonicLoadMotorCADImportOptions
    ]
):
    """HarmonicLoadDataMotorCADImport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_LOAD_DATA_MOTOR_CAD_IMPORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def derive_rotor_forces_from_stator_loads(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DeriveRotorForcesFromStatorLoads")

        if temp is None:
            return False

        return temp

    @derive_rotor_forces_from_stator_loads.setter
    @exception_bridge
    @enforce_parameter_types
    def derive_rotor_forces_from_stator_loads(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DeriveRotorForcesFromStatorLoads",
            bool(value) if value is not None else False,
        )

    @exception_bridge
    def select_motor_cad_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectMotorCADFile")

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicLoadDataMotorCADImport":
        """Cast to another type.

        Returns:
            _Cast_HarmonicLoadDataMotorCADImport
        """
        return _Cast_HarmonicLoadDataMotorCADImport(self)
