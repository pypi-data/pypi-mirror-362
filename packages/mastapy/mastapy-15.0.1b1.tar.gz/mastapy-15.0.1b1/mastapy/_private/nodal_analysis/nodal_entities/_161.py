"""SimpleBar"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _170

_SIMPLE_BAR = python_net_import("SMT.MastaAPI.NodalAnalysis.NodalEntities", "SimpleBar")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _141, _154, _155

    Self = TypeVar("Self", bound="SimpleBar")
    CastSelf = TypeVar("CastSelf", bound="SimpleBar._Cast_SimpleBar")


__docformat__ = "restructuredtext en"
__all__ = ("SimpleBar",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SimpleBar:
    """Special nested class for casting SimpleBar to subclasses."""

    __parent__: "SimpleBar"

    @property
    def two_body_connection_nodal_component(
        self: "CastSelf",
    ) -> "_170.TwoBodyConnectionNodalComponent":
        return self.__parent__._cast(_170.TwoBodyConnectionNodalComponent)

    @property
    def component_nodal_composite_base(
        self: "CastSelf",
    ) -> "_141.ComponentNodalCompositeBase":
        from mastapy._private.nodal_analysis.nodal_entities import _141

        return self.__parent__._cast(_141.ComponentNodalCompositeBase)

    @property
    def nodal_composite(self: "CastSelf") -> "_154.NodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _154

        return self.__parent__._cast(_154.NodalComposite)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def simple_bar(self: "CastSelf") -> "SimpleBar":
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
class SimpleBar(_170.TwoBodyConnectionNodalComponent):
    """SimpleBar

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SIMPLE_BAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SimpleBar":
        """Cast to another type.

        Returns:
            _Cast_SimpleBar
        """
        return _Cast_SimpleBar(self)
