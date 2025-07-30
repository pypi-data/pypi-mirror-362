"""ConicalGearToothSurface"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_CONICAL_GEAR_TOOTH_SURFACE = python_net_import(
    "SMT.MastaAPI.Gears", "ConicalGearToothSurface"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _416
    from mastapy._private.gears.manufacturing.bevel import (
        _883,
        _904,
        _905,
        _907,
        _909,
        _910,
        _911,
        _912,
    )

    Self = TypeVar("Self", bound="ConicalGearToothSurface")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearToothSurface._Cast_ConicalGearToothSurface"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearToothSurface",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearToothSurface:
    """Special nested class for casting ConicalGearToothSurface to subclasses."""

    __parent__: "ConicalGearToothSurface"

    @property
    def gear_nurbs_surface(self: "CastSelf") -> "_416.GearNURBSSurface":
        from mastapy._private.gears import _416

        return self.__parent__._cast(_416.GearNURBSSurface)

    @property
    def conical_meshed_wheel_flank_manufacturing_config(
        self: "CastSelf",
    ) -> "_883.ConicalMeshedWheelFlankManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _883

        return self.__parent__._cast(_883.ConicalMeshedWheelFlankManufacturingConfig)

    @property
    def pinion_bevel_generating_modified_roll_machine_settings(
        self: "CastSelf",
    ) -> "_904.PinionBevelGeneratingModifiedRollMachineSettings":
        from mastapy._private.gears.manufacturing.bevel import _904

        return self.__parent__._cast(
            _904.PinionBevelGeneratingModifiedRollMachineSettings
        )

    @property
    def pinion_bevel_generating_tilt_machine_settings(
        self: "CastSelf",
    ) -> "_905.PinionBevelGeneratingTiltMachineSettings":
        from mastapy._private.gears.manufacturing.bevel import _905

        return self.__parent__._cast(_905.PinionBevelGeneratingTiltMachineSettings)

    @property
    def pinion_conical_machine_settings_specified(
        self: "CastSelf",
    ) -> "_907.PinionConicalMachineSettingsSpecified":
        from mastapy._private.gears.manufacturing.bevel import _907

        return self.__parent__._cast(_907.PinionConicalMachineSettingsSpecified)

    @property
    def pinion_finish_machine_settings(
        self: "CastSelf",
    ) -> "_909.PinionFinishMachineSettings":
        from mastapy._private.gears.manufacturing.bevel import _909

        return self.__parent__._cast(_909.PinionFinishMachineSettings)

    @property
    def pinion_hypoid_formate_tilt_machine_settings(
        self: "CastSelf",
    ) -> "_910.PinionHypoidFormateTiltMachineSettings":
        from mastapy._private.gears.manufacturing.bevel import _910

        return self.__parent__._cast(_910.PinionHypoidFormateTiltMachineSettings)

    @property
    def pinion_hypoid_generating_tilt_machine_settings(
        self: "CastSelf",
    ) -> "_911.PinionHypoidGeneratingTiltMachineSettings":
        from mastapy._private.gears.manufacturing.bevel import _911

        return self.__parent__._cast(_911.PinionHypoidGeneratingTiltMachineSettings)

    @property
    def pinion_machine_settings_smt(
        self: "CastSelf",
    ) -> "_912.PinionMachineSettingsSMT":
        from mastapy._private.gears.manufacturing.bevel import _912

        return self.__parent__._cast(_912.PinionMachineSettingsSMT)

    @property
    def conical_gear_tooth_surface(self: "CastSelf") -> "ConicalGearToothSurface":
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
class ConicalGearToothSurface(_0.APIBase):
    """ConicalGearToothSurface

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_TOOTH_SURFACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearToothSurface":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearToothSurface
        """
        return _Cast_ConicalGearToothSurface(self)
