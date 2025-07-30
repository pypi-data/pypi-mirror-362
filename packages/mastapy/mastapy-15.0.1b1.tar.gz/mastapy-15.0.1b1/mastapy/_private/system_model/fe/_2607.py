"""FESubstructureNode"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.nodal_analysis import _70

_FE_SUBSTRUCTURE_NODE = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FESubstructureNode"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1748

    Self = TypeVar("Self", bound="FESubstructureNode")
    CastSelf = TypeVar("CastSelf", bound="FESubstructureNode._Cast_FESubstructureNode")


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructureNode",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructureNode:
    """Special nested class for casting FESubstructureNode to subclasses."""

    __parent__: "FESubstructureNode"

    @property
    def fe_stiffness_node(self: "CastSelf") -> "_70.FEStiffnessNode":
        return self.__parent__._cast(_70.FEStiffnessNode)

    @property
    def fe_substructure_node(self: "CastSelf") -> "FESubstructureNode":
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
class FESubstructureNode(_70.FEStiffnessNode):
    """FESubstructureNode

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE_NODE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def external_id(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ExternalID")

        if temp is None:
            return 0

        return temp

    @external_id.setter
    @exception_bridge
    @enforce_parameter_types
    def external_id(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ExternalID", int(value) if value is not None else 0
        )

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
    def override_default_name(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideDefaultName")

        if temp is None:
            return False

        return temp

    @override_default_name.setter
    @exception_bridge
    @enforce_parameter_types
    def override_default_name(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDefaultName",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def force_due_to_gravity_in_local_coordinate_system(
        self: "Self",
    ) -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ForceDueToGravityInLocalCoordinateSystem"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force_due_to_gravity_in_local_coordinate_system_with_gravity_in_fex_direction(
        self: "Self",
    ) -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ForceDueToGravityInLocalCoordinateSystemWithGravityInFEXDirection",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force_due_to_gravity_in_local_coordinate_system_with_gravity_in_fey_direction(
        self: "Self",
    ) -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ForceDueToGravityInLocalCoordinateSystemWithGravityInFEYDirection",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force_due_to_gravity_in_local_coordinate_system_with_gravity_in_fez_direction(
        self: "Self",
    ) -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ForceDueToGravityInLocalCoordinateSystemWithGravityInFEZDirection",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def position_in_world_coordinate_system(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PositionInWorldCoordinateSystem")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FESubstructureNode":
        """Cast to another type.

        Returns:
            _Cast_FESubstructureNode
        """
        return _Cast_FESubstructureNode(self)
