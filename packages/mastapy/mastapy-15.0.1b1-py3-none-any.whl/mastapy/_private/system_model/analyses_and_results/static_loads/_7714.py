"""ConicalGearManufactureError"""

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
from mastapy._private.system_model.analyses_and_results.static_loads import _7760

_CONICAL_GEAR_MANUFACTURE_ERROR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ConicalGearManufactureError",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1718

    Self = TypeVar("Self", bound="ConicalGearManufactureError")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearManufactureError._Cast_ConicalGearManufactureError",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearManufactureError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearManufactureError:
    """Special nested class for casting ConicalGearManufactureError to subclasses."""

    __parent__: "ConicalGearManufactureError"

    @property
    def gear_manufacture_error(self: "CastSelf") -> "_7760.GearManufactureError":
        return self.__parent__._cast(_7760.GearManufactureError)

    @property
    def conical_gear_manufacture_error(
        self: "CastSelf",
    ) -> "ConicalGearManufactureError":
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
class ConicalGearManufactureError(_7760.GearManufactureError):
    """ConicalGearManufactureError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MANUFACTURE_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def pitch_error_phase_shift_on_concave_flank(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "PitchErrorPhaseShiftOnConcaveFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @pitch_error_phase_shift_on_concave_flank.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_error_phase_shift_on_concave_flank(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PitchErrorPhaseShiftOnConcaveFlank",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pitch_error_phase_shift_on_convex_flank(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PitchErrorPhaseShiftOnConvexFlank")

        if temp is None:
            return 0.0

        return temp

    @pitch_error_phase_shift_on_convex_flank.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_error_phase_shift_on_convex_flank(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PitchErrorPhaseShiftOnConvexFlank",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pitch_errors_concave_flank(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "PitchErrorsConcaveFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @pitch_errors_concave_flank.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_errors_concave_flank(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "PitchErrorsConcaveFlank", value.wrapped)

    @property
    @exception_bridge
    def pitch_errors_convex_flank(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "PitchErrorsConvexFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @pitch_errors_convex_flank.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_errors_convex_flank(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "PitchErrorsConvexFlank", value.wrapped)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearManufactureError":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearManufactureError
        """
        return _Cast_ConicalGearManufactureError(self)
