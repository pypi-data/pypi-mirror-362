"""LoadedSelfAligningBallBearingRow"""

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
from mastapy._private.bearings.bearing_results.rolling import _2211

_LOADED_SELF_ALIGNING_BALL_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedSelfAligningBallBearingRow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2242, _2244

    Self = TypeVar("Self", bound="LoadedSelfAligningBallBearingRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedSelfAligningBallBearingRow._Cast_LoadedSelfAligningBallBearingRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedSelfAligningBallBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedSelfAligningBallBearingRow:
    """Special nested class for casting LoadedSelfAligningBallBearingRow to subclasses."""

    __parent__: "LoadedSelfAligningBallBearingRow"

    @property
    def loaded_ball_bearing_row(self: "CastSelf") -> "_2211.LoadedBallBearingRow":
        return self.__parent__._cast(_2211.LoadedBallBearingRow)

    @property
    def loaded_rolling_bearing_row(self: "CastSelf") -> "_2242.LoadedRollingBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2242

        return self.__parent__._cast(_2242.LoadedRollingBearingRow)

    @property
    def loaded_self_aligning_ball_bearing_row(
        self: "CastSelf",
    ) -> "LoadedSelfAligningBallBearingRow":
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
class LoadedSelfAligningBallBearingRow(_2211.LoadedBallBearingRow):
    """LoadedSelfAligningBallBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_SELF_ALIGNING_BALL_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def loaded_bearing(self: "Self") -> "_2244.LoadedSelfAligningBallBearingResults":
        """mastapy.bearings.bearing_results.rolling.LoadedSelfAligningBallBearingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBearing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedSelfAligningBallBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedSelfAligningBallBearingRow
        """
        return _Cast_LoadedSelfAligningBallBearingRow(self)
