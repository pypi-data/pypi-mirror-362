"""FormWheelGrindingSimulationCalculator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _834

_FORM_WHEEL_GRINDING_SIMULATION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "FormWheelGrindingSimulationCalculator",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _827

    Self = TypeVar("Self", bound="FormWheelGrindingSimulationCalculator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FormWheelGrindingSimulationCalculator._Cast_FormWheelGrindingSimulationCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FormWheelGrindingSimulationCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FormWheelGrindingSimulationCalculator:
    """Special nested class for casting FormWheelGrindingSimulationCalculator to subclasses."""

    __parent__: "FormWheelGrindingSimulationCalculator"

    @property
    def cutter_simulation_calc(self: "CastSelf") -> "_834.CutterSimulationCalc":
        return self.__parent__._cast(_834.CutterSimulationCalc)

    @property
    def form_wheel_grinding_simulation_calculator(
        self: "CastSelf",
    ) -> "FormWheelGrindingSimulationCalculator":
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
class FormWheelGrindingSimulationCalculator(_834.CutterSimulationCalc):
    """FormWheelGrindingSimulationCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FORM_WHEEL_GRINDING_SIMULATION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def finish_depth_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishDepthRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limiting_finish_depth_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitingFinishDepthRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_root_fillet_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseRootFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def profiled_grinding_wheel(
        self: "Self",
    ) -> "_827.CylindricalGearFormedWheelGrinderTangible":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.CylindricalGearFormedWheelGrinderTangible

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfiledGrindingWheel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FormWheelGrindingSimulationCalculator":
        """Cast to another type.

        Returns:
            _Cast_FormWheelGrindingSimulationCalculator
        """
        return _Cast_FormWheelGrindingSimulationCalculator(self)
