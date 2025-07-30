"""ScuffingResultsRowGear"""

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

_SCUFFING_RESULTS_ROW_GEAR = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "ScuffingResultsRowGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1135

    Self = TypeVar("Self", bound="ScuffingResultsRowGear")
    CastSelf = TypeVar(
        "CastSelf", bound="ScuffingResultsRowGear._Cast_ScuffingResultsRowGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ScuffingResultsRowGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ScuffingResultsRowGear:
    """Special nested class for casting ScuffingResultsRowGear to subclasses."""

    __parent__: "ScuffingResultsRowGear"

    @property
    def scuffing_results_row_gear(self: "CastSelf") -> "ScuffingResultsRowGear":
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
class ScuffingResultsRowGear(_0.APIBase):
    """ScuffingResultsRowGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SCUFFING_RESULTS_ROW_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def profile_measurement(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileMeasurement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ScuffingResultsRowGear":
        """Cast to another type.

        Returns:
            _Cast_ScuffingResultsRowGear
        """
        return _Cast_ScuffingResultsRowGear(self)
