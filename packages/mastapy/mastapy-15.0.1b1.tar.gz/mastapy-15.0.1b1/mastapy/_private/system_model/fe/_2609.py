"""FESubstructureNodeModeShapes"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_FE_SUBSTRUCTURE_NODE_MODE_SHAPES = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FESubstructureNodeModeShapes"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1683
    from mastapy._private.system_model.fe import _2607, _2608

    Self = TypeVar("Self", bound="FESubstructureNodeModeShapes")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FESubstructureNodeModeShapes._Cast_FESubstructureNodeModeShapes",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructureNodeModeShapes",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructureNodeModeShapes:
    """Special nested class for casting FESubstructureNodeModeShapes to subclasses."""

    __parent__: "FESubstructureNodeModeShapes"

    @property
    def fe_substructure_node_mode_shapes(
        self: "CastSelf",
    ) -> "FESubstructureNodeModeShapes":
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
class FESubstructureNodeModeShapes(_0.APIBase):
    """FESubstructureNodeModeShapes

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE_NODE_MODE_SHAPES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def condensation_node(self: "Self") -> "_2607.FESubstructureNode":
        """mastapy.system_model.fe.FESubstructureNode

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CondensationNode")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connected_component_local_coordinate_system(
        self: "Self",
    ) -> "_1683.CoordinateSystem3D":
        """mastapy.math_utility.CoordinateSystem3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConnectedComponentLocalCoordinateSystem"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mode_shapes_at_condensation_node(
        self: "Self",
    ) -> "List[_2608.FESubstructureNodeModeShape]":
        """List[mastapy.system_model.fe.FESubstructureNodeModeShape]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModeShapesAtCondensationNode")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FESubstructureNodeModeShapes":
        """Cast to another type.

        Returns:
            _Cast_FESubstructureNodeModeShapes
        """
        return _Cast_FESubstructureNodeModeShapes(self)
