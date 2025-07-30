"""ConicalMeshDutyCycleRating"""

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

_CONICAL_MESH_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalMeshDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.rating import _443
    from mastapy._private.gears.rating.conical import _630

    Self = TypeVar("Self", bound="ConicalMeshDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalMeshDutyCycleRating._Cast_ConicalMeshDutyCycleRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshDutyCycleRating:
    """Special nested class for casting ConicalMeshDutyCycleRating to subclasses."""

    __parent__: "ConicalMeshDutyCycleRating"

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
    def conical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "ConicalMeshDutyCycleRating":
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
class ConicalMeshDutyCycleRating(_456.MeshDutyCycleRating):
    """ConicalMeshDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def conical_mesh_ratings(self: "Self") -> "List[_630.ConicalGearMeshRating]":
        """List[mastapy.gears.rating.conical.ConicalGearMeshRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshDutyCycleRating
        """
        return _Cast_ConicalMeshDutyCycleRating(self)
