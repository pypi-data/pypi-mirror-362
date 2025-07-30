"""Clutch"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.couplings import _2823

_CLUTCH = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Clutch")

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility import _1718
    from mastapy._private.math_utility.measured_data import _1749
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5686
    from mastapy._private.system_model.connections_and_sockets.couplings import _2563
    from mastapy._private.system_model.part_model import _2659, _2698, _2708
    from mastapy._private.system_model.part_model.couplings import _2819

    Self = TypeVar("Self", bound="Clutch")
    CastSelf = TypeVar("CastSelf", bound="Clutch._Cast_Clutch")


__docformat__ = "restructuredtext en"
__all__ = ("Clutch",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Clutch:
    """Special nested class for casting Clutch to subclasses."""

    __parent__: "Clutch"

    @property
    def coupling(self: "CastSelf") -> "_2823.Coupling":
        return self.__parent__._cast(_2823.Coupling)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2708.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2708

        return self.__parent__._cast(_2708.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2659

        return self.__parent__._cast(_2659.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def clutch(self: "CastSelf") -> "Clutch":
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
class Clutch(_2823.Coupling):
    """Clutch

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLUTCH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_speed_temperature_grid(self: "Self") -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "AngularSpeedTemperatureGrid")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @angular_speed_temperature_grid.setter
    @exception_bridge
    @enforce_parameter_types
    def angular_speed_temperature_grid(
        self: "Self", value: "_1749.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "AngularSpeedTemperatureGrid", value.wrapped
        )

    @property
    @exception_bridge
    def area_of_friction_surface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AreaOfFrictionSurface")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bore(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def clearance_between_friction_surfaces(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ClearanceBetweenFrictionSurfaces")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @clearance_between_friction_surfaces.setter
    @exception_bridge
    @enforce_parameter_types
    def clearance_between_friction_surfaces(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ClearanceBetweenFrictionSurfaces", value)

    @property
    @exception_bridge
    def clutch_plate_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClutchPlateTemperature")

        if temp is None:
            return 0.0

        return temp

    @clutch_plate_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def clutch_plate_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ClutchPlateTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def clutch_specific_heat_capacity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClutchSpecificHeatCapacity")

        if temp is None:
            return 0.0

        return temp

    @clutch_specific_heat_capacity.setter
    @exception_bridge
    @enforce_parameter_types
    def clutch_specific_heat_capacity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ClutchSpecificHeatCapacity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def clutch_thermal_mass(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClutchThermalMass")

        if temp is None:
            return 0.0

        return temp

    @clutch_thermal_mass.setter
    @exception_bridge
    @enforce_parameter_types
    def clutch_thermal_mass(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ClutchThermalMass",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def clutch_type(self: "Self") -> "_2819.ClutchType":
        """mastapy.system_model.part_model.couplings.ClutchType"""
        temp = pythonnet_property_get(self.wrapped, "ClutchType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PartModel.Couplings.ClutchType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model.couplings._2819", "ClutchType"
        )(value)

    @clutch_type.setter
    @exception_bridge
    @enforce_parameter_types
    def clutch_type(self: "Self", value: "_2819.ClutchType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PartModel.Couplings.ClutchType"
        )
        pythonnet_property_set(self.wrapped, "ClutchType", value)

    @property
    @exception_bridge
    def clutch_to_oil_heat_transfer_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ClutchToOilHeatTransferCoefficient"
        )

        if temp is None:
            return 0.0

        return temp

    @clutch_to_oil_heat_transfer_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def clutch_to_oil_heat_transfer_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ClutchToOilHeatTransferCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_coefficient_of_friction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DynamicCoefficientOfFriction")

        if temp is None:
            return 0.0

        return temp

    @dynamic_coefficient_of_friction.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_coefficient_of_friction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DynamicCoefficientOfFriction",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def flow_rate_vs_speed(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "FlowRateVsSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @flow_rate_vs_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def flow_rate_vs_speed(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "FlowRateVsSpeed", value.wrapped)

    @property
    @exception_bridge
    def inner_diameter_of_friction_surface(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerDiameterOfFrictionSurface")

        if temp is None:
            return 0.0

        return temp

    @inner_diameter_of_friction_surface.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_diameter_of_friction_surface(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerDiameterOfFrictionSurface",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def kiss_point_clutch_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KissPointClutchPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def kiss_point_piston_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KissPointPistonPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def kiss_point_pressure_percent(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KissPointPressurePercent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def linear_speed_temperature_grid(self: "Self") -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "LinearSpeedTemperatureGrid")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @linear_speed_temperature_grid.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_speed_temperature_grid(
        self: "Self", value: "_1749.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "LinearSpeedTemperatureGrid", value.wrapped
        )

    @property
    @exception_bridge
    def maximum_pressure_at_clutch(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumPressureAtClutch")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_pressure_at_clutch.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_pressure_at_clutch(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumPressureAtClutch", value)

    @property
    @exception_bridge
    def maximum_pressure_at_piston(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumPressureAtPiston")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_pressure_at_piston.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_pressure_at_piston(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumPressureAtPiston", value)

    @property
    @exception_bridge
    def number_of_friction_surfaces(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfFrictionSurfaces")

        if temp is None:
            return 0

        return temp

    @number_of_friction_surfaces.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_friction_surfaces(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfFrictionSurfaces",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def outer_diameter_of_friction_surface(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameterOfFrictionSurface")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter_of_friction_surface.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter_of_friction_surface(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterDiameterOfFrictionSurface",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def piston_area(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PistonArea")

        if temp is None:
            return 0.0

        return temp

    @piston_area.setter
    @exception_bridge
    @enforce_parameter_types
    def piston_area(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PistonArea", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def specified_torque_capacity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedTorqueCapacity")

        if temp is None:
            return 0.0

        return temp

    @specified_torque_capacity.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_torque_capacity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedTorqueCapacity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def spring_preload(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpringPreload")

        if temp is None:
            return 0.0

        return temp

    @spring_preload.setter
    @exception_bridge
    @enforce_parameter_types
    def spring_preload(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SpringPreload", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def spring_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpringStiffness")

        if temp is None:
            return 0.0

        return temp

    @spring_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def spring_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SpringStiffness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def spring_type(self: "Self") -> "_5686.ClutchSpringType":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ClutchSpringType"""
        temp = pythonnet_property_get(self.wrapped, "SpringType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.ClutchSpringType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5686",
            "ClutchSpringType",
        )(value)

    @spring_type.setter
    @exception_bridge
    @enforce_parameter_types
    def spring_type(self: "Self", value: "_5686.ClutchSpringType") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.ClutchSpringType",
        )
        pythonnet_property_set(self.wrapped, "SpringType", value)

    @property
    @exception_bridge
    def static_to_dynamic_friction_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StaticToDynamicFrictionRatio")

        if temp is None:
            return 0.0

        return temp

    @static_to_dynamic_friction_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def static_to_dynamic_friction_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StaticToDynamicFrictionRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_friction_coefficient_lookup(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseFrictionCoefficientLookup")

        if temp is None:
            return False

        return temp

    @use_friction_coefficient_lookup.setter
    @exception_bridge
    @enforce_parameter_types
    def use_friction_coefficient_lookup(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseFrictionCoefficientLookup",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def volumetric_oil_air_mixture_ratio(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "VolumetricOilAirMixtureRatio")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @volumetric_oil_air_mixture_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def volumetric_oil_air_mixture_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "VolumetricOilAirMixtureRatio", value)

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def clutch_connection(self: "Self") -> "_2563.ClutchConnection":
        """mastapy.system_model.connections_and_sockets.couplings.ClutchConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClutchConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_Clutch":
        """Cast to another type.

        Returns:
            _Cast_Clutch
        """
        return _Cast_Clutch(self)
