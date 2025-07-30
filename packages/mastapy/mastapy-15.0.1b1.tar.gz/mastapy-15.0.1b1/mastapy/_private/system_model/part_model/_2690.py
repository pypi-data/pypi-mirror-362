"""MeasurementComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2711

_MEASUREMENT_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MeasurementComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2693, _2698

    Self = TypeVar("Self", bound="MeasurementComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="MeasurementComponent._Cast_MeasurementComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeasurementComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeasurementComponent:
    """Special nested class for casting MeasurementComponent to subclasses."""

    __parent__: "MeasurementComponent"

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
    def measurement_component(self: "CastSelf") -> "MeasurementComponent":
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
class MeasurementComponent(_2711.VirtualComponent):
    """MeasurementComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MEASUREMENT_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MeasurementComponent":
        """Cast to another type.

        Returns:
            _Cast_MeasurementComponent
        """
        return _Cast_MeasurementComponent(self)
