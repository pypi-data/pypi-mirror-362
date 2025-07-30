"""ConicalWheelManufacturingConfig"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.bevel import _879

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_CONICAL_WHEEL_MANUFACTURING_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalWheelManufacturingConfig"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335, _1338, _1341
    from mastapy._private.gears.manufacturing.bevel import _881
    from mastapy._private.gears.manufacturing.bevel.basic_machine_settings import (
        _924,
        _927,
    )
    from mastapy._private.gears.manufacturing.bevel.cutters import _918, _919

    Self = TypeVar("Self", bound="ConicalWheelManufacturingConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalWheelManufacturingConfig._Cast_ConicalWheelManufacturingConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalWheelManufacturingConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalWheelManufacturingConfig:
    """Special nested class for casting ConicalWheelManufacturingConfig to subclasses."""

    __parent__: "ConicalWheelManufacturingConfig"

    @property
    def conical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_879.ConicalGearManufacturingConfig":
        return self.__parent__._cast(_879.ConicalGearManufacturingConfig)

    @property
    def conical_gear_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_881.ConicalGearMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _881

        return self.__parent__._cast(_881.ConicalGearMicroGeometryConfigBase)

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1341.GearImplementationDetail":
        from mastapy._private.gears.analysis import _1341

        return self.__parent__._cast(_1341.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1338

        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def conical_wheel_manufacturing_config(
        self: "CastSelf",
    ) -> "ConicalWheelManufacturingConfig":
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
class ConicalWheelManufacturingConfig(_879.ConicalGearManufacturingConfig):
    """ConicalWheelManufacturingConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_WHEEL_MANUFACTURING_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def use_cutter_tilt(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseCutterTilt")

        if temp is None:
            return False

        return temp

    @use_cutter_tilt.setter
    @exception_bridge
    @enforce_parameter_types
    def use_cutter_tilt(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseCutterTilt", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def wheel_finish_manufacturing_machine(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "WheelFinishManufacturingMachine", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @wheel_finish_manufacturing_machine.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_finish_manufacturing_machine(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "WheelFinishManufacturingMachine",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def wheel_rough_manufacturing_machine(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "WheelRoughManufacturingMachine", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @wheel_rough_manufacturing_machine.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_rough_manufacturing_machine(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "WheelRoughManufacturingMachine",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def specified_cradle_style_machine_settings(
        self: "Self",
    ) -> "_927.CradleStyleConicalMachineSettingsGenerated":
        """mastapy.gears.manufacturing.bevel.basic_machine_settings.CradleStyleConicalMachineSettingsGenerated

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpecifiedCradleStyleMachineSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def specified_machine_settings(
        self: "Self",
    ) -> "_924.BasicConicalGearMachineSettings":
        """mastapy.gears.manufacturing.bevel.basic_machine_settings.BasicConicalGearMachineSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpecifiedMachineSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def wheel_finish_cutter(self: "Self") -> "_918.WheelFinishCutter":
        """mastapy.gears.manufacturing.bevel.cutters.WheelFinishCutter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelFinishCutter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def wheel_rough_cutter(self: "Self") -> "_919.WheelRoughCutter":
        """mastapy.gears.manufacturing.bevel.cutters.WheelRoughCutter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelRoughCutter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalWheelManufacturingConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalWheelManufacturingConfig
        """
        return _Cast_ConicalWheelManufacturingConfig(self)
