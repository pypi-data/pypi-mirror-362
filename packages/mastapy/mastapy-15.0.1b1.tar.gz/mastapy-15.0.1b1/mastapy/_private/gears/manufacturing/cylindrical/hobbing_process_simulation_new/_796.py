"""WormGrindingLeadCalculation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _797,
)

_WORM_GRINDING_LEAD_CALCULATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "WormGrindingLeadCalculation",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _763,
        _783,
    )
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="WormGrindingLeadCalculation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGrindingLeadCalculation._Cast_WormGrindingLeadCalculation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGrindingLeadCalculation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGrindingLeadCalculation:
    """Special nested class for casting WormGrindingLeadCalculation to subclasses."""

    __parent__: "WormGrindingLeadCalculation"

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
    def worm_grinding_lead_calculation(
        self: "CastSelf",
    ) -> "WormGrindingLeadCalculation":
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
class WormGrindingLeadCalculation(_797.WormGrindingProcessCalculation):
    """WormGrindingLeadCalculation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GRINDING_LEAD_CALCULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def left_flank_lead_modification_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankLeadModificationChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def radius_for_lead_modification_calculation(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RadiusForLeadModificationCalculation"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @radius_for_lead_modification_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def radius_for_lead_modification_calculation(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "RadiusForLeadModificationCalculation", value
        )

    @property
    @exception_bridge
    def right_flank_lead_modification_chart(
        self: "Self",
    ) -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankLeadModificationChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def left_flank(self: "Self") -> "_763.CalculateLeadDeviationAccuracy":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.CalculateLeadDeviationAccuracy

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank(self: "Self") -> "_763.CalculateLeadDeviationAccuracy":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.CalculateLeadDeviationAccuracy

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WormGrindingLeadCalculation":
        """Cast to another type.

        Returns:
            _Cast_WormGrindingLeadCalculation
        """
        return _Cast_WormGrindingLeadCalculation(self)
