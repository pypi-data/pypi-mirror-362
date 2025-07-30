"""InnerBearingRaceMountingOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2666

_INNER_BEARING_RACE_MOUNTING_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "InnerBearingRaceMountingOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InnerBearingRaceMountingOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InnerBearingRaceMountingOptions._Cast_InnerBearingRaceMountingOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InnerBearingRaceMountingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InnerBearingRaceMountingOptions:
    """Special nested class for casting InnerBearingRaceMountingOptions to subclasses."""

    __parent__: "InnerBearingRaceMountingOptions"

    @property
    def bearing_race_mounting_options(
        self: "CastSelf",
    ) -> "_2666.BearingRaceMountingOptions":
        return self.__parent__._cast(_2666.BearingRaceMountingOptions)

    @property
    def inner_bearing_race_mounting_options(
        self: "CastSelf",
    ) -> "InnerBearingRaceMountingOptions":
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
class InnerBearingRaceMountingOptions(_2666.BearingRaceMountingOptions):
    """InnerBearingRaceMountingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INNER_BEARING_RACE_MOUNTING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_InnerBearingRaceMountingOptions":
        """Cast to another type.

        Returns:
            _Cast_InnerBearingRaceMountingOptions
        """
        return _Cast_InnerBearingRaceMountingOptions(self)
