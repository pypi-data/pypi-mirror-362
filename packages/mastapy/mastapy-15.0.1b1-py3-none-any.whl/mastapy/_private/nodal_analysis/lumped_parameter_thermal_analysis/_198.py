"""FaceNode"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _212

_FACE_NODE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis", "FaceNode"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _185,
        _210,
    )

    Self = TypeVar("Self", bound="FaceNode")
    CastSelf = TypeVar("CastSelf", bound="FaceNode._Cast_FaceNode")


__docformat__ = "restructuredtext en"
__all__ = ("FaceNode",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceNode:
    """Special nested class for casting FaceNode to subclasses."""

    __parent__: "FaceNode"

    @property
    def simple_thermal_node_base(self: "CastSelf") -> "_212.SimpleThermalNodeBase":
        return self.__parent__._cast(_212.SimpleThermalNodeBase)

    @property
    def simple_node(self: "CastSelf") -> "_210.SimpleNode":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _210,
        )

        return self.__parent__._cast(_210.SimpleNode)

    @property
    def channel_face_thermal_node(self: "CastSelf") -> "_185.ChannelFaceThermalNode":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _185,
        )

        return self.__parent__._cast(_185.ChannelFaceThermalNode)

    @property
    def face_node(self: "CastSelf") -> "FaceNode":
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
class FaceNode(_212.SimpleThermalNodeBase):
    """FaceNode

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_NODE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FaceNode":
        """Cast to another type.

        Returns:
            _Cast_FaceNode
        """
        return _Cast_FaceNode(self)
