"""CylindricalGearTwoDimensionalFEAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CYLINDRICAL_GEAR_TWO_DIMENSIONAL_FE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.GearTwoDFEAnalysis", "CylindricalGearTwoDimensionalFEAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_two_d_fe_analysis import _1004
    from mastapy._private.nodal_analysis.dev_tools_analyses import _269
    from mastapy._private.nodal_analysis.states import _129

    Self = TypeVar("Self", bound="CylindricalGearTwoDimensionalFEAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearTwoDimensionalFEAnalysis._Cast_CylindricalGearTwoDimensionalFEAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearTwoDimensionalFEAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearTwoDimensionalFEAnalysis:
    """Special nested class for casting CylindricalGearTwoDimensionalFEAnalysis to subclasses."""

    __parent__: "CylindricalGearTwoDimensionalFEAnalysis"

    @property
    def cylindrical_gear_two_dimensional_fe_analysis(
        self: "CastSelf",
    ) -> "CylindricalGearTwoDimensionalFEAnalysis":
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
class CylindricalGearTwoDimensionalFEAnalysis(_0.APIBase):
    """CylindricalGearTwoDimensionalFEAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_TWO_DIMENSIONAL_FE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_stress_states(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfStressStates")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def fe_model(self: "Self") -> "_269.FEModel":
        """mastapy.nodal_analysis.dev_tools_analyses.FEModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def findley_critical_plane_analysis(
        self: "Self",
    ) -> "_1004.FindleyCriticalPlaneAnalysis":
        """mastapy.gears.gear_two_d_fe_analysis.FindleyCriticalPlaneAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FindleyCriticalPlaneAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def get_stress_states(self: "Self", index: "int") -> "_129.NodeVectorState":
        """mastapy.nodal_analysis.states.NodeVectorState

        Args:
            index (int)
        """
        index = int(index)
        method_result = pythonnet_method_call(
            self.wrapped, "GetStressStates", index if index else 0
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def perform(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Perform")

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearTwoDimensionalFEAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearTwoDimensionalFEAnalysis
        """
        return _Cast_CylindricalGearTwoDimensionalFEAnalysis(self)
