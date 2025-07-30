"""InterferenceFitDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.detailed_rigid_connectors import _1572
from mastapy._private.detailed_rigid_connectors.interference_fits import _1633

_INTERFERENCE_FIT_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits", "InterferenceFitDesign"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.detailed_rigid_connectors.interference_fits import (
        _1628,
        _1629,
    )
    from mastapy._private.detailed_rigid_connectors.keyed_joints import _1622

    Self = TypeVar("Self", bound="InterferenceFitDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="InterferenceFitDesign._Cast_InterferenceFitDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterferenceFitDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterferenceFitDesign:
    """Special nested class for casting InterferenceFitDesign to subclasses."""

    __parent__: "InterferenceFitDesign"

    @property
    def detailed_rigid_connector_design(
        self: "CastSelf",
    ) -> "_1572.DetailedRigidConnectorDesign":
        return self.__parent__._cast(_1572.DetailedRigidConnectorDesign)

    @property
    def keyed_joint_design(self: "CastSelf") -> "_1622.KeyedJointDesign":
        from mastapy._private.detailed_rigid_connectors.keyed_joints import _1622

        return self.__parent__._cast(_1622.KeyedJointDesign)

    @property
    def interference_fit_design(self: "CastSelf") -> "InterferenceFitDesign":
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
class InterferenceFitDesign(_1572.DetailedRigidConnectorDesign):
    """InterferenceFitDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTERFERENCE_FIT_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def assembly_method(self: "Self") -> "_1628.AssemblyMethods":
        """mastapy.detailed_rigid_connectors.interference_fits.AssemblyMethods"""
        temp = pythonnet_property_get(self.wrapped, "AssemblyMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits.AssemblyMethods",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.interference_fits._1628",
            "AssemblyMethods",
        )(value)

    @assembly_method.setter
    @exception_bridge
    @enforce_parameter_types
    def assembly_method(self: "Self", value: "_1628.AssemblyMethods") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits.AssemblyMethods",
        )
        pythonnet_property_set(self.wrapped, "AssemblyMethod", value)

    @property
    @exception_bridge
    def auxiliary_elasticity_parameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryElasticityParameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_allowable_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageAllowableAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_allowable_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageAllowableTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_effective_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageEffectiveInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_joint_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageJointPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_permissible_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AveragePermissibleAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_permissible_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AveragePermissibleTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_relative_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageRelativeInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def calculation_method(self: "Self") -> "_1629.CalculationMethods":
        """mastapy.detailed_rigid_connectors.interference_fits.CalculationMethods"""
        temp = pythonnet_property_get(self.wrapped, "CalculationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits.CalculationMethods",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.interference_fits._1629",
            "CalculationMethods",
        )(value)

    @calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def calculation_method(self: "Self", value: "_1629.CalculationMethods") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits.CalculationMethods",
        )
        pythonnet_property_set(self.wrapped, "CalculationMethod", value)

    @property
    @exception_bridge
    def coefficient_of_friction_assembly(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFrictionAssembly")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @coefficient_of_friction_assembly.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction_assembly(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CoefficientOfFrictionAssembly", value)

    @property
    @exception_bridge
    def coefficient_of_friction_circumferential(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionCircumferential"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @coefficient_of_friction_circumferential.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction_circumferential(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "CoefficientOfFrictionCircumferential", value
        )

    @property
    @exception_bridge
    def coefficient_of_friction_longitudinal(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFrictionLongitudinal")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @coefficient_of_friction_longitudinal.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction_longitudinal(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CoefficientOfFrictionLongitudinal", value)

    @property
    @exception_bridge
    def diameter_of_joint(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DiameterOfJoint")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter_of_joint.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter_of_joint(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DiameterOfJoint", value)

    @property
    @exception_bridge
    def dimensionless_plasticity_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DimensionlessPlasticityDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def insertion_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InsertionForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def joining_play(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "JoiningPlay")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def joint_interface_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_Table4JointInterfaceTypes":
        """EnumWithSelectedValue[mastapy.detailed_rigid_connectors.interference_fits.Table4JointInterfaceTypes]"""
        temp = pythonnet_property_get(self.wrapped, "JointInterfaceType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_Table4JointInterfaceTypes.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @joint_interface_type.setter
    @exception_bridge
    @enforce_parameter_types
    def joint_interface_type(
        self: "Self", value: "_1633.Table4JointInterfaceTypes"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_Table4JointInterfaceTypes.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "JointInterfaceType", value)

    @property
    @exception_bridge
    def maximum_allowable_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumAllowableAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_allowable_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumAllowableTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_assembly_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumAssemblyInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_effective_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumEffectiveInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_joint_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumJointPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_permissible_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPermissibleAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_permissible_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPermissibleTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_relative_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumRelativeInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_allowable_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumAllowableAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_allowable_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumAllowableTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_effective_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumEffectiveInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_joint_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumJointPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_permissible_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumPermissibleAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_permissible_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumPermissibleTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_relative_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumRelativeInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_dimensionless_plasticity_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleDimensionlessPlasticityDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def proportion_of_outer_plastically_stressed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProportionOfOuterPlasticallyStressed"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ratio_of_joint_length_to_joint_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatioOfJointLengthToJointDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def required_assembly_temperature_of_the_outer_part(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RequiredAssemblyTemperatureOfTheOuterPart"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def room_temperature_during_assembly(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RoomTemperatureDuringAssembly")

        if temp is None:
            return 0.0

        return temp

    @room_temperature_during_assembly.setter
    @exception_bridge
    @enforce_parameter_types
    def room_temperature_during_assembly(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RoomTemperatureDuringAssembly",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def specified_joint_pressure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedJointPressure")

        if temp is None:
            return 0.0

        return temp

    @specified_joint_pressure.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_joint_pressure(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedJointPressure",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def temperature_of_inner_part_during_assembly(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TemperatureOfInnerPartDuringAssembly"
        )

        if temp is None:
            return 0.0

        return temp

    @temperature_of_inner_part_during_assembly.setter
    @exception_bridge
    @enforce_parameter_types
    def temperature_of_inner_part_during_assembly(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TemperatureOfInnerPartDuringAssembly",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_InterferenceFitDesign":
        """Cast to another type.

        Returns:
            _Cast_InterferenceFitDesign
        """
        return _Cast_InterferenceFitDesign(self)
