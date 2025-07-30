"""SMTBitmap"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _7895
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)

_SMT_BITMAP = python_net_import("SMT.MastaAPIUtility.Scripting", "SMTBitmap")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SMTBitmap")
    CastSelf = TypeVar("CastSelf", bound="SMTBitmap._Cast_SMTBitmap")


__docformat__ = "restructuredtext en"
__all__ = ("SMTBitmap",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SMTBitmap:
    """Special nested class for casting SMTBitmap to subclasses."""

    __parent__: "SMTBitmap"

    @property
    def smt_bitmap(self: "CastSelf") -> "SMTBitmap":
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
class SMTBitmap(_7895.MarshalByRefObjectPermanent):
    """SMTBitmap

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SMT_BITMAP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    def to_image(self: "Self") -> "Image":
        """Image"""
        return conversion.pn_to_mp_image(pythonnet_method_call(self.wrapped, "ToImage"))

    @exception_bridge
    def to_bytes(self: "Self") -> "bytes":
        """bytes"""
        return conversion.pn_to_mp_bytes(pythonnet_method_call(self.wrapped, "ToBytes"))

    @property
    def cast_to(self: "Self") -> "_Cast_SMTBitmap":
        """Cast to another type.

        Returns:
            _Cast_SMTBitmap
        """
        return _Cast_SMTBitmap(self)
