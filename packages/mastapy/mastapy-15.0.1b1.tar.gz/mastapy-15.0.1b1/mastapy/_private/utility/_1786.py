"""PerMachineSettings"""

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
from mastapy._private.utility import _1787

_PER_MACHINE_SETTINGS = python_net_import("SMT.MastaAPI.Utility", "PerMachineSettings")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2102
    from mastapy._private.gears.gear_designs.cylindrical import _1121
    from mastapy._private.gears.ltca.cylindrical import _958
    from mastapy._private.gears.materials import _690
    from mastapy._private.nodal_analysis import _71
    from mastapy._private.nodal_analysis.geometry_modeller_link import _238
    from mastapy._private.system_model.part_model import _2675, _2701
    from mastapy._private.utility import _1788
    from mastapy._private.utility.cad_export import _2034
    from mastapy._private.utility.databases import _2026
    from mastapy._private.utility.scripting import _1934
    from mastapy._private.utility.units_and_measurements import _1798

    Self = TypeVar("Self", bound="PerMachineSettings")
    CastSelf = TypeVar("CastSelf", bound="PerMachineSettings._Cast_PerMachineSettings")


__docformat__ = "restructuredtext en"
__all__ = ("PerMachineSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PerMachineSettings:
    """Special nested class for casting PerMachineSettings to subclasses."""

    __parent__: "PerMachineSettings"

    @property
    def persistent_singleton(self: "CastSelf") -> "_1787.PersistentSingleton":
        return self.__parent__._cast(_1787.PersistentSingleton)

    @property
    def fe_user_settings(self: "CastSelf") -> "_71.FEUserSettings":
        from mastapy._private.nodal_analysis import _71

        return self.__parent__._cast(_71.FEUserSettings)

    @property
    def geometry_modeller_settings(self: "CastSelf") -> "_238.GeometryModellerSettings":
        from mastapy._private.nodal_analysis.geometry_modeller_link import _238

        return self.__parent__._cast(_238.GeometryModellerSettings)

    @property
    def gear_material_expert_system_factor_settings(
        self: "CastSelf",
    ) -> "_690.GearMaterialExpertSystemFactorSettings":
        from mastapy._private.gears.materials import _690

        return self.__parent__._cast(_690.GearMaterialExpertSystemFactorSettings)

    @property
    def cylindrical_gear_fe_settings(
        self: "CastSelf",
    ) -> "_958.CylindricalGearFESettings":
        from mastapy._private.gears.ltca.cylindrical import _958

        return self.__parent__._cast(_958.CylindricalGearFESettings)

    @property
    def cylindrical_gear_defaults(self: "CastSelf") -> "_1121.CylindricalGearDefaults":
        from mastapy._private.gears.gear_designs.cylindrical import _1121

        return self.__parent__._cast(_1121.CylindricalGearDefaults)

    @property
    def program_settings(self: "CastSelf") -> "_1788.ProgramSettings":
        from mastapy._private.utility import _1788

        return self.__parent__._cast(_1788.ProgramSettings)

    @property
    def measurement_settings(self: "CastSelf") -> "_1798.MeasurementSettings":
        from mastapy._private.utility.units_and_measurements import _1798

        return self.__parent__._cast(_1798.MeasurementSettings)

    @property
    def scripting_setup(self: "CastSelf") -> "_1934.ScriptingSetup":
        from mastapy._private.utility.scripting import _1934

        return self.__parent__._cast(_1934.ScriptingSetup)

    @property
    def database_settings(self: "CastSelf") -> "_2026.DatabaseSettings":
        from mastapy._private.utility.databases import _2026

        return self.__parent__._cast(_2026.DatabaseSettings)

    @property
    def cad_export_settings(self: "CastSelf") -> "_2034.CADExportSettings":
        from mastapy._private.utility.cad_export import _2034

        return self.__parent__._cast(_2034.CADExportSettings)

    @property
    def skf_settings(self: "CastSelf") -> "_2102.SKFSettings":
        from mastapy._private.bearings import _2102

        return self.__parent__._cast(_2102.SKFSettings)

    @property
    def default_export_settings(self: "CastSelf") -> "_2675.DefaultExportSettings":
        from mastapy._private.system_model.part_model import _2675

        return self.__parent__._cast(_2675.DefaultExportSettings)

    @property
    def planet_carrier_settings(self: "CastSelf") -> "_2701.PlanetCarrierSettings":
        from mastapy._private.system_model.part_model import _2701

        return self.__parent__._cast(_2701.PlanetCarrierSettings)

    @property
    def per_machine_settings(self: "CastSelf") -> "PerMachineSettings":
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
class PerMachineSettings(_1787.PersistentSingleton):
    """PerMachineSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PER_MACHINE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    def reset_to_defaults(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ResetToDefaults")

    @property
    def cast_to(self: "Self") -> "_Cast_PerMachineSettings":
        """Cast to another type.

        Returns:
            _Cast_PerMachineSettings
        """
        return _Cast_PerMachineSettings(self)
