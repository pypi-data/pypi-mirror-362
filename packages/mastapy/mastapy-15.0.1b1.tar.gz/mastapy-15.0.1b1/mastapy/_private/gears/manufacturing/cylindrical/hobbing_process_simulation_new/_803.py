"""WormGrindingProcessSimulationNew"""

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
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _789,
    _802,
)

_WORM_GRINDING_PROCESS_SIMULATION_NEW = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "WormGrindingProcessSimulationNew",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _795,
        _796,
        _798,
        _799,
        _800,
        _801,
        _805,
    )

    Self = TypeVar("Self", bound="WormGrindingProcessSimulationNew")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGrindingProcessSimulationNew._Cast_WormGrindingProcessSimulationNew",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGrindingProcessSimulationNew",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGrindingProcessSimulationNew:
    """Special nested class for casting WormGrindingProcessSimulationNew to subclasses."""

    __parent__: "WormGrindingProcessSimulationNew"

    @property
    def process_simulation_new(self: "CastSelf") -> "_789.ProcessSimulationNew":
        return self.__parent__._cast(_789.ProcessSimulationNew)

    @property
    def worm_grinding_process_simulation_new(
        self: "CastSelf",
    ) -> "WormGrindingProcessSimulationNew":
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
class WormGrindingProcessSimulationNew(
    _789.ProcessSimulationNew[_802.WormGrindingProcessSimulationInput]
):
    """WormGrindingProcessSimulationNew

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GRINDING_PROCESS_SIMULATION_NEW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def worm_grinding_cutter_calculation(
        self: "Self",
    ) -> "_795.WormGrindingCutterCalculation":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.WormGrindingCutterCalculation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGrindingCutterCalculation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def worm_grinding_process_gear_shape_calculation(
        self: "Self",
    ) -> "_798.WormGrindingProcessGearShape":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.WormGrindingProcessGearShape

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WormGrindingProcessGearShapeCalculation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def worm_grinding_process_lead_calculation(
        self: "Self",
    ) -> "_796.WormGrindingLeadCalculation":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.WormGrindingLeadCalculation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WormGrindingProcessLeadCalculation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def worm_grinding_process_mark_on_shaft_calculation(
        self: "Self",
    ) -> "_799.WormGrindingProcessMarkOnShaft":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.WormGrindingProcessMarkOnShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WormGrindingProcessMarkOnShaftCalculation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def worm_grinding_process_pitch_calculation(
        self: "Self",
    ) -> "_800.WormGrindingProcessPitchCalculation":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.WormGrindingProcessPitchCalculation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WormGrindingProcessPitchCalculation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def worm_grinding_process_profile_calculation(
        self: "Self",
    ) -> "_801.WormGrindingProcessProfileCalculation":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.WormGrindingProcessProfileCalculation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WormGrindingProcessProfileCalculation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def worm_grinding_process_total_modification_calculation(
        self: "Self",
    ) -> "_805.WormGrindingProcessTotalModificationCalculation":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.WormGrindingProcessTotalModificationCalculation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WormGrindingProcessTotalModificationCalculation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WormGrindingProcessSimulationNew":
        """Cast to another type.

        Returns:
            _Cast_WormGrindingProcessSimulationNew
        """
        return _Cast_WormGrindingProcessSimulationNew(self)
