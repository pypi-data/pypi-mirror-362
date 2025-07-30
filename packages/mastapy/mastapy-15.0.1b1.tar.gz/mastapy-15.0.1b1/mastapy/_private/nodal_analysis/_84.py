"""NodalMatrixEditorWrapperColumn"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_NODAL_MATRIX_EDITOR_WRAPPER_COLUMN = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "NodalMatrixEditorWrapperColumn"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NodalMatrixEditorWrapperColumn")
    CastSelf = TypeVar(
        "CastSelf",
        bound="NodalMatrixEditorWrapperColumn._Cast_NodalMatrixEditorWrapperColumn",
    )


__docformat__ = "restructuredtext en"
__all__ = ("NodalMatrixEditorWrapperColumn",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalMatrixEditorWrapperColumn:
    """Special nested class for casting NodalMatrixEditorWrapperColumn to subclasses."""

    __parent__: "NodalMatrixEditorWrapperColumn"

    @property
    def nodal_matrix_editor_wrapper_column(
        self: "CastSelf",
    ) -> "NodalMatrixEditorWrapperColumn":
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
class NodalMatrixEditorWrapperColumn(_0.APIBase):
    """NodalMatrixEditorWrapperColumn

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_MATRIX_EDITOR_WRAPPER_COLUMN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def node_1_theta_x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node1ThetaX")

        if temp is None:
            return 0.0

        return temp

    @node_1_theta_x.setter
    @exception_bridge
    @enforce_parameter_types
    def node_1_theta_x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node1ThetaX", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def node_1_theta_y(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node1ThetaY")

        if temp is None:
            return 0.0

        return temp

    @node_1_theta_y.setter
    @exception_bridge
    @enforce_parameter_types
    def node_1_theta_y(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node1ThetaY", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def node_1_theta_z(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node1ThetaZ")

        if temp is None:
            return 0.0

        return temp

    @node_1_theta_z.setter
    @exception_bridge
    @enforce_parameter_types
    def node_1_theta_z(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node1ThetaZ", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def node_1x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node1X")

        if temp is None:
            return 0.0

        return temp

    @node_1x.setter
    @exception_bridge
    @enforce_parameter_types
    def node_1x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node1X", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def node_1y(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node1Y")

        if temp is None:
            return 0.0

        return temp

    @node_1y.setter
    @exception_bridge
    @enforce_parameter_types
    def node_1y(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node1Y", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def node_1z(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node1Z")

        if temp is None:
            return 0.0

        return temp

    @node_1z.setter
    @exception_bridge
    @enforce_parameter_types
    def node_1z(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node1Z", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def node_2_theta_x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node2ThetaX")

        if temp is None:
            return 0.0

        return temp

    @node_2_theta_x.setter
    @exception_bridge
    @enforce_parameter_types
    def node_2_theta_x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node2ThetaX", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def node_2_theta_y(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node2ThetaY")

        if temp is None:
            return 0.0

        return temp

    @node_2_theta_y.setter
    @exception_bridge
    @enforce_parameter_types
    def node_2_theta_y(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node2ThetaY", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def node_2_theta_z(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node2ThetaZ")

        if temp is None:
            return 0.0

        return temp

    @node_2_theta_z.setter
    @exception_bridge
    @enforce_parameter_types
    def node_2_theta_z(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node2ThetaZ", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def node_2x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node2X")

        if temp is None:
            return 0.0

        return temp

    @node_2x.setter
    @exception_bridge
    @enforce_parameter_types
    def node_2x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node2X", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def node_2y(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node2Y")

        if temp is None:
            return 0.0

        return temp

    @node_2y.setter
    @exception_bridge
    @enforce_parameter_types
    def node_2y(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node2Y", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def node_2z(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Node2Z")

        if temp is None:
            return 0.0

        return temp

    @node_2z.setter
    @exception_bridge
    @enforce_parameter_types
    def node_2z(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Node2Z", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_NodalMatrixEditorWrapperColumn":
        """Cast to another type.

        Returns:
            _Cast_NodalMatrixEditorWrapperColumn
        """
        return _Cast_NodalMatrixEditorWrapperColumn(self)
