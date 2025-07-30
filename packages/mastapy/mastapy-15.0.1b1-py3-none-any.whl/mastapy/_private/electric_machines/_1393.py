"""ElectricMachineMeshingOptionsBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis import _64

_ELECTRIC_MACHINE_MESHING_OPTIONS_BASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "ElectricMachineMeshingOptionsBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1389, _1391, _1392, _1396

    Self = TypeVar("Self", bound="ElectricMachineMeshingOptionsBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineMeshingOptionsBase._Cast_ElectricMachineMeshingOptionsBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineMeshingOptionsBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineMeshingOptionsBase:
    """Special nested class for casting ElectricMachineMeshingOptionsBase to subclasses."""

    __parent__: "ElectricMachineMeshingOptionsBase"

    @property
    def fe_meshing_options(self: "CastSelf") -> "_64.FEMeshingOptions":
        return self.__parent__._cast(_64.FEMeshingOptions)

    @property
    def electric_machine_electromagnetic_and_thermal_meshing_options(
        self: "CastSelf",
    ) -> "_1389.ElectricMachineElectromagneticAndThermalMeshingOptions":
        from mastapy._private.electric_machines import _1389

        return self.__parent__._cast(
            _1389.ElectricMachineElectromagneticAndThermalMeshingOptions
        )

    @property
    def electric_machine_mechanical_analysis_meshing_options(
        self: "CastSelf",
    ) -> "_1391.ElectricMachineMechanicalAnalysisMeshingOptions":
        from mastapy._private.electric_machines import _1391

        return self.__parent__._cast(
            _1391.ElectricMachineMechanicalAnalysisMeshingOptions
        )

    @property
    def electric_machine_meshing_options(
        self: "CastSelf",
    ) -> "_1392.ElectricMachineMeshingOptions":
        from mastapy._private.electric_machines import _1392

        return self.__parent__._cast(_1392.ElectricMachineMeshingOptions)

    @property
    def electric_machine_thermal_meshing_options(
        self: "CastSelf",
    ) -> "_1396.ElectricMachineThermalMeshingOptions":
        from mastapy._private.electric_machines import _1396

        return self.__parent__._cast(_1396.ElectricMachineThermalMeshingOptions)

    @property
    def electric_machine_meshing_options_base(
        self: "CastSelf",
    ) -> "ElectricMachineMeshingOptionsBase":
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
class ElectricMachineMeshingOptionsBase(_64.FEMeshingOptions):
    """ElectricMachineMeshingOptionsBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_MESHING_OPTIONS_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def autogenerate_mesh(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "AutogenerateMesh")

        if temp is None:
            return False

        return temp

    @autogenerate_mesh.setter
    @exception_bridge
    @enforce_parameter_types
    def autogenerate_mesh(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AutogenerateMesh",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def utilise_periodicity_when_meshing_geometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UtilisePeriodicityWhenMeshingGeometry"
        )

        if temp is None:
            return False

        return temp

    @utilise_periodicity_when_meshing_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def utilise_periodicity_when_meshing_geometry(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UtilisePeriodicityWhenMeshingGeometry",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineMeshingOptionsBase":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineMeshingOptionsBase
        """
        return _Cast_ElectricMachineMeshingOptionsBase(self)
