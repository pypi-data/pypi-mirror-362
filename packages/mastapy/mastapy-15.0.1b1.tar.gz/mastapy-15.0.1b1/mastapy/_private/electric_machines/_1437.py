"""StatorRotorMaterial"""

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
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.materials import _358

_STATOR_ROTOR_MATERIAL = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "StatorRotorMaterial"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.electric_machines import _1382, _1411
    from mastapy._private.materials import _335
    from mastapy._private.utility import _1782
    from mastapy._private.utility.databases import _2028
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="StatorRotorMaterial")
    CastSelf = TypeVar(
        "CastSelf", bound="StatorRotorMaterial._Cast_StatorRotorMaterial"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StatorRotorMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StatorRotorMaterial:
    """Special nested class for casting StatorRotorMaterial to subclasses."""

    __parent__: "StatorRotorMaterial"

    @property
    def material(self: "CastSelf") -> "_358.Material":
        return self.__parent__._cast(_358.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def stator_rotor_material(self: "CastSelf") -> "StatorRotorMaterial":
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
class StatorRotorMaterial(_358.Material):
    """StatorRotorMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATOR_ROTOR_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def annealing(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Annealing")

        if temp is None:
            return ""

        return temp

    @annealing.setter
    @exception_bridge
    @enforce_parameter_types
    def annealing(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Annealing", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def coefficient_specification_method(
        self: "Self",
    ) -> "_1411.IronLossCoefficientSpecificationMethod":
        """mastapy.electric_machines.IronLossCoefficientSpecificationMethod"""
        temp = pythonnet_property_get(self.wrapped, "CoefficientSpecificationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.IronLossCoefficientSpecificationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1411",
            "IronLossCoefficientSpecificationMethod",
        )(value)

    @coefficient_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_specification_method(
        self: "Self", value: "_1411.IronLossCoefficientSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.IronLossCoefficientSpecificationMethod",
        )
        pythonnet_property_set(self.wrapped, "CoefficientSpecificationMethod", value)

    @property
    @exception_bridge
    def country(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Country")

        if temp is None:
            return ""

        return temp

    @country.setter
    @exception_bridge
    @enforce_parameter_types
    def country(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Country", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def electrical_resistivity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ElectricalResistivity")

        if temp is None:
            return 0.0

        return temp

    @electrical_resistivity.setter
    @exception_bridge
    @enforce_parameter_types
    def electrical_resistivity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ElectricalResistivity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def grade_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "GradeName")

        if temp is None:
            return ""

        return temp

    @grade_name.setter
    @exception_bridge
    @enforce_parameter_types
    def grade_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "GradeName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def lamination_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LaminationThickness")

        if temp is None:
            return 0.0

        return temp

    @lamination_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def lamination_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LaminationThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def loss_curves(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LossCurves")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def manufacturer(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Manufacturer")

        if temp is None:
            return ""

        return temp

    @manufacturer.setter
    @exception_bridge
    @enforce_parameter_types
    def manufacturer(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Manufacturer", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def material_category(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "MaterialCategory")

        if temp is None:
            return ""

        return temp

    @material_category.setter
    @exception_bridge
    @enforce_parameter_types
    def material_category(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "MaterialCategory", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def stacking_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "StackingFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @stacking_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def stacking_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "StackingFactor", value)

    @property
    @exception_bridge
    def bh_curve_specification(self: "Self") -> "_335.BHCurveSpecification":
        """mastapy.materials.BHCurveSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BHCurveSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def core_loss_coefficients(self: "Self") -> "_1382.CoreLossCoefficients":
        """mastapy.electric_machines.CoreLossCoefficients

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoreLossCoefficients")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def loss_curve_flux_densities(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LossCurveFluxDensities")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def loss_curve_frequencies(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LossCurveFrequencies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def loss_curve_losses(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LossCurveLosses")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def set_loss_curve_data(
        self: "Self",
        frequencies: "List[float]",
        flux_densities: "List[float]",
        loss: "List[float]",
    ) -> None:
        """Method does not return.

        Args:
            frequencies (List[float])
            flux_densities (List[float])
            loss (List[float])
        """
        frequencies = conversion.mp_to_pn_list_float(frequencies)
        flux_densities = conversion.mp_to_pn_list_float(flux_densities)
        loss = conversion.mp_to_pn_list_float(loss)
        pythonnet_method_call(
            self.wrapped, "SetLossCurveData", frequencies, flux_densities, loss
        )

    @exception_bridge
    def try_update_coefficients_from_loss_curve_data(
        self: "Self",
    ) -> "_1782.MethodOutcome":
        """mastapy.utility.MethodOutcome"""
        method_result = pythonnet_method_call(
            self.wrapped, "TryUpdateCoefficientsFromLossCurveData"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_StatorRotorMaterial":
        """Cast to another type.

        Returns:
            _Cast_StatorRotorMaterial
        """
        return _Cast_StatorRotorMaterial(self)
