"""SingleNodeFELink"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe.links import _2643

_SINGLE_NODE_FE_LINK = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "SingleNodeFELink"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SingleNodeFELink")
    CastSelf = TypeVar("CastSelf", bound="SingleNodeFELink._Cast_SingleNodeFELink")


__docformat__ = "restructuredtext en"
__all__ = ("SingleNodeFELink",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SingleNodeFELink:
    """Special nested class for casting SingleNodeFELink to subclasses."""

    __parent__: "SingleNodeFELink"

    @property
    def fe_link(self: "CastSelf") -> "_2643.FELink":
        return self.__parent__._cast(_2643.FELink)

    @property
    def single_node_fe_link(self: "CastSelf") -> "SingleNodeFELink":
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
class SingleNodeFELink(_2643.FELink):
    """SingleNodeFELink

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SINGLE_NODE_FE_LINK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SingleNodeFELink":
        """Cast to another type.

        Returns:
            _Cast_SingleNodeFELink
        """
        return _Cast_SingleNodeFELink(self)
