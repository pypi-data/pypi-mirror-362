"""LoadedDeepGrooveBallBearingElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2208

_LOADED_DEEP_GROOVE_BALL_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedDeepGrooveBallBearingElement"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2222

    Self = TypeVar("Self", bound="LoadedDeepGrooveBallBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedDeepGrooveBallBearingElement._Cast_LoadedDeepGrooveBallBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedDeepGrooveBallBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedDeepGrooveBallBearingElement:
    """Special nested class for casting LoadedDeepGrooveBallBearingElement to subclasses."""

    __parent__: "LoadedDeepGrooveBallBearingElement"

    @property
    def loaded_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2208.LoadedBallBearingElement":
        return self.__parent__._cast(_2208.LoadedBallBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "_2222.LoadedElement":
        from mastapy._private.bearings.bearing_results.rolling import _2222

        return self.__parent__._cast(_2222.LoadedElement)

    @property
    def loaded_deep_groove_ball_bearing_element(
        self: "CastSelf",
    ) -> "LoadedDeepGrooveBallBearingElement":
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
class LoadedDeepGrooveBallBearingElement(_2208.LoadedBallBearingElement):
    """LoadedDeepGrooveBallBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_DEEP_GROOVE_BALL_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedDeepGrooveBallBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedDeepGrooveBallBearingElement
        """
        return _Cast_LoadedDeepGrooveBallBearingElement(self)
