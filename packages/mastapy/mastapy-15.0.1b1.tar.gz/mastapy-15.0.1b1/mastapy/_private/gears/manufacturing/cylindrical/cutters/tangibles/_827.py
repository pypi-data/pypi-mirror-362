"""CylindricalGearFormedWheelGrinderTangible"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _826

_CYLINDRICAL_GEAR_FORMED_WHEEL_GRINDER_TANGIBLE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters.Tangibles",
    "CylindricalGearFormedWheelGrinderTangible",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _810

    Self = TypeVar("Self", bound="CylindricalGearFormedWheelGrinderTangible")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearFormedWheelGrinderTangible._Cast_CylindricalGearFormedWheelGrinderTangible",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFormedWheelGrinderTangible",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFormedWheelGrinderTangible:
    """Special nested class for casting CylindricalGearFormedWheelGrinderTangible to subclasses."""

    __parent__: "CylindricalGearFormedWheelGrinderTangible"

    @property
    def cutter_shape_definition(self: "CastSelf") -> "_826.CutterShapeDefinition":
        return self.__parent__._cast(_826.CutterShapeDefinition)

    @property
    def cylindrical_gear_formed_wheel_grinder_tangible(
        self: "CastSelf",
    ) -> "CylindricalGearFormedWheelGrinderTangible":
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
class CylindricalGearFormedWheelGrinderTangible(_826.CutterShapeDefinition):
    """CylindricalGearFormedWheelGrinderTangible

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FORMED_WHEEL_GRINDER_TANGIBLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def design(self: "Self") -> "_810.CylindricalGearFormGrindingWheel":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearFormGrindingWheel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Design")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFormedWheelGrinderTangible":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFormedWheelGrinderTangible
        """
        return _Cast_CylindricalGearFormedWheelGrinderTangible(self)
