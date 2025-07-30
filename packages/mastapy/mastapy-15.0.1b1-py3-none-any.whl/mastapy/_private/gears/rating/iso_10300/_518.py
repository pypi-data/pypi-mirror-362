"""ISO10300RateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.conical import _638

_ISO10300_RATEABLE_MESH = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300RateableMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.rating import _458
    from mastapy._private.gears.rating.virtual_cylindrical_gears import _480

    Self = TypeVar("Self", bound="ISO10300RateableMesh")
    CastSelf = TypeVar(
        "CastSelf", bound="ISO10300RateableMesh._Cast_ISO10300RateableMesh"
    )

T = TypeVar("T", bound="_480.VirtualCylindricalGearBasic")

__docformat__ = "restructuredtext en"
__all__ = ("ISO10300RateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO10300RateableMesh:
    """Special nested class for casting ISO10300RateableMesh to subclasses."""

    __parent__: "ISO10300RateableMesh"

    @property
    def conical_rateable_mesh(self: "CastSelf") -> "_638.ConicalRateableMesh":
        return self.__parent__._cast(_638.ConicalRateableMesh)

    @property
    def rateable_mesh(self: "CastSelf") -> "_458.RateableMesh":
        from mastapy._private.gears.rating import _458

        return self.__parent__._cast(_458.RateableMesh)

    @property
    def iso10300_rateable_mesh(self: "CastSelf") -> "ISO10300RateableMesh":
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
class ISO10300RateableMesh(_638.ConicalRateableMesh, Generic[T]):
    """ISO10300RateableMesh

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _ISO10300_RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ISO10300RateableMesh":
        """Cast to another type.

        Returns:
            _Cast_ISO10300RateableMesh
        """
        return _Cast_ISO10300RateableMesh(self)
