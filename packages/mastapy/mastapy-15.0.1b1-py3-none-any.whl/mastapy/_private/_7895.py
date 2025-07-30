"""MarshalByRefObjectPermanent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)

_MARSHAL_BY_REF_OBJECT_PERMANENT = python_net_import(
    "SMT.MastaAPIUtility", "MarshalByRefObjectPermanent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MarshalByRefObjectPermanent")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MarshalByRefObjectPermanent._Cast_MarshalByRefObjectPermanent",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MarshalByRefObjectPermanent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MarshalByRefObjectPermanent:
    """Special nested class for casting MarshalByRefObjectPermanent to subclasses."""

    __parent__: "MarshalByRefObjectPermanent"

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "MarshalByRefObjectPermanent":
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
class MarshalByRefObjectPermanent:
    """MarshalByRefObjectPermanent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MARSHAL_BY_REF_OBJECT_PERMANENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    def initialize_lifetime_service(self: "Self") -> "object":
        """object"""
        method_result = pythonnet_method_call(self.wrapped, "InitializeLifetimeService")
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_MarshalByRefObjectPermanent":
        """Cast to another type.

        Returns:
            _Cast_MarshalByRefObjectPermanent
        """
        return _Cast_MarshalByRefObjectPermanent(self)
