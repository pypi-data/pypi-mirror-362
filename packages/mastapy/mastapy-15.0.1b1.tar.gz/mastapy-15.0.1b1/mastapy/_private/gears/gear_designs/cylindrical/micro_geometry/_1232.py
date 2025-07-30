"""LinearCylindricalGearTriangularEndModification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1247

_LINEAR_CYLINDRICAL_GEAR_TRIANGULAR_END_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "LinearCylindricalGearTriangularEndModification",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LinearCylindricalGearTriangularEndModification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LinearCylindricalGearTriangularEndModification._Cast_LinearCylindricalGearTriangularEndModification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LinearCylindricalGearTriangularEndModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LinearCylindricalGearTriangularEndModification:
    """Special nested class for casting LinearCylindricalGearTriangularEndModification to subclasses."""

    __parent__: "LinearCylindricalGearTriangularEndModification"

    @property
    def single_cylindrical_gear_triangular_end_modification(
        self: "CastSelf",
    ) -> "_1247.SingleCylindricalGearTriangularEndModification":
        return self.__parent__._cast(
            _1247.SingleCylindricalGearTriangularEndModification
        )

    @property
    def linear_cylindrical_gear_triangular_end_modification(
        self: "CastSelf",
    ) -> "LinearCylindricalGearTriangularEndModification":
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
class LinearCylindricalGearTriangularEndModification(
    _1247.SingleCylindricalGearTriangularEndModification
):
    """LinearCylindricalGearTriangularEndModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LINEAR_CYLINDRICAL_GEAR_TRIANGULAR_END_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LinearCylindricalGearTriangularEndModification":
        """Cast to another type.

        Returns:
            _Cast_LinearCylindricalGearTriangularEndModification
        """
        return _Cast_LinearCylindricalGearTriangularEndModification(self)
