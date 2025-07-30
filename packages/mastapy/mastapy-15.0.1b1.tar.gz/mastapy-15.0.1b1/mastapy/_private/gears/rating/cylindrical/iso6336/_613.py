"""ISO6336MetalRateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.cylindrical.iso6336 import _614

_ISO6336_METAL_RATEABLE_MESH = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336", "ISO6336MetalRateableMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _458
    from mastapy._private.gears.rating.cylindrical import _562

    Self = TypeVar("Self", bound="ISO6336MetalRateableMesh")
    CastSelf = TypeVar(
        "CastSelf", bound="ISO6336MetalRateableMesh._Cast_ISO6336MetalRateableMesh"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO6336MetalRateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO6336MetalRateableMesh:
    """Special nested class for casting ISO6336MetalRateableMesh to subclasses."""

    __parent__: "ISO6336MetalRateableMesh"

    @property
    def iso6336_rateable_mesh(self: "CastSelf") -> "_614.ISO6336RateableMesh":
        return self.__parent__._cast(_614.ISO6336RateableMesh)

    @property
    def cylindrical_rateable_mesh(self: "CastSelf") -> "_562.CylindricalRateableMesh":
        from mastapy._private.gears.rating.cylindrical import _562

        return self.__parent__._cast(_562.CylindricalRateableMesh)

    @property
    def rateable_mesh(self: "CastSelf") -> "_458.RateableMesh":
        from mastapy._private.gears.rating import _458

        return self.__parent__._cast(_458.RateableMesh)

    @property
    def iso6336_metal_rateable_mesh(self: "CastSelf") -> "ISO6336MetalRateableMesh":
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
class ISO6336MetalRateableMesh(_614.ISO6336RateableMesh):
    """ISO6336MetalRateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO6336_METAL_RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ISO6336MetalRateableMesh":
        """Cast to another type.

        Returns:
            _Cast_ISO6336MetalRateableMesh
        """
        return _Cast_ISO6336MetalRateableMesh(self)
