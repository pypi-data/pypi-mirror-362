"""ElementScalarState"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.states import _126

_ELEMENT_SCALAR_STATE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.States", "ElementScalarState"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.states import _127

    Self = TypeVar("Self", bound="ElementScalarState")
    CastSelf = TypeVar("CastSelf", bound="ElementScalarState._Cast_ElementScalarState")


__docformat__ = "restructuredtext en"
__all__ = ("ElementScalarState",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementScalarState:
    """Special nested class for casting ElementScalarState to subclasses."""

    __parent__: "ElementScalarState"

    @property
    def element_vector_state(self: "CastSelf") -> "_126.ElementVectorState":
        return self.__parent__._cast(_126.ElementVectorState)

    @property
    def entity_vector_state(self: "CastSelf") -> "_127.EntityVectorState":
        from mastapy._private.nodal_analysis.states import _127

        return self.__parent__._cast(_127.EntityVectorState)

    @property
    def element_scalar_state(self: "CastSelf") -> "ElementScalarState":
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
class ElementScalarState(_126.ElementVectorState):
    """ElementScalarState

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_SCALAR_STATE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElementScalarState":
        """Cast to another type.

        Returns:
            _Cast_ElementScalarState
        """
        return _Cast_ElementScalarState(self)
