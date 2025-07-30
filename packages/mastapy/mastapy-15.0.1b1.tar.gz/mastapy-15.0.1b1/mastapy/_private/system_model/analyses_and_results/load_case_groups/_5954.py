"""DutyCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5950

_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups", "DutyCycle"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5949,
        _5957,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7674
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
        _7873,
    )

    Self = TypeVar("Self", bound="DutyCycle")
    CastSelf = TypeVar("CastSelf", bound="DutyCycle._Cast_DutyCycle")


__docformat__ = "restructuredtext en"
__all__ = ("DutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DutyCycle:
    """Special nested class for casting DutyCycle to subclasses."""

    __parent__: "DutyCycle"

    @property
    def abstract_static_load_case_group(
        self: "CastSelf",
    ) -> "_5950.AbstractStaticLoadCaseGroup":
        return self.__parent__._cast(_5950.AbstractStaticLoadCaseGroup)

    @property
    def abstract_load_case_group(self: "CastSelf") -> "_5949.AbstractLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5949,
        )

        return self.__parent__._cast(_5949.AbstractLoadCaseGroup)

    @property
    def duty_cycle(self: "CastSelf") -> "DutyCycle":
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
class DutyCycle(_5950.AbstractStaticLoadCaseGroup):
    """DutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def duty_cycle_design_states(
        self: "Self",
    ) -> "List[_5957.SubGroupInSingleDesignState]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.SubGroupInSingleDesignState]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DutyCycleDesignStates")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def time_series_importer(self: "Self") -> "_7873.TimeSeriesImporter":
        """mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.TimeSeriesImporter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeSeriesImporter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def convert_to_condensed_parametric_study_tool_duty_cycle(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ConvertToCondensedParametricStudyToolDutyCycle"
        )

    @exception_bridge
    @enforce_parameter_types
    def add_static_load(self: "Self", static_load: "_7674.StaticLoadCase") -> None:
        """Method does not return.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
        """
        pythonnet_method_call(
            self.wrapped, "AddStaticLoad", static_load.wrapped if static_load else None
        )

    @exception_bridge
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @exception_bridge
    @enforce_parameter_types
    def remove_design_state_sub_group(
        self: "Self", sub_group: "_5957.SubGroupInSingleDesignState"
    ) -> None:
        """Method does not return.

        Args:
            sub_group (mastapy.system_model.analyses_and_results.load_case_groups.SubGroupInSingleDesignState)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveDesignStateSubGroup",
            sub_group.wrapped if sub_group else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_static_load(self: "Self", static_load: "_7674.StaticLoadCase") -> None:
        """Method does not return.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveStaticLoad",
            static_load.wrapped if static_load else None,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_DutyCycle":
        """Cast to another type.

        Returns:
            _Cast_DutyCycle
        """
        return _Cast_DutyCycle(self)
