"""ElementPropertiesInterface"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import _294

_ELEMENT_PROPERTIES_INTERFACE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ElementPropertiesInterface",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElementPropertiesInterface")
    CastSelf = TypeVar(
        "CastSelf", bound="ElementPropertiesInterface._Cast_ElementPropertiesInterface"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesInterface",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementPropertiesInterface:
    """Special nested class for casting ElementPropertiesInterface to subclasses."""

    __parent__: "ElementPropertiesInterface"

    @property
    def element_properties_base(self: "CastSelf") -> "_294.ElementPropertiesBase":
        return self.__parent__._cast(_294.ElementPropertiesBase)

    @property
    def element_properties_interface(self: "CastSelf") -> "ElementPropertiesInterface":
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
class ElementPropertiesInterface(_294.ElementPropertiesBase):
    """ElementPropertiesInterface

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_PROPERTIES_INTERFACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElementPropertiesInterface":
        """Cast to another type.

        Returns:
            _Cast_ElementPropertiesInterface
        """
        return _Cast_ElementPropertiesInterface(self)
