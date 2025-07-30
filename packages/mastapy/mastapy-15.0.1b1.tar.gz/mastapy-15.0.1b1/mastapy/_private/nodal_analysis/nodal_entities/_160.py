"""RigidBar"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _153

_RIGID_BAR = python_net_import("SMT.MastaAPI.NodalAnalysis.NodalEntities", "RigidBar")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _155

    Self = TypeVar("Self", bound="RigidBar")
    CastSelf = TypeVar("CastSelf", bound="RigidBar._Cast_RigidBar")


__docformat__ = "restructuredtext en"
__all__ = ("RigidBar",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RigidBar:
    """Special nested class for casting RigidBar to subclasses."""

    __parent__: "RigidBar"

    @property
    def nodal_component(self: "CastSelf") -> "_153.NodalComponent":
        return self.__parent__._cast(_153.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def rigid_bar(self: "CastSelf") -> "RigidBar":
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
class RigidBar(_153.NodalComponent):
    """RigidBar

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RIGID_BAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RigidBar":
        """Cast to another type.

        Returns:
            _Cast_RigidBar
        """
        return _Cast_RigidBar(self)
