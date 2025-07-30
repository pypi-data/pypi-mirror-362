"""ElementPropertiesWithSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

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

_ELEMENT_PROPERTIES_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "ElementPropertiesWithSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _294,
    )

    Self = TypeVar("Self", bound="ElementPropertiesWithSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElementPropertiesWithSelection._Cast_ElementPropertiesWithSelection",
    )

T = TypeVar("T", bound="_294.ElementPropertiesBase")

__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementPropertiesWithSelection:
    """Special nested class for casting ElementPropertiesWithSelection to subclasses."""

    __parent__: "ElementPropertiesWithSelection"

    @property
    def element_properties_with_selection(
        self: "CastSelf",
    ) -> "ElementPropertiesWithSelection":
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
class ElementPropertiesWithSelection(_0.APIBase, Generic[T]):
    """ElementPropertiesWithSelection

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _ELEMENT_PROPERTIES_WITH_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def element_properties(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def select_nodes(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectNodes")

    @property
    def cast_to(self: "Self") -> "_Cast_ElementPropertiesWithSelection":
        """Cast to another type.

        Returns:
            _Cast_ElementPropertiesWithSelection
        """
        return _Cast_ElementPropertiesWithSelection(self)
