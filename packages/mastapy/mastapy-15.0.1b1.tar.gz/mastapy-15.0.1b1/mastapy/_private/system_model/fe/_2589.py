"""CoordinateSystemWithSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)

_COORDINATE_SYSTEM_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "CoordinateSystemWithSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _290,
    )

    Self = TypeVar("Self", bound="CoordinateSystemWithSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoordinateSystemWithSelection._Cast_CoordinateSystemWithSelection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoordinateSystemWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoordinateSystemWithSelection:
    """Special nested class for casting CoordinateSystemWithSelection to subclasses."""

    __parent__: "CoordinateSystemWithSelection"

    @property
    def coordinate_system_with_selection(
        self: "CastSelf",
    ) -> "CoordinateSystemWithSelection":
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
class CoordinateSystemWithSelection(_0.APIBase):
    """CoordinateSystemWithSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COORDINATE_SYSTEM_WITH_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def coordinate_system(self: "Self") -> "_290.CoordinateSystemReporting":
        """mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.CoordinateSystemReporting

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoordinateSystem")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def select_nodes_using_this_for_material_orientation(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "SelectNodesUsingThisForMaterialOrientation"
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CoordinateSystemWithSelection":
        """Cast to another type.

        Returns:
            _Cast_CoordinateSystemWithSelection
        """
        return _Cast_CoordinateSystemWithSelection(self)
