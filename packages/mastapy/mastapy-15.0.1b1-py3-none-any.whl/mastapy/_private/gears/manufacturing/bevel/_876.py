"""BevelMachineSettingOptimizationResult"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_BEVEL_MACHINE_SETTING_OPTIMIZATION_RESULT = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "BevelMachineSettingOptimizationResult"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.bevel import _877

    Self = TypeVar("Self", bound="BevelMachineSettingOptimizationResult")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelMachineSettingOptimizationResult._Cast_BevelMachineSettingOptimizationResult",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelMachineSettingOptimizationResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelMachineSettingOptimizationResult:
    """Special nested class for casting BevelMachineSettingOptimizationResult to subclasses."""

    __parent__: "BevelMachineSettingOptimizationResult"

    @property
    def bevel_machine_setting_optimization_result(
        self: "CastSelf",
    ) -> "BevelMachineSettingOptimizationResult":
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
class BevelMachineSettingOptimizationResult(_0.APIBase):
    """BevelMachineSettingOptimizationResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_MACHINE_SETTING_OPTIMIZATION_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_absolute_residual(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumAbsoluteResidual")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sum_of_squared_residuals(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SumOfSquaredResiduals")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def calculated_deviations_concave(
        self: "Self",
    ) -> "_877.ConicalFlankDeviationsData":
        """mastapy.gears.manufacturing.bevel.ConicalFlankDeviationsData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedDeviationsConcave")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def calculated_deviations_convex(self: "Self") -> "_877.ConicalFlankDeviationsData":
        """mastapy.gears.manufacturing.bevel.ConicalFlankDeviationsData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedDeviationsConvex")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def imported_deviations_concave(self: "Self") -> "_877.ConicalFlankDeviationsData":
        """mastapy.gears.manufacturing.bevel.ConicalFlankDeviationsData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ImportedDeviationsConcave")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def imported_deviations_convex(self: "Self") -> "_877.ConicalFlankDeviationsData":
        """mastapy.gears.manufacturing.bevel.ConicalFlankDeviationsData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ImportedDeviationsConvex")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelMachineSettingOptimizationResult":
        """Cast to another type.

        Returns:
            _Cast_BevelMachineSettingOptimizationResult
        """
        return _Cast_BevelMachineSettingOptimizationResult(self)
