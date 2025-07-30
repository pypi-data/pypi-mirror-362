"""TorqueInputOptions"""

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
from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
    _7870,
)

_TORQUE_INPUT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "TorqueInputOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
        _7876,
    )
    from mastapy._private.utility_gui import _2050

    Self = TypeVar("Self", bound="TorqueInputOptions")
    CastSelf = TypeVar("CastSelf", bound="TorqueInputOptions._Cast_TorqueInputOptions")


__docformat__ = "restructuredtext en"
__all__ = ("TorqueInputOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueInputOptions:
    """Special nested class for casting TorqueInputOptions to subclasses."""

    __parent__: "TorqueInputOptions"

    @property
    def power_load_input_options(self: "CastSelf") -> "_7870.PowerLoadInputOptions":
        return self.__parent__._cast(_7870.PowerLoadInputOptions)

    @property
    def column_input_options(self: "CastSelf") -> "_2050.ColumnInputOptions":
        from mastapy._private.utility_gui import _2050

        return self.__parent__._cast(_2050.ColumnInputOptions)

    @property
    def torque_input_options(self: "CastSelf") -> "TorqueInputOptions":
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
class TorqueInputOptions(_7870.PowerLoadInputOptions):
    """TorqueInputOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_INPUT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bin_start(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BinStart")

        if temp is None:
            return 0.0

        return temp

    @bin_start.setter
    @exception_bridge
    @enforce_parameter_types
    def bin_start(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BinStart", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def bin_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BinWidth")

        if temp is None:
            return 0.0

        return temp

    @bin_width.setter
    @exception_bridge
    @enforce_parameter_types
    def bin_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BinWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def conversion_to_load_case(self: "Self") -> "_7876.TorqueValuesObtainedFrom":
        """mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.TorqueValuesObtainedFrom"""
        temp = pythonnet_property_get(self.wrapped, "ConversionToLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition.TorqueValuesObtainedFrom",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition._7876",
            "TorqueValuesObtainedFrom",
        )(value)

    @conversion_to_load_case.setter
    @exception_bridge
    @enforce_parameter_types
    def conversion_to_load_case(
        self: "Self", value: "_7876.TorqueValuesObtainedFrom"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition.TorqueValuesObtainedFrom",
        )
        pythonnet_property_set(self.wrapped, "ConversionToLoadCase", value)

    @property
    @exception_bridge
    def include_bin_boundary_at_zero(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBinBoundaryAtZero")

        if temp is None:
            return False

        return temp

    @include_bin_boundary_at_zero.setter
    @exception_bridge
    @enforce_parameter_types
    def include_bin_boundary_at_zero(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBinBoundaryAtZero",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def number_of_bins(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfBins")

        if temp is None:
            return 0

        return temp

    @number_of_bins.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_bins(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfBins", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def specify_bins(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyBins")

        if temp is None:
            return False

        return temp

    @specify_bins.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_bins(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SpecifyBins", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TorqueInputOptions":
        """Cast to another type.

        Returns:
            _Cast_TorqueInputOptions
        """
        return _Cast_TorqueInputOptions(self)
