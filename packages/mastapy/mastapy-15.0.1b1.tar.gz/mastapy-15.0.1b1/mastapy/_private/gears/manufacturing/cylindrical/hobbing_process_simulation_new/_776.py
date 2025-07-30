"""HobbingProcessSimulationNew"""

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
    _775,
    _789,
)

_HOBBING_PROCESS_SIMULATION_NEW = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "HobbingProcessSimulationNew",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _770,
        _771,
        _772,
        _773,
        _774,
        _778,
    )

    Self = TypeVar("Self", bound="HobbingProcessSimulationNew")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HobbingProcessSimulationNew._Cast_HobbingProcessSimulationNew",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HobbingProcessSimulationNew",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HobbingProcessSimulationNew:
    """Special nested class for casting HobbingProcessSimulationNew to subclasses."""

    __parent__: "HobbingProcessSimulationNew"

    @property
    def process_simulation_new(self: "CastSelf") -> "_789.ProcessSimulationNew":
        return self.__parent__._cast(_789.ProcessSimulationNew)

    @property
    def hobbing_process_simulation_new(
        self: "CastSelf",
    ) -> "HobbingProcessSimulationNew":
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
class HobbingProcessSimulationNew(
    _789.ProcessSimulationNew[_775.HobbingProcessSimulationInput]
):
    """HobbingProcessSimulationNew

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HOBBING_PROCESS_SIMULATION_NEW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def hobbing_process_gear_shape_calculation(
        self: "Self",
    ) -> "_770.HobbingProcessGearShape":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.HobbingProcessGearShape

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HobbingProcessGearShapeCalculation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def hobbing_process_lead_calculation(
        self: "Self",
    ) -> "_771.HobbingProcessLeadCalculation":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.HobbingProcessLeadCalculation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HobbingProcessLeadCalculation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def hobbing_process_mark_on_shaft_calculation(
        self: "Self",
    ) -> "_772.HobbingProcessMarkOnShaft":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.HobbingProcessMarkOnShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HobbingProcessMarkOnShaftCalculation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def hobbing_process_pitch_calculation(
        self: "Self",
    ) -> "_773.HobbingProcessPitchCalculation":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.HobbingProcessPitchCalculation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HobbingProcessPitchCalculation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def hobbing_process_profile_calculation(
        self: "Self",
    ) -> "_774.HobbingProcessProfileCalculation":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.HobbingProcessProfileCalculation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HobbingProcessProfileCalculation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def hobbing_process_total_modification(
        self: "Self",
    ) -> "_778.HobbingProcessTotalModificationCalculation":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.HobbingProcessTotalModificationCalculation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HobbingProcessTotalModification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_HobbingProcessSimulationNew":
        """Cast to another type.

        Returns:
            _Cast_HobbingProcessSimulationNew
        """
        return _Cast_HobbingProcessSimulationNew(self)
