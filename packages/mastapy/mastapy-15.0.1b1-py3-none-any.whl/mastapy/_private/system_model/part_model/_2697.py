"""OuterBearingRaceMountingOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2666

_OUTER_BEARING_RACE_MOUNTING_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "OuterBearingRaceMountingOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OuterBearingRaceMountingOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="OuterBearingRaceMountingOptions._Cast_OuterBearingRaceMountingOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("OuterBearingRaceMountingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OuterBearingRaceMountingOptions:
    """Special nested class for casting OuterBearingRaceMountingOptions to subclasses."""

    __parent__: "OuterBearingRaceMountingOptions"

    @property
    def bearing_race_mounting_options(
        self: "CastSelf",
    ) -> "_2666.BearingRaceMountingOptions":
        return self.__parent__._cast(_2666.BearingRaceMountingOptions)

    @property
    def outer_bearing_race_mounting_options(
        self: "CastSelf",
    ) -> "OuterBearingRaceMountingOptions":
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
class OuterBearingRaceMountingOptions(_2666.BearingRaceMountingOptions):
    """OuterBearingRaceMountingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OUTER_BEARING_RACE_MOUNTING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_OuterBearingRaceMountingOptions":
        """Cast to another type.

        Returns:
            _Cast_OuterBearingRaceMountingOptions
        """
        return _Cast_OuterBearingRaceMountingOptions(self)
