"""ContactPairWithSelection"""

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

_CONTACT_PAIR_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "ContactPairWithSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _289,
    )

    Self = TypeVar("Self", bound="ContactPairWithSelection")
    CastSelf = TypeVar(
        "CastSelf", bound="ContactPairWithSelection._Cast_ContactPairWithSelection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ContactPairWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ContactPairWithSelection:
    """Special nested class for casting ContactPairWithSelection to subclasses."""

    __parent__: "ContactPairWithSelection"

    @property
    def contact_pair_with_selection(self: "CastSelf") -> "ContactPairWithSelection":
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
class ContactPairWithSelection(_0.APIBase):
    """ContactPairWithSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONTACT_PAIR_WITH_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_pair(self: "Self") -> "_289.ContactPairReporting":
        """mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ContactPairReporting

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPair")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def select_constrained_surface(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectConstrainedSurface")

    @exception_bridge
    def select_contacting_constrained_surface(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectContactingConstrainedSurface")

    @exception_bridge
    def select_contacting_reference_surface(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectContactingReferenceSurface")

    @exception_bridge
    def select_reference_surface(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectReferenceSurface")

    @property
    def cast_to(self: "Self") -> "_Cast_ContactPairWithSelection":
        """Cast to another type.

        Returns:
            _Cast_ContactPairWithSelection
        """
        return _Cast_ContactPairWithSelection(self)
