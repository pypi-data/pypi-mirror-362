"""CylindricalGearDefaults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
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
from mastapy._private.utility import _1786

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_CYLINDRICAL_GEAR_DEFAULTS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearDefaults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1157
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1259,
    )
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
        _1203,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _845
    from mastapy._private.gears.manufacturing.cylindrical.cutters import _825
    from mastapy._private.utility import _1787

    Self = TypeVar("Self", bound="CylindricalGearDefaults")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearDefaults._Cast_CylindricalGearDefaults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearDefaults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearDefaults:
    """Special nested class for casting CylindricalGearDefaults to subclasses."""

    __parent__: "CylindricalGearDefaults"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1786.PerMachineSettings":
        return self.__parent__._cast(_1786.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1787.PersistentSingleton":
        from mastapy._private.utility import _1787

        return self.__parent__._cast(_1787.PersistentSingleton)

    @property
    def cylindrical_gear_defaults(self: "CastSelf") -> "CylindricalGearDefaults":
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
class CylindricalGearDefaults(_1786.PerMachineSettings):
    """CylindricalGearDefaults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_DEFAULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def agma_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "AGMAMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @agma_material.setter
    @exception_bridge
    @enforce_parameter_types
    def agma_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "AGMAMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def chamfer_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ChamferAngle")

        if temp is None:
            return 0.0

        return temp

    @chamfer_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def chamfer_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ChamferAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def diameter_chamfer_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DiameterChamferHeight")

        if temp is None:
            return 0.0

        return temp

    @diameter_chamfer_height.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter_chamfer_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DiameterChamferHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def fillet_roughness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FilletRoughness")

        if temp is None:
            return 0.0

        return temp

    @fillet_roughness.setter
    @exception_bridge
    @enforce_parameter_types
    def fillet_roughness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FilletRoughness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def finish_stock_type(self: "Self") -> "_1203.FinishStockType":
        """mastapy.gears.gear_designs.cylindrical.thickness_stock_and_backlash.FinishStockType"""
        temp = pythonnet_property_get(self.wrapped, "FinishStockType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ThicknessStockAndBacklash.FinishStockType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash._1203",
            "FinishStockType",
        )(value)

    @finish_stock_type.setter
    @exception_bridge
    @enforce_parameter_types
    def finish_stock_type(self: "Self", value: "_1203.FinishStockType") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ThicknessStockAndBacklash.FinishStockType",
        )
        pythonnet_property_set(self.wrapped, "FinishStockType", value)

    @property
    @exception_bridge
    def flank_roughness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FlankRoughness")

        if temp is None:
            return 0.0

        return temp

    @flank_roughness.setter
    @exception_bridge
    @enforce_parameter_types
    def flank_roughness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FlankRoughness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def gear_fit_system(self: "Self") -> "_1157.GearFitSystems":
        """mastapy.gears.gear_designs.cylindrical.GearFitSystems"""
        temp = pythonnet_property_get(self.wrapped, "GearFitSystem")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.GearFitSystems"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1157", "GearFitSystems"
        )(value)

    @gear_fit_system.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_fit_system(self: "Self", value: "_1157.GearFitSystems") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.GearFitSystems"
        )
        pythonnet_property_set(self.wrapped, "GearFitSystem", value)

    @property
    @exception_bridge
    def iso_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ISOMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @iso_material.setter
    @exception_bridge
    @enforce_parameter_types
    def iso_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ISOMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def iso_quality_grade(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ISOQualityGrade")

        if temp is None:
            return 0

        return temp

    @iso_quality_grade.setter
    @exception_bridge
    @enforce_parameter_types
    def iso_quality_grade(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ISOQualityGrade", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def finish_manufacturing_process_controls(
        self: "Self",
    ) -> "_845.ManufacturingProcessControls":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.ManufacturingProcessControls

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FinishManufacturingProcessControls"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rough_cutter_creation_settings(
        self: "Self",
    ) -> "_825.RoughCutterCreationSettings":
        """mastapy.gears.manufacturing.cylindrical.cutters.RoughCutterCreationSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughCutterCreationSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rough_manufacturing_process_controls(
        self: "Self",
    ) -> "_845.ManufacturingProcessControls":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.ManufacturingProcessControls

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughManufacturingProcessControls")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_of_fits_defaults(self: "Self") -> "_1259.DIN3967SystemOfGearFits":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.DIN3967SystemOfGearFits

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemOfFitsDefaults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearDefaults":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearDefaults
        """
        return _Cast_CylindricalGearDefaults(self)
