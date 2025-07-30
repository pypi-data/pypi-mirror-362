"""ShaftDeflectionDrawingNodeItem"""

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

_SHAFT_DEFLECTION_DRAWING_NODE_ITEM = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "ShaftDeflectionDrawingNodeItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1744
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3046,
    )

    Self = TypeVar("Self", bound="ShaftDeflectionDrawingNodeItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftDeflectionDrawingNodeItem._Cast_ShaftDeflectionDrawingNodeItem",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftDeflectionDrawingNodeItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftDeflectionDrawingNodeItem:
    """Special nested class for casting ShaftDeflectionDrawingNodeItem to subclasses."""

    __parent__: "ShaftDeflectionDrawingNodeItem"

    @property
    def shaft_deflection_drawing_node_item(
        self: "CastSelf",
    ) -> "ShaftDeflectionDrawingNodeItem":
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
class ShaftDeflectionDrawingNodeItem(_0.APIBase):
    """ShaftDeflectionDrawingNodeItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_DEFLECTION_DRAWING_NODE_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_deflection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialDeflection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def offset(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_deflection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialDeflection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def node_detail(self: "Self") -> "_1744.ForceAndDisplacementResults":
        """mastapy.math_utility.measured_vectors.ForceAndDisplacementResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def section_to_the_left_side(self: "Self") -> "_3046.ShaftSectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SectionToTheLeftSide")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def section_to_the_right_side(self: "Self") -> "_3046.ShaftSectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SectionToTheRightSide")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftDeflectionDrawingNodeItem":
        """Cast to another type.

        Returns:
            _Cast_ShaftDeflectionDrawingNodeItem
        """
        return _Cast_ShaftDeflectionDrawingNodeItem(self)
