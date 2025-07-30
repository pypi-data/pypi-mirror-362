"""FESubstructureNodeModeShape"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_FE_SUBSTRUCTURE_NODE_MODE_SHAPE = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FESubstructureNodeModeShape"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1748

    Self = TypeVar("Self", bound="FESubstructureNodeModeShape")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FESubstructureNodeModeShape._Cast_FESubstructureNodeModeShape",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructureNodeModeShape",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructureNodeModeShape:
    """Special nested class for casting FESubstructureNodeModeShape to subclasses."""

    __parent__: "FESubstructureNodeModeShape"

    @property
    def fe_substructure_node_mode_shape(
        self: "CastSelf",
    ) -> "FESubstructureNodeModeShape":
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
class FESubstructureNodeModeShape(_0.APIBase):
    """FESubstructureNodeModeShape

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE_NODE_MODE_SHAPE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def mode(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mode")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def mode_shape_component_coordinate_system(
        self: "Self",
    ) -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ModeShapeComponentCoordinateSystem"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mode_shape_fe_coordinate_system(
        self: "Self",
    ) -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModeShapeFECoordinateSystem")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mode_shape_global_cordinate_system(
        self: "Self",
    ) -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModeShapeGlobalCordinateSystem")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FESubstructureNodeModeShape":
        """Cast to another type.

        Returns:
            _Cast_FESubstructureNodeModeShape
        """
        return _Cast_FESubstructureNodeModeShape(self)
