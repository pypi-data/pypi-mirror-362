"""CADFaceGroup"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CAD_FACE_GROUP = python_net_import("SMT.MastaAPI.Geometry.TwoD", "CADFaceGroup")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry.two_d import _399

    Self = TypeVar("Self", bound="CADFaceGroup")
    CastSelf = TypeVar("CastSelf", bound="CADFaceGroup._Cast_CADFaceGroup")


__docformat__ = "restructuredtext en"
__all__ = ("CADFaceGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CADFaceGroup:
    """Special nested class for casting CADFaceGroup to subclasses."""

    __parent__: "CADFaceGroup"

    @property
    def cad_face_group(self: "CastSelf") -> "CADFaceGroup":
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
class CADFaceGroup(_0.APIBase):
    """CADFaceGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAD_FACE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    @enforce_parameter_types
    def add_face(self: "Self", moniker: "str") -> "_399.CADFace":
        """mastapy.geometry.two_d.CADFace

        Args:
            moniker (str)
        """
        moniker = str(moniker)
        method_result = pythonnet_method_call(
            self.wrapped, "AddFace", moniker if moniker else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CADFaceGroup":
        """Cast to another type.

        Returns:
            _Cast_CADFaceGroup
        """
        return _Cast_CADFaceGroup(self)
