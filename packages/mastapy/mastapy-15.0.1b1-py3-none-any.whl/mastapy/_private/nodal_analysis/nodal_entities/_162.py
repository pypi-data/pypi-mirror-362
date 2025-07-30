"""SplineContactNodalComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.nodal_analysis.nodal_entities import _154

_SPLINE_CONTACT_NODAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "SplineContactNodalComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _155

    Self = TypeVar("Self", bound="SplineContactNodalComponent")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SplineContactNodalComponent._Cast_SplineContactNodalComponent",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SplineContactNodalComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SplineContactNodalComponent:
    """Special nested class for casting SplineContactNodalComponent to subclasses."""

    __parent__: "SplineContactNodalComponent"

    @property
    def nodal_composite(self: "CastSelf") -> "_154.NodalComposite":
        return self.__parent__._cast(_154.NodalComposite)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def spline_contact_nodal_component(
        self: "CastSelf",
    ) -> "SplineContactNodalComponent":
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
class SplineContactNodalComponent(_154.NodalComposite):
    """SplineContactNodalComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPLINE_CONTACT_NODAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_teeth_in_contact(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethInContact")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_teeth_in_contact_left_flank(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethInContactLeftFlank")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_teeth_in_contact_right_flank(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethInContactRightFlank")

        if temp is None:
            return 0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SplineContactNodalComponent":
        """Cast to another type.

        Returns:
            _Cast_SplineContactNodalComponent
        """
        return _Cast_SplineContactNodalComponent(self)
