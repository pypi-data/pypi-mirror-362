"""FaceGearRating"""

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
from mastapy._private.gears.rating import _452

_FACE_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Face", "FaceGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335
    from mastapy._private.gears.gear_designs.face import _1093
    from mastapy._private.gears.rating import _444

    Self = TypeVar("Self", bound="FaceGearRating")
    CastSelf = TypeVar("CastSelf", bound="FaceGearRating._Cast_FaceGearRating")


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearRating:
    """Special nested class for casting FaceGearRating to subclasses."""

    __parent__: "FaceGearRating"

    @property
    def gear_rating(self: "CastSelf") -> "_452.GearRating":
        return self.__parent__._cast(_452.GearRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_444.AbstractGearRating":
        from mastapy._private.gears.rating import _444

        return self.__parent__._cast(_444.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def face_gear_rating(self: "CastSelf") -> "FaceGearRating":
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
class FaceGearRating(_452.GearRating):
    """FaceGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face_gear(self: "Self") -> "_1093.FaceGearDesign":
        """mastapy.gears.gear_designs.face.FaceGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearRating":
        """Cast to another type.

        Returns:
            _Cast_FaceGearRating
        """
        return _Cast_FaceGearRating(self)
