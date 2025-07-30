"""WormMeshDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _456

_WORM_MESH_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Worm", "WormMeshDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.rating import _443
    from mastapy._private.gears.rating.worm import _464

    Self = TypeVar("Self", bound="WormMeshDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf", bound="WormMeshDutyCycleRating._Cast_WormMeshDutyCycleRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormMeshDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormMeshDutyCycleRating:
    """Special nested class for casting WormMeshDutyCycleRating to subclasses."""

    __parent__: "WormMeshDutyCycleRating"

    @property
    def mesh_duty_cycle_rating(self: "CastSelf") -> "_456.MeshDutyCycleRating":
        return self.__parent__._cast(_456.MeshDutyCycleRating)

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "_443.AbstractGearMeshRating":
        from mastapy._private.gears.rating import _443

        return self.__parent__._cast(_443.AbstractGearMeshRating)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def worm_mesh_duty_cycle_rating(self: "CastSelf") -> "WormMeshDutyCycleRating":
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
class WormMeshDutyCycleRating(_456.MeshDutyCycleRating):
    """WormMeshDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_MESH_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def worm_mesh_ratings(self: "Self") -> "List[_464.WormGearMeshRating]":
        """List[mastapy.gears.rating.worm.WormGearMeshRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormMeshRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_WormMeshDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_WormMeshDutyCycleRating
        """
        return _Cast_WormMeshDutyCycleRating(self)
