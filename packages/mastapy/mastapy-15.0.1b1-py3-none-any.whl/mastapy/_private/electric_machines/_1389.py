"""ElectricMachineElectromagneticAndThermalMeshingOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
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
from mastapy._private.electric_machines import _1393

_ELECTRIC_MACHINE_ELECTROMAGNETIC_AND_THERMAL_MESHING_OPTIONS = python_net_import(
    "SMT.MastaAPI.ElectricMachines",
    "ElectricMachineElectromagneticAndThermalMeshingOptions",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.electric_machines import _1392, _1396
    from mastapy._private.nodal_analysis import _64

    Self = TypeVar(
        "Self", bound="ElectricMachineElectromagneticAndThermalMeshingOptions"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineElectromagneticAndThermalMeshingOptions._Cast_ElectricMachineElectromagneticAndThermalMeshingOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineElectromagneticAndThermalMeshingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineElectromagneticAndThermalMeshingOptions:
    """Special nested class for casting ElectricMachineElectromagneticAndThermalMeshingOptions to subclasses."""

    __parent__: "ElectricMachineElectromagneticAndThermalMeshingOptions"

    @property
    def electric_machine_meshing_options_base(
        self: "CastSelf",
    ) -> "_1393.ElectricMachineMeshingOptionsBase":
        return self.__parent__._cast(_1393.ElectricMachineMeshingOptionsBase)

    @property
    def fe_meshing_options(self: "CastSelf") -> "_64.FEMeshingOptions":
        from mastapy._private.nodal_analysis import _64

        return self.__parent__._cast(_64.FEMeshingOptions)

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
    def electric_machine_electromagnetic_and_thermal_meshing_options(
        self: "CastSelf",
    ) -> "ElectricMachineElectromagneticAndThermalMeshingOptions":
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
class ElectricMachineElectromagneticAndThermalMeshingOptions(
    _1393.ElectricMachineMeshingOptionsBase
):
    """ElectricMachineElectromagneticAndThermalMeshingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ELECTRIC_MACHINE_ELECTROMAGNETIC_AND_THERMAL_MESHING_OPTIONS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def conductor_element_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ConductorElementSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @conductor_element_size.setter
    @exception_bridge
    @enforce_parameter_types
    def conductor_element_size(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ConductorElementSize", value)

    @property
    @exception_bridge
    def field_winding_element_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FieldWindingElementSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @field_winding_element_size.setter
    @exception_bridge
    @enforce_parameter_types
    def field_winding_element_size(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FieldWindingElementSize", value)

    @property
    @exception_bridge
    def magnet_element_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MagnetElementSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @magnet_element_size.setter
    @exception_bridge
    @enforce_parameter_types
    def magnet_element_size(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MagnetElementSize", value)

    @property
    @exception_bridge
    def rotor_element_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RotorElementSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rotor_element_size.setter
    @exception_bridge
    @enforce_parameter_types
    def rotor_element_size(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RotorElementSize", value)

    @property
    @exception_bridge
    def slot_element_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SlotElementSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @slot_element_size.setter
    @exception_bridge
    @enforce_parameter_types
    def slot_element_size(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SlotElementSize", value)

    @property
    @exception_bridge
    def stator_element_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "StatorElementSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @stator_element_size.setter
    @exception_bridge
    @enforce_parameter_types
    def stator_element_size(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "StatorElementSize", value)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ElectricMachineElectromagneticAndThermalMeshingOptions":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineElectromagneticAndThermalMeshingOptions
        """
        return _Cast_ElectricMachineElectromagneticAndThermalMeshingOptions(self)
