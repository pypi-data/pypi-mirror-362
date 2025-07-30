"""ElectricMachineMeshingOptions"""

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
from mastapy._private.electric_machines import _1389

_ELECTRIC_MACHINE_MESHING_OPTIONS = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "ElectricMachineMeshingOptions"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.electric_machines import _1393
    from mastapy._private.nodal_analysis import _64

    Self = TypeVar("Self", bound="ElectricMachineMeshingOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineMeshingOptions._Cast_ElectricMachineMeshingOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineMeshingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineMeshingOptions:
    """Special nested class for casting ElectricMachineMeshingOptions to subclasses."""

    __parent__: "ElectricMachineMeshingOptions"

    @property
    def electric_machine_electromagnetic_and_thermal_meshing_options(
        self: "CastSelf",
    ) -> "_1389.ElectricMachineElectromagneticAndThermalMeshingOptions":
        return self.__parent__._cast(
            _1389.ElectricMachineElectromagneticAndThermalMeshingOptions
        )

    @property
    def electric_machine_meshing_options_base(
        self: "CastSelf",
    ) -> "_1393.ElectricMachineMeshingOptionsBase":
        from mastapy._private.electric_machines import _1393

        return self.__parent__._cast(_1393.ElectricMachineMeshingOptionsBase)

    @property
    def fe_meshing_options(self: "CastSelf") -> "_64.FEMeshingOptions":
        from mastapy._private.nodal_analysis import _64

        return self.__parent__._cast(_64.FEMeshingOptions)

    @property
    def electric_machine_meshing_options(
        self: "CastSelf",
    ) -> "ElectricMachineMeshingOptions":
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
class ElectricMachineMeshingOptions(
    _1389.ElectricMachineElectromagneticAndThermalMeshingOptions
):
    """ElectricMachineMeshingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_MESHING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def air_gap_element_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AirGapElementSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @air_gap_element_size.setter
    @exception_bridge
    @enforce_parameter_types
    def air_gap_element_size(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AirGapElementSize", value)

    @property
    @exception_bridge
    def number_of_element_layers_in_air_gap(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfElementLayersInAirGap")

        if temp is None:
            return 0

        return temp

    @number_of_element_layers_in_air_gap.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_element_layers_in_air_gap(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfElementLayersInAirGap",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def p_element_order(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PElementOrder")

        if temp is None:
            return 0

        return temp

    @p_element_order.setter
    @exception_bridge
    @enforce_parameter_types
    def p_element_order(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PElementOrder", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def use_p_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UsePElements")

        if temp is None:
            return False

        return temp

    @use_p_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def use_p_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UsePElements", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineMeshingOptions":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineMeshingOptions
        """
        return _Cast_ElectricMachineMeshingOptions(self)
