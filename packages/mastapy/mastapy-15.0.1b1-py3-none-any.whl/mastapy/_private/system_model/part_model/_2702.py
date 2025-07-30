"""PointLoad"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_2d import Vector2D
from mastapy._private.system_model.part_model import _2711

_POINT_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PointLoad")

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2693, _2698

    Self = TypeVar("Self", bound="PointLoad")
    CastSelf = TypeVar("CastSelf", bound="PointLoad._Cast_PointLoad")


__docformat__ = "restructuredtext en"
__all__ = ("PointLoad",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PointLoad:
    """Special nested class for casting PointLoad to subclasses."""

    __parent__: "PointLoad"

    @property
    def virtual_component(self: "CastSelf") -> "_2711.VirtualComponent":
        return self.__parent__._cast(_2711.VirtualComponent)

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
        from mastapy._private.system_model.part_model import _2693

        return self.__parent__._cast(_2693.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        from mastapy._private.system_model.part_model import _2670

        return self.__parent__._cast(_2670.Component)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def point_load(self: "CastSelf") -> "PointLoad":
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
class PointLoad(_2711.VirtualComponent):
    """PointLoad

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POINT_LOAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def drawing_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DrawingRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @drawing_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def drawing_radius(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DrawingRadius", value)

    @property
    @exception_bridge
    def offset(self: "Self") -> "Vector2D":
        """Vector2D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def set_offset(self: "Self", radius: "float", angle: "float") -> None:
        """Method does not return.

        Args:
            radius (float)
            angle (float)
        """
        radius = float(radius)
        angle = float(angle)
        pythonnet_method_call(
            self.wrapped,
            "SetOffset",
            radius if radius else 0.0,
            angle if angle else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PointLoad":
        """Cast to another type.

        Returns:
            _Cast_PointLoad
        """
        return _Cast_PointLoad(self)
