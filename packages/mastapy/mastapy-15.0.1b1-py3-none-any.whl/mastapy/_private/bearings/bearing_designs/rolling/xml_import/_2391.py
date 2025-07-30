"""XMLVariableAssignment"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs.rolling.xml_import import _2387

_XML_VARIABLE_ASSIGNMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.XmlImport", "XMLVariableAssignment"
)

if TYPE_CHECKING:
    from typing import Any, Type

    Self = TypeVar("Self", bound="XMLVariableAssignment")
    CastSelf = TypeVar(
        "CastSelf", bound="XMLVariableAssignment._Cast_XMLVariableAssignment"
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("XMLVariableAssignment",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_XMLVariableAssignment:
    """Special nested class for casting XMLVariableAssignment to subclasses."""

    __parent__: "XMLVariableAssignment"

    @property
    def abstract_xml_variable_assignment(
        self: "CastSelf",
    ) -> "_2387.AbstractXmlVariableAssignment":
        return self.__parent__._cast(_2387.AbstractXmlVariableAssignment)

    @property
    def xml_variable_assignment(self: "CastSelf") -> "XMLVariableAssignment":
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
class XMLVariableAssignment(_2387.AbstractXmlVariableAssignment, Generic[T]):
    """XMLVariableAssignment

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _XML_VARIABLE_ASSIGNMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_XMLVariableAssignment":
        """Cast to another type.

        Returns:
            _Cast_XMLVariableAssignment
        """
        return _Cast_XMLVariableAssignment(self)
