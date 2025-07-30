"""ScuffingResultsRow"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_SCUFFING_RESULTS_ROW = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "ScuffingResultsRow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical import _542, _565, _576

    Self = TypeVar("Self", bound="ScuffingResultsRow")
    CastSelf = TypeVar("CastSelf", bound="ScuffingResultsRow._Cast_ScuffingResultsRow")


__docformat__ = "restructuredtext en"
__all__ = ("ScuffingResultsRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ScuffingResultsRow:
    """Special nested class for casting ScuffingResultsRow to subclasses."""

    __parent__: "ScuffingResultsRow"

    @property
    def agma_scuffing_results_row(self: "CastSelf") -> "_542.AGMAScuffingResultsRow":
        from mastapy._private.gears.rating.cylindrical import _542

        return self.__parent__._cast(_542.AGMAScuffingResultsRow)

    @property
    def iso_scuffing_results_row(self: "CastSelf") -> "_565.ISOScuffingResultsRow":
        from mastapy._private.gears.rating.cylindrical import _565

        return self.__parent__._cast(_565.ISOScuffingResultsRow)

    @property
    def scuffing_results_row(self: "CastSelf") -> "ScuffingResultsRow":
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
class ScuffingResultsRow(_0.APIBase):
    """ScuffingResultsRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SCUFFING_RESULTS_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactTemperature")

        if temp is None:
            return 0.0

        return temp

    @contact_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ContactTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def flash_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @flash_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def flash_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FlashTemperature", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def index_label(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IndexLabel")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def line_of_action_parameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LineOfActionParameter")

        if temp is None:
            return 0.0

        return temp

    @line_of_action_parameter.setter
    @exception_bridge
    @enforce_parameter_types
    def line_of_action_parameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LineOfActionParameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def load_sharing_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LoadSharingFactor")

        if temp is None:
            return 0.0

        return temp

    @load_sharing_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def load_sharing_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LoadSharingFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_relative_radius_of_curvature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalRelativeRadiusOfCurvature")

        if temp is None:
            return 0.0

        return temp

    @normal_relative_radius_of_curvature.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_relative_radius_of_curvature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalRelativeRadiusOfCurvature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pinion_flank_transverse_radius_of_curvature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "PinionFlankTransverseRadiusOfCurvature"
        )

        if temp is None:
            return 0.0

        return temp

    @pinion_flank_transverse_radius_of_curvature.setter
    @exception_bridge
    @enforce_parameter_types
    def pinion_flank_transverse_radius_of_curvature(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinionFlankTransverseRadiusOfCurvature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pinion_rolling_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionRollingVelocity")

        if temp is None:
            return 0.0

        return temp

    @pinion_rolling_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def pinion_rolling_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinionRollingVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def sliding_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocity")

        if temp is None:
            return 0.0

        return temp

    @sliding_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def sliding_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SlidingVelocity", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def wheel_flank_transverse_radius_of_curvature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "WheelFlankTransverseRadiusOfCurvature"
        )

        if temp is None:
            return 0.0

        return temp

    @wheel_flank_transverse_radius_of_curvature.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_flank_transverse_radius_of_curvature(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelFlankTransverseRadiusOfCurvature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def wheel_rolling_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelRollingVelocity")

        if temp is None:
            return 0.0

        return temp

    @wheel_rolling_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_rolling_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelRollingVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pinion(self: "Self") -> "_576.ScuffingResultsRowGear":
        """mastapy.gears.rating.cylindrical.ScuffingResultsRowGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Pinion")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ScuffingResultsRow":
        """Cast to another type.

        Returns:
            _Cast_ScuffingResultsRow
        """
        return _Cast_ScuffingResultsRow(self)
