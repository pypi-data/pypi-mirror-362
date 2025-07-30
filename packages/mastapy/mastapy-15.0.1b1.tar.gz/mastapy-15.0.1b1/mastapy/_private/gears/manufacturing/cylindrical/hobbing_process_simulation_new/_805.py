"""WormGrindingProcessTotalModificationCalculation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _797,
)

_WORM_GRINDING_PROCESS_TOTAL_MODIFICATION_CALCULATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "WormGrindingProcessTotalModificationCalculation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _783,
    )
    from mastapy._private.utility_gui.charts import _2068

    Self = TypeVar("Self", bound="WormGrindingProcessTotalModificationCalculation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGrindingProcessTotalModificationCalculation._Cast_WormGrindingProcessTotalModificationCalculation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGrindingProcessTotalModificationCalculation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGrindingProcessTotalModificationCalculation:
    """Special nested class for casting WormGrindingProcessTotalModificationCalculation to subclasses."""

    __parent__: "WormGrindingProcessTotalModificationCalculation"

    @property
    def worm_grinding_process_calculation(
        self: "CastSelf",
    ) -> "_797.WormGrindingProcessCalculation":
        return self.__parent__._cast(_797.WormGrindingProcessCalculation)

    @property
    def process_calculation(self: "CastSelf") -> "_783.ProcessCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _783,
        )

        return self.__parent__._cast(_783.ProcessCalculation)

    @property
    def worm_grinding_process_total_modification_calculation(
        self: "CastSelf",
    ) -> "WormGrindingProcessTotalModificationCalculation":
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
class WormGrindingProcessTotalModificationCalculation(
    _797.WormGrindingProcessCalculation
):
    """WormGrindingProcessTotalModificationCalculation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GRINDING_PROCESS_TOTAL_MODIFICATION_CALCULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def lead_range_max(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LeadRangeMax")

        if temp is None:
            return 0.0

        return temp

    @lead_range_max.setter
    @exception_bridge
    @enforce_parameter_types
    def lead_range_max(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LeadRangeMax", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def lead_range_min(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LeadRangeMin")

        if temp is None:
            return 0.0

        return temp

    @lead_range_min.setter
    @exception_bridge
    @enforce_parameter_types
    def lead_range_min(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LeadRangeMin", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def number_of_lead_bands(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfLeadBands")

        if temp is None:
            return 0

        return temp

    @number_of_lead_bands.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_lead_bands(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfLeadBands", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_profile_bands(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfProfileBands")

        if temp is None:
            return 0

        return temp

    @number_of_profile_bands.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_profile_bands(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfProfileBands", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def total_errors_chart_left_flank(self: "Self") -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalErrorsChartLeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def total_errors_chart_right_flank(self: "Self") -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalErrorsChartRightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_WormGrindingProcessTotalModificationCalculation":
        """Cast to another type.

        Returns:
            _Cast_WormGrindingProcessTotalModificationCalculation
        """
        return _Cast_WormGrindingProcessTotalModificationCalculation(self)
