"""GearSetOptimisationResults"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEAR_SET_OPTIMISATION_RESULTS = python_net_import(
    "SMT.MastaAPI.Gears", "GearSetOptimisationResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _419

    Self = TypeVar("Self", bound="GearSetOptimisationResults")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetOptimisationResults._Cast_GearSetOptimisationResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetOptimisationResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetOptimisationResults:
    """Special nested class for casting GearSetOptimisationResults to subclasses."""

    __parent__: "GearSetOptimisationResults"

    @property
    def gear_set_optimisation_results(self: "CastSelf") -> "GearSetOptimisationResults":
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
class GearSetOptimisationResults(_0.APIBase):
    """GearSetOptimisationResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_OPTIMISATION_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def optimiser_settings_report_table(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OptimiserSettingsReportTable")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def report(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Report")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def results(self: "Self") -> "List[_419.GearSetOptimisationResult]":
        """List[mastapy.gears.GearSetOptimisationResult]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Results")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def run_time(self: "Self") -> "datetime":
        """datetime

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RunTime")

        if temp is None:
            return None

        value = conversion.pn_to_mp_datetime(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def delete_all_results(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteAllResults")

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetOptimisationResults":
        """Cast to another type.

        Returns:
            _Cast_GearSetOptimisationResults
        """
        return _Cast_GearSetOptimisationResults(self)
