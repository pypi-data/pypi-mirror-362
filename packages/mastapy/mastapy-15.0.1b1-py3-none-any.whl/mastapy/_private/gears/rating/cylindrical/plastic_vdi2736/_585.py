"""PlasticPlasticVDI2736MeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _583

_PLASTIC_PLASTIC_VDI2736_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.PlasticVDI2736",
    "PlasticPlasticVDI2736MeshSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _457
    from mastapy._private.gears.rating.cylindrical import _558
    from mastapy._private.gears.rating.cylindrical.iso6336 import _609

    Self = TypeVar("Self", bound="PlasticPlasticVDI2736MeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlasticPlasticVDI2736MeshSingleFlankRating._Cast_PlasticPlasticVDI2736MeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlasticPlasticVDI2736MeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlasticPlasticVDI2736MeshSingleFlankRating:
    """Special nested class for casting PlasticPlasticVDI2736MeshSingleFlankRating to subclasses."""

    __parent__: "PlasticPlasticVDI2736MeshSingleFlankRating"

    @property
    def plastic_gear_vdi2736_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_583.PlasticGearVDI2736AbstractMeshSingleFlankRating":
        return self.__parent__._cast(
            _583.PlasticGearVDI2736AbstractMeshSingleFlankRating
        )

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
    def plastic_plastic_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "PlasticPlasticVDI2736MeshSingleFlankRating":
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
class PlasticPlasticVDI2736MeshSingleFlankRating(
    _583.PlasticGearVDI2736AbstractMeshSingleFlankRating
):
    """PlasticPlasticVDI2736MeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLASTIC_PLASTIC_VDI2736_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PlasticPlasticVDI2736MeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_PlasticPlasticVDI2736MeshSingleFlankRating
        """
        return _Cast_PlasticPlasticVDI2736MeshSingleFlankRating(self)
