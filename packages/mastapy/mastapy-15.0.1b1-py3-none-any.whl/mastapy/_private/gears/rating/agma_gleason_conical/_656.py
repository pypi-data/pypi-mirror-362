"""AGMAGleasonConicalGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.conical import _630

_AGMA_GLEASON_CONICAL_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.AGMAGleasonConical", "AGMAGleasonConicalGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.gear_designs.conical import _1289
    from mastapy._private.gears.rating import _443, _451
    from mastapy._private.gears.rating.bevel import _645
    from mastapy._private.gears.rating.hypoid import _529
    from mastapy._private.gears.rating.spiral_bevel import _493
    from mastapy._private.gears.rating.straight_bevel import _486
    from mastapy._private.gears.rating.zerol_bevel import _460

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshRating._Cast_AGMAGleasonConicalGearMeshRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshRating:
    """Special nested class for casting AGMAGleasonConicalGearMeshRating to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshRating"

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
    def zerol_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_460.ZerolBevelGearMeshRating":
        from mastapy._private.gears.rating.zerol_bevel import _460

        return self.__parent__._cast(_460.ZerolBevelGearMeshRating)

    @property
    def straight_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_486.StraightBevelGearMeshRating":
        from mastapy._private.gears.rating.straight_bevel import _486

        return self.__parent__._cast(_486.StraightBevelGearMeshRating)

    @property
    def spiral_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_493.SpiralBevelGearMeshRating":
        from mastapy._private.gears.rating.spiral_bevel import _493

        return self.__parent__._cast(_493.SpiralBevelGearMeshRating)

    @property
    def hypoid_gear_mesh_rating(self: "CastSelf") -> "_529.HypoidGearMeshRating":
        from mastapy._private.gears.rating.hypoid import _529

        return self.__parent__._cast(_529.HypoidGearMeshRating)

    @property
    def bevel_gear_mesh_rating(self: "CastSelf") -> "_645.BevelGearMeshRating":
        from mastapy._private.gears.rating.bevel import _645

        return self.__parent__._cast(_645.BevelGearMeshRating)

    @property
    def agma_gleason_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshRating":
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
class AGMAGleasonConicalGearMeshRating(_630.ConicalGearMeshRating):
    """AGMAGleasonConicalGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def load_distribution_factor_method(
        self: "Self",
    ) -> "_1289.LoadDistributionFactorMethods":
        """mastapy.gears.gear_designs.conical.LoadDistributionFactorMethods

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactorMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.LoadDistributionFactorMethods"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1289",
            "LoadDistributionFactorMethods",
        )(value)

    @property
    @exception_bridge
    def maximum_relative_displacement(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumRelativeDisplacement")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def overload_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverloadFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def overload_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverloadFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshRating
        """
        return _Cast_AGMAGleasonConicalGearMeshRating(self)
