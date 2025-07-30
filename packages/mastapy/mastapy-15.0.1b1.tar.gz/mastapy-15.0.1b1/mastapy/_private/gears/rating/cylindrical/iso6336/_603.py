"""ISO63361996MeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical.iso6336 import _611

_ISO63361996_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336", "ISO63361996MeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _457
    from mastapy._private.gears.rating.cylindrical import _558
    from mastapy._private.gears.rating.cylindrical.din3990 import _624
    from mastapy._private.gears.rating.cylindrical.iso6336 import _609

    Self = TypeVar("Self", bound="ISO63361996MeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO63361996MeshSingleFlankRating._Cast_ISO63361996MeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO63361996MeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO63361996MeshSingleFlankRating:
    """Special nested class for casting ISO63361996MeshSingleFlankRating to subclasses."""

    __parent__: "ISO63361996MeshSingleFlankRating"

    @property
    def iso6336_abstract_metal_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_611.ISO6336AbstractMetalMeshSingleFlankRating":
        return self.__parent__._cast(_611.ISO6336AbstractMetalMeshSingleFlankRating)

    @property
    def iso6336_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_609.ISO6336AbstractMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _609

        return self.__parent__._cast(_609.ISO6336AbstractMeshSingleFlankRating)

    @property
    def cylindrical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_558.CylindricalMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _558

        return self.__parent__._cast(_558.CylindricalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_457.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _457

        return self.__parent__._cast(_457.MeshSingleFlankRating)

    @property
    def din3990_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_624.DIN3990MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.din3990 import _624

        return self.__parent__._cast(_624.DIN3990MeshSingleFlankRating)

    @property
    def iso63361996_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "ISO63361996MeshSingleFlankRating":
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
class ISO63361996MeshSingleFlankRating(_611.ISO6336AbstractMetalMeshSingleFlankRating):
    """ISO63361996MeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO63361996_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def helix_angle_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngleFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rating_standard_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingStandardName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def transverse_load_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseLoadFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO63361996MeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO63361996MeshSingleFlankRating
        """
        return _Cast_ISO63361996MeshSingleFlankRating(self)
