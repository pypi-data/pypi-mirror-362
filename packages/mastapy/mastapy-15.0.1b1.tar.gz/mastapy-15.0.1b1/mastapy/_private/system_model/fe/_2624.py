"""MaterialPropertiesWithSelection"""

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

_MATERIAL_PROPERTIES_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "MaterialPropertiesWithSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _303,
    )

    Self = TypeVar("Self", bound="MaterialPropertiesWithSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MaterialPropertiesWithSelection._Cast_MaterialPropertiesWithSelection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MaterialPropertiesWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MaterialPropertiesWithSelection:
    """Special nested class for casting MaterialPropertiesWithSelection to subclasses."""

    __parent__: "MaterialPropertiesWithSelection"

    @property
    def material_properties_with_selection(
        self: "CastSelf",
    ) -> "MaterialPropertiesWithSelection":
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
class MaterialPropertiesWithSelection(_0.APIBase):
    """MaterialPropertiesWithSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MATERIAL_PROPERTIES_WITH_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def material_properties(self: "Self") -> "_303.MaterialPropertiesReporting":
        """mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.MaterialPropertiesReporting

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def select_nodes(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectNodes")

    @property
    def cast_to(self: "Self") -> "_Cast_MaterialPropertiesWithSelection":
        """Cast to another type.

        Returns:
            _Cast_MaterialPropertiesWithSelection
        """
        return _Cast_MaterialPropertiesWithSelection(self)
