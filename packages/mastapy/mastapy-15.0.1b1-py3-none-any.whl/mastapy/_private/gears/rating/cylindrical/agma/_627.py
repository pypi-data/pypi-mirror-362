"""AGMA2101RateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.cylindrical import _562

_AGMA2101_RATEABLE_MESH = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.AGMA", "AGMA2101RateableMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _458

    Self = TypeVar("Self", bound="AGMA2101RateableMesh")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMA2101RateableMesh._Cast_AGMA2101RateableMesh"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMA2101RateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMA2101RateableMesh:
    """Special nested class for casting AGMA2101RateableMesh to subclasses."""

    __parent__: "AGMA2101RateableMesh"

    @property
    def cylindrical_rateable_mesh(self: "CastSelf") -> "_562.CylindricalRateableMesh":
        return self.__parent__._cast(_562.CylindricalRateableMesh)

    @property
    def rateable_mesh(self: "CastSelf") -> "_458.RateableMesh":
        from mastapy._private.gears.rating import _458

        return self.__parent__._cast(_458.RateableMesh)

    @property
    def agma2101_rateable_mesh(self: "CastSelf") -> "AGMA2101RateableMesh":
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
class AGMA2101RateableMesh(_562.CylindricalRateableMesh):
    """AGMA2101RateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA2101_RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMA2101RateableMesh":
        """Cast to another type.

        Returns:
            _Cast_AGMA2101RateableMesh
        """
        return _Cast_AGMA2101RateableMesh(self)
