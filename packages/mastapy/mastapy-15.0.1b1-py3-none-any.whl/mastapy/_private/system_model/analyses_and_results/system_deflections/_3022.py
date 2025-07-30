"""MeshSeparationsAtFaceWidth"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_MESH_SEPARATIONS_AT_FACE_WIDTH = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "MeshSeparationsAtFaceWidth",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MeshSeparationsAtFaceWidth")
    CastSelf = TypeVar(
        "CastSelf", bound="MeshSeparationsAtFaceWidth._Cast_MeshSeparationsAtFaceWidth"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeshSeparationsAtFaceWidth",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshSeparationsAtFaceWidth:
    """Special nested class for casting MeshSeparationsAtFaceWidth to subclasses."""

    __parent__: "MeshSeparationsAtFaceWidth"

    @property
    def mesh_separations_at_face_width(
        self: "CastSelf",
    ) -> "MeshSeparationsAtFaceWidth":
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
class MeshSeparationsAtFaceWidth(_0.APIBase):
    """MeshSeparationsAtFaceWidth

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESH_SEPARATIONS_AT_FACE_WIDTH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face_width_location(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidthLocation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def left_flank_separation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankSeparation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def right_flank_separation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankSeparation")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_MeshSeparationsAtFaceWidth":
        """Cast to another type.

        Returns:
            _Cast_MeshSeparationsAtFaceWidth
        """
        return _Cast_MeshSeparationsAtFaceWidth(self)
