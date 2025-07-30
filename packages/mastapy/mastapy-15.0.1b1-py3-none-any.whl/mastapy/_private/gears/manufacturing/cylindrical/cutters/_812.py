"""CylindricalGearHobDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.cutters import _815

_CYLINDRICAL_GEAR_HOB_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters", "CylindricalGearHobDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical import _734
    from mastapy._private.gears.manufacturing.cylindrical.cutters import _809, _816
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
        _828,
        _833,
    )
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="CylindricalGearHobDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearHobDesign._Cast_CylindricalGearHobDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearHobDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearHobDesign:
    """Special nested class for casting CylindricalGearHobDesign to subclasses."""

    __parent__: "CylindricalGearHobDesign"

    @property
    def cylindrical_gear_rack_design(
        self: "CastSelf",
    ) -> "_815.CylindricalGearRackDesign":
        return self.__parent__._cast(_815.CylindricalGearRackDesign)

    @property
    def cylindrical_gear_real_cutter_design(
        self: "CastSelf",
    ) -> "_816.CylindricalGearRealCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _816

        return self.__parent__._cast(_816.CylindricalGearRealCutterDesign)

    @property
    def cylindrical_gear_abstract_cutter_design(
        self: "CastSelf",
    ) -> "_809.CylindricalGearAbstractCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _809

        return self.__parent__._cast(_809.CylindricalGearAbstractCutterDesign)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def cylindrical_gear_hob_design(self: "CastSelf") -> "CylindricalGearHobDesign":
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
class CylindricalGearHobDesign(_815.CylindricalGearRackDesign):
    """CylindricalGearHobDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_HOB_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def addendum_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AddendumTolerance")

        if temp is None:
            return 0.0

        return temp

    @addendum_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def addendum_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AddendumTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def blade_control_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BladeControlDistance")

        if temp is None:
            return 0.0

        return temp

    @blade_control_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def blade_control_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BladeControlDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def blade_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BladeRelief")

        if temp is None:
            return 0.0

        return temp

    @blade_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def blade_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BladeRelief", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def edge_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EdgeHeight")

        if temp is None:
            return 0.0

        return temp

    @edge_height.setter
    @exception_bridge
    @enforce_parameter_types
    def edge_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EdgeHeight", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def edge_radius_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EdgeRadiusTolerance")

        if temp is None:
            return 0.0

        return temp

    @edge_radius_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def edge_radius_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EdgeRadiusTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def flat_tip_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FlatTipWidth")

        if temp is None:
            return 0.0

        return temp

    @flat_tip_width.setter
    @exception_bridge
    @enforce_parameter_types
    def flat_tip_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FlatTipWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def has_protuberance(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasProtuberance")

        if temp is None:
            return False

        return temp

    @has_protuberance.setter
    @exception_bridge
    @enforce_parameter_types
    def has_protuberance(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasProtuberance", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def has_semi_topping_blade(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasSemiToppingBlade")

        if temp is None:
            return False

        return temp

    @has_semi_topping_blade.setter
    @exception_bridge
    @enforce_parameter_types
    def has_semi_topping_blade(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HasSemiToppingBlade",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def hob_edge_type(self: "Self") -> "_734.HobEdgeTypes":
        """mastapy.gears.manufacturing.cylindrical.HobEdgeTypes"""
        temp = pythonnet_property_get(self.wrapped, "HobEdgeType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobEdgeTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.manufacturing.cylindrical._734", "HobEdgeTypes"
        )(value)

    @hob_edge_type.setter
    @exception_bridge
    @enforce_parameter_types
    def hob_edge_type(self: "Self", value: "_734.HobEdgeTypes") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobEdgeTypes"
        )
        pythonnet_property_set(self.wrapped, "HobEdgeType", value)

    @property
    @exception_bridge
    def normal_thickness_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalThicknessTolerance")

        if temp is None:
            return 0.0

        return temp

    @normal_thickness_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_thickness_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalThicknessTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_gashes(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfGashes")

        if temp is None:
            return 0

        return temp

    @number_of_gashes.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_gashes(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfGashes", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def protuberance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Protuberance")

        if temp is None:
            return 0.0

        return temp

    @protuberance.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Protuberance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def protuberance_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceAngle")

        if temp is None:
            return 0.0

        return temp

    @protuberance_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def protuberance_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceFactor")

        if temp is None:
            return 0.0

        return temp

    @protuberance_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def protuberance_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceHeight")

        if temp is None:
            return 0.0

        return temp

    @protuberance_height.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def protuberance_height_relative_to_edge_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ProtuberanceHeightRelativeToEdgeHeight"
        )

        if temp is None:
            return 0.0

        return temp

    @protuberance_height_relative_to_edge_height.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_height_relative_to_edge_height(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceHeightRelativeToEdgeHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def protuberance_height_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceHeightTolerance")

        if temp is None:
            return 0.0

        return temp

    @protuberance_height_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_height_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceHeightTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def protuberance_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def protuberance_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceTolerance")

        if temp is None:
            return 0.0

        return temp

    @protuberance_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def semi_topping_blade_height_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SemiToppingBladeHeightTolerance")

        if temp is None:
            return 0.0

        return temp

    @semi_topping_blade_height_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def semi_topping_blade_height_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SemiToppingBladeHeightTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def semi_topping_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SemiToppingHeight")

        if temp is None:
            return 0.0

        return temp

    @semi_topping_height.setter
    @exception_bridge
    @enforce_parameter_types
    def semi_topping_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SemiToppingHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def semi_topping_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SemiToppingPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @semi_topping_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def semi_topping_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SemiToppingPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def semi_topping_pressure_angle_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SemiToppingPressureAngleTolerance")

        if temp is None:
            return 0.0

        return temp

    @semi_topping_pressure_angle_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def semi_topping_pressure_angle_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SemiToppingPressureAngleTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def semi_topping_start(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SemiToppingStart")

        if temp is None:
            return 0.0

        return temp

    @semi_topping_start.setter
    @exception_bridge
    @enforce_parameter_types
    def semi_topping_start(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SemiToppingStart", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tip_control_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TipControlDistance")

        if temp is None:
            return 0.0

        return temp

    @tip_control_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def tip_control_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TipControlDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_hob_material_shape(self: "Self") -> "_828.CylindricalGearHobShape":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.CylindricalGearHobShape

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumHobMaterialShape")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minimum_hob_material_shape(self: "Self") -> "_828.CylindricalGearHobShape":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.CylindricalGearHobShape

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumHobMaterialShape")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def nominal_hob_shape(self: "Self") -> "_828.CylindricalGearHobShape":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.CylindricalGearHobShape

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalHobShape")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def nominal_rack_shape(self: "Self") -> "_833.RackShape":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.RackShape

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalRackShape")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearHobDesign":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearHobDesign
        """
        return _Cast_CylindricalGearHobDesign(self)
