"""KlingelnbergConicalRateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating import _458

_KLINGELNBERG_CONICAL_RATEABLE_MESH = python_net_import(
    "SMT.MastaAPI.Gears.Rating.KlingelnbergConical.KN3030",
    "KlingelnbergConicalRateableMesh",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="KlingelnbergConicalRateableMesh")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergConicalRateableMesh._Cast_KlingelnbergConicalRateableMesh",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergConicalRateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergConicalRateableMesh:
    """Special nested class for casting KlingelnbergConicalRateableMesh to subclasses."""

    __parent__: "KlingelnbergConicalRateableMesh"

    @property
    def rateable_mesh(self: "CastSelf") -> "_458.RateableMesh":
        return self.__parent__._cast(_458.RateableMesh)

    @property
    def klingelnberg_conical_rateable_mesh(
        self: "CastSelf",
    ) -> "KlingelnbergConicalRateableMesh":
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
class KlingelnbergConicalRateableMesh(_458.RateableMesh):
    """KlingelnbergConicalRateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CONICAL_RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergConicalRateableMesh":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergConicalRateableMesh
        """
        return _Cast_KlingelnbergConicalRateableMesh(self)
