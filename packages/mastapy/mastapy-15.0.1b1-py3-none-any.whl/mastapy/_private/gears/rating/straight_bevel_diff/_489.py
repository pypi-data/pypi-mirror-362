"""StraightBevelDiffGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.conical import _630

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.StraightBevelDiff", "StraightBevelDiffGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _1070
    from mastapy._private.gears.rating import _443, _451
    from mastapy._private.gears.rating.straight_bevel_diff import _490, _492

    Self = TypeVar("Self", bound="StraightBevelDiffGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearMeshRating._Cast_StraightBevelDiffGearMeshRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearMeshRating:
    """Special nested class for casting StraightBevelDiffGearMeshRating to subclasses."""

    __parent__: "StraightBevelDiffGearMeshRating"

    @property
    def conical_gear_mesh_rating(self: "CastSelf") -> "_630.ConicalGearMeshRating":
        return self.__parent__._cast(_630.ConicalGearMeshRating)

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_451.GearMeshRating":
        from mastapy._private.gears.rating import _451

        return self.__parent__._cast(_451.GearMeshRating)

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
    def straight_bevel_diff_gear_mesh_rating(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearMeshRating":
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
class StraightBevelDiffGearMeshRating(_630.ConicalGearMeshRating):
    """StraightBevelDiffGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def derating_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DeratingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inertia_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InertiaFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_distribution_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rating_result(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingResult")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def straight_bevel_diff_gear_mesh(
        self: "Self",
    ) -> "_1070.StraightBevelDiffGearMeshDesign":
        """mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGearMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def meshed_gears(self: "Self") -> "List[_492.StraightBevelDiffMeshedGearRating]":
        """List[mastapy.gears.rating.straight_bevel_diff.StraightBevelDiffMeshedGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gears_in_mesh(self: "Self") -> "List[_492.StraightBevelDiffMeshedGearRating]":
        """List[mastapy.gears.rating.straight_bevel_diff.StraightBevelDiffMeshedGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsInMesh")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def straight_bevel_diff_gear_ratings(
        self: "Self",
    ) -> "List[_490.StraightBevelDiffGearRating]":
        """List[mastapy.gears.rating.straight_bevel_diff.StraightBevelDiffGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearMeshRating
        """
        return _Cast_StraightBevelDiffGearMeshRating(self)
