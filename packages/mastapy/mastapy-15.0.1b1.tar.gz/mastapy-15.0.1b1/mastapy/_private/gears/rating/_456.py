"""MeshDutyCycleRating"""

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
from mastapy._private.gears.rating import _443

_MESH_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "MeshDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.rating import _448
    from mastapy._private.gears.rating.concept import _640
    from mastapy._private.gears.rating.conical import _635
    from mastapy._private.gears.rating.cylindrical import _557
    from mastapy._private.gears.rating.face import _537
    from mastapy._private.gears.rating.worm import _468

    Self = TypeVar("Self", bound="MeshDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf", bound="MeshDutyCycleRating._Cast_MeshDutyCycleRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeshDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshDutyCycleRating:
    """Special nested class for casting MeshDutyCycleRating to subclasses."""

    __parent__: "MeshDutyCycleRating"

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "_443.AbstractGearMeshRating":
        return self.__parent__._cast(_443.AbstractGearMeshRating)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def worm_mesh_duty_cycle_rating(self: "CastSelf") -> "_468.WormMeshDutyCycleRating":
        from mastapy._private.gears.rating.worm import _468

        return self.__parent__._cast(_468.WormMeshDutyCycleRating)

    @property
    def face_gear_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_537.FaceGearMeshDutyCycleRating":
        from mastapy._private.gears.rating.face import _537

        return self.__parent__._cast(_537.FaceGearMeshDutyCycleRating)

    @property
    def cylindrical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_557.CylindricalMeshDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _557

        return self.__parent__._cast(_557.CylindricalMeshDutyCycleRating)

    @property
    def conical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_635.ConicalMeshDutyCycleRating":
        from mastapy._private.gears.rating.conical import _635

        return self.__parent__._cast(_635.ConicalMeshDutyCycleRating)

    @property
    def concept_gear_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_640.ConceptGearMeshDutyCycleRating":
        from mastapy._private.gears.rating.concept import _640

        return self.__parent__._cast(_640.ConceptGearMeshDutyCycleRating)

    @property
    def mesh_duty_cycle_rating(self: "CastSelf") -> "MeshDutyCycleRating":
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
class MeshDutyCycleRating(_443.AbstractGearMeshRating):
    """MeshDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESH_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def calculated_energy_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedEnergyLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def calculated_mesh_efficiency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedMeshEfficiency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_energy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalEnergy")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_duty_cycle_ratings(self: "Self") -> "List[_448.GearDutyCycleRating]":
        """List[mastapy.gears.rating.GearDutyCycleRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearDutyCycleRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_MeshDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_MeshDutyCycleRating
        """
        return _Cast_MeshDutyCycleRating(self)
