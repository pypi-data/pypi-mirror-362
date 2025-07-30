"""AGMAGleasonConicalRateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.conical import _638

_AGMA_GLEASON_CONICAL_RATEABLE_MESH = python_net_import(
    "SMT.MastaAPI.Gears.Rating.AGMAGleasonConical", "AGMAGleasonConicalRateableMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _458
    from mastapy._private.gears.rating.bevel.standards import _655
    from mastapy._private.gears.rating.hypoid.standards import _535

    Self = TypeVar("Self", bound="AGMAGleasonConicalRateableMesh")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalRateableMesh._Cast_AGMAGleasonConicalRateableMesh",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalRateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalRateableMesh:
    """Special nested class for casting AGMAGleasonConicalRateableMesh to subclasses."""

    __parent__: "AGMAGleasonConicalRateableMesh"

    @property
    def conical_rateable_mesh(self: "CastSelf") -> "_638.ConicalRateableMesh":
        return self.__parent__._cast(_638.ConicalRateableMesh)

    @property
    def rateable_mesh(self: "CastSelf") -> "_458.RateableMesh":
        from mastapy._private.gears.rating import _458

        return self.__parent__._cast(_458.RateableMesh)

    @property
    def hypoid_rateable_mesh(self: "CastSelf") -> "_535.HypoidRateableMesh":
        from mastapy._private.gears.rating.hypoid.standards import _535

        return self.__parent__._cast(_535.HypoidRateableMesh)

    @property
    def spiral_bevel_rateable_mesh(self: "CastSelf") -> "_655.SpiralBevelRateableMesh":
        from mastapy._private.gears.rating.bevel.standards import _655

        return self.__parent__._cast(_655.SpiralBevelRateableMesh)

    @property
    def agma_gleason_conical_rateable_mesh(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalRateableMesh":
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
class AGMAGleasonConicalRateableMesh(_638.ConicalRateableMesh):
    """AGMAGleasonConicalRateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalRateableMesh":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalRateableMesh
        """
        return _Cast_AGMAGleasonConicalRateableMesh(self)
