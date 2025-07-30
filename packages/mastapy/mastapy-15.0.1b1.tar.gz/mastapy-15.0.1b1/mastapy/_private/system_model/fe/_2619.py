"""IndependentMASTACreatedConstrainedNodes"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D

_INDEPENDENT_MASTA_CREATED_CONSTRAINED_NODES = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "IndependentMASTACreatedConstrainedNodes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe import _2618, _2621

    Self = TypeVar("Self", bound="IndependentMASTACreatedConstrainedNodes")
    CastSelf = TypeVar(
        "CastSelf",
        bound="IndependentMASTACreatedConstrainedNodes._Cast_IndependentMASTACreatedConstrainedNodes",
    )


__docformat__ = "restructuredtext en"
__all__ = ("IndependentMASTACreatedConstrainedNodes",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IndependentMASTACreatedConstrainedNodes:
    """Special nested class for casting IndependentMASTACreatedConstrainedNodes to subclasses."""

    __parent__: "IndependentMASTACreatedConstrainedNodes"

    @property
    def independent_masta_created_condensation_node(
        self: "CastSelf",
    ) -> "_2618.IndependentMASTACreatedCondensationNode":
        from mastapy._private.system_model.fe import _2618

        return self.__parent__._cast(_2618.IndependentMASTACreatedCondensationNode)

    @property
    def independent_masta_created_rigidly_connected_node_group(
        self: "CastSelf",
    ) -> "_2621.IndependentMASTACreatedRigidlyConnectedNodeGroup":
        from mastapy._private.system_model.fe import _2621

        return self.__parent__._cast(
            _2621.IndependentMASTACreatedRigidlyConnectedNodeGroup
        )

    @property
    def independent_masta_created_constrained_nodes(
        self: "CastSelf",
    ) -> "IndependentMASTACreatedConstrainedNodes":
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
class IndependentMASTACreatedConstrainedNodes(_0.APIBase):
    """IndependentMASTACreatedConstrainedNodes

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INDEPENDENT_MASTA_CREATED_CONSTRAINED_NODES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def node_position(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "NodePosition")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @node_position.setter
    @exception_bridge
    @enforce_parameter_types
    def node_position(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "NodePosition", value)

    @exception_bridge
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @property
    def cast_to(self: "Self") -> "_Cast_IndependentMASTACreatedConstrainedNodes":
        """Cast to another type.

        Returns:
            _Cast_IndependentMASTACreatedConstrainedNodes
        """
        return _Cast_IndependentMASTACreatedConstrainedNodes(self)
