"""NodeDetailsForFEModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D

_NODE_DETAILS_FOR_FE_MODEL = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "NodeDetailsForFEModel",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="NodeDetailsForFEModel")
    CastSelf = TypeVar(
        "CastSelf", bound="NodeDetailsForFEModel._Cast_NodeDetailsForFEModel"
    )


__docformat__ = "restructuredtext en"
__all__ = ("NodeDetailsForFEModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodeDetailsForFEModel:
    """Special nested class for casting NodeDetailsForFEModel to subclasses."""

    __parent__: "NodeDetailsForFEModel"

    @property
    def node_details_for_fe_model(self: "CastSelf") -> "NodeDetailsForFEModel":
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
class NodeDetailsForFEModel(_0.APIBase):
    """NodeDetailsForFEModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODE_DETAILS_FOR_FE_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def external_ids(self: "Self") -> "List[int]":
        """List[int]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExternalIDs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def node_positions(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodePositions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_NodeDetailsForFEModel":
        """Cast to another type.

        Returns:
            _Cast_NodeDetailsForFEModel
        """
        return _Cast_NodeDetailsForFEModel(self)
