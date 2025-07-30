"""AbstractShaftOrHousingLoadCase"""

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
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5770
from mastapy._private.system_model.analyses_and_results.static_loads import _7706

_ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractShaftOrHousingLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7676,
        _7728,
        _7756,
        _7799,
        _7821,
    )
    from mastapy._private.system_model.part_model import _2661

    Self = TypeVar("Self", bound="AbstractShaftOrHousingLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftOrHousingLoadCase._Cast_AbstractShaftOrHousingLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousingLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousingLoadCase:
    """Special nested class for casting AbstractShaftOrHousingLoadCase to subclasses."""

    __parent__: "AbstractShaftOrHousingLoadCase"

    @property
    def component_load_case(self: "CastSelf") -> "_7706.ComponentLoadCase":
        return self.__parent__._cast(_7706.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7799,
        )

        return self.__parent__._cast(_7799.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def abstract_shaft_load_case(self: "CastSelf") -> "_7676.AbstractShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7676,
        )

        return self.__parent__._cast(_7676.AbstractShaftLoadCase)

    @property
    def cycloidal_disc_load_case(self: "CastSelf") -> "_7728.CycloidalDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7728,
        )

        return self.__parent__._cast(_7728.CycloidalDiscLoadCase)

    @property
    def fe_part_load_case(self: "CastSelf") -> "_7756.FEPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7756,
        )

        return self.__parent__._cast(_7756.FEPartLoadCase)

    @property
    def shaft_load_case(self: "CastSelf") -> "_7821.ShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7821,
        )

        return self.__parent__._cast(_7821.ShaftLoadCase)

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "AbstractShaftOrHousingLoadCase":
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
class AbstractShaftOrHousingLoadCase(_7706.ComponentLoadCase):
    """AbstractShaftOrHousingLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def include_flexibilities_setting(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.mbd_analyses.ShaftAndHousingFlexibilityOption]"""
        temp = pythonnet_property_get(self.wrapped, "IncludeFlexibilitiesSetting")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @include_flexibilities_setting.setter
    @exception_bridge
    @enforce_parameter_types
    def include_flexibilities_setting(
        self: "Self", value: "_5770.ShaftAndHousingFlexibilityOption"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "IncludeFlexibilitiesSetting", value)

    @property
    @exception_bridge
    def rayleigh_damping_alpha(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingAlpha")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rayleigh_damping_alpha.setter
    @exception_bridge
    @enforce_parameter_types
    def rayleigh_damping_alpha(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RayleighDampingAlpha", value)

    @property
    @exception_bridge
    def temperature(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Temperature")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def temperature(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Temperature", value)

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2661.AbstractShaftOrHousing":
        """mastapy.system_model.part_model.AbstractShaftOrHousing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftOrHousingLoadCase":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousingLoadCase
        """
        return _Cast_AbstractShaftOrHousingLoadCase(self)
