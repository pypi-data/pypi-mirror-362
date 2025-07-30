"""CADFace"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_2d import Vector2D

_CAD_FACE = python_net_import("SMT.MastaAPI.Geometry.TwoD", "CADFace")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="CADFace")
    CastSelf = TypeVar("CastSelf", bound="CADFace._Cast_CADFace")


__docformat__ = "restructuredtext en"
__all__ = ("CADFace",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CADFace:
    """Special nested class for casting CADFace to subclasses."""

    __parent__: "CADFace"

    @property
    def cad_face(self: "CastSelf") -> "CADFace":
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
class CADFace(_0.APIBase):
    """CADFace

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAD_FACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    @enforce_parameter_types
    def add_arc(
        self: "Self",
        circle_origin: "Vector2D",
        radius: "float",
        start_angle: "float",
        sweep_angle: "float",
    ) -> None:
        """Method does not return.

        Args:
            circle_origin (Vector2D)
            radius (float)
            start_angle (float)
            sweep_angle (float)
        """
        circle_origin = conversion.mp_to_pn_vector2d(circle_origin)
        radius = float(radius)
        start_angle = float(start_angle)
        sweep_angle = float(sweep_angle)
        pythonnet_method_call(
            self.wrapped,
            "AddArc",
            circle_origin,
            radius if radius else 0.0,
            start_angle if start_angle else 0.0,
            sweep_angle if sweep_angle else 0.0,
        )

    @exception_bridge
    @enforce_parameter_types
    def add_line(self: "Self", point_1: "Vector2D", point_2: "Vector2D") -> None:
        """Method does not return.

        Args:
            point_1 (Vector2D)
            point_2 (Vector2D)
        """
        point_1 = conversion.mp_to_pn_vector2d(point_1)
        point_2 = conversion.mp_to_pn_vector2d(point_2)
        pythonnet_method_call(self.wrapped, "AddLine", point_1, point_2)

    @exception_bridge
    @enforce_parameter_types
    def add_poly_line(self: "Self", points: "List[Vector2D]") -> None:
        """Method does not return.

        Args:
            points (List[Vector2D])
        """
        points = conversion.mp_to_pn_objects_in_list(points)
        pythonnet_method_call(self.wrapped, "AddPolyLine", points)

    @property
    def cast_to(self: "Self") -> "_Cast_CADFace":
        """Cast to another type.

        Returns:
            _Cast_CADFace
        """
        return _Cast_CADFace(self)
