"""AlignmentUsingAxialNodePositions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility import _1675

_ALIGNMENT_USING_AXIAL_NODE_POSITIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "AlignmentUsingAxialNodePositions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AlignmentUsingAxialNodePositions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AlignmentUsingAxialNodePositions._Cast_AlignmentUsingAxialNodePositions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AlignmentUsingAxialNodePositions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AlignmentUsingAxialNodePositions:
    """Special nested class for casting AlignmentUsingAxialNodePositions to subclasses."""

    __parent__: "AlignmentUsingAxialNodePositions"

    @property
    def alignment_using_axial_node_positions(
        self: "CastSelf",
    ) -> "AlignmentUsingAxialNodePositions":
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
class AlignmentUsingAxialNodePositions(_0.APIBase):
    """AlignmentUsingAxialNodePositions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ALIGNMENT_USING_AXIAL_NODE_POSITIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fe_axis_for_angle_alignment(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis":
        """EnumWithSelectedValue[mastapy.math_utility.AlignmentAxis]"""
        temp = pythonnet_property_get(self.wrapped, "FEAxisForAngleAlignment")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @fe_axis_for_angle_alignment.setter
    @exception_bridge
    @enforce_parameter_types
    def fe_axis_for_angle_alignment(self: "Self", value: "_1675.AlignmentAxis") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "FEAxisForAngleAlignment", value)

    @property
    @exception_bridge
    def rotation_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAngle")

        if temp is None:
            return 0.0

        return temp

    @rotation_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def rotation_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RotationAngle", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AlignmentUsingAxialNodePositions":
        """Cast to another type.

        Returns:
            _Cast_AlignmentUsingAxialNodePositions
        """
        return _Cast_AlignmentUsingAxialNodePositions(self)
