"""CylindricalGearWormGrinderShape"""

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
from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _833

_CYLINDRICAL_GEAR_WORM_GRINDER_SHAPE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters.Tangibles",
    "CylindricalGearWormGrinderShape",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _811
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _826

    Self = TypeVar("Self", bound="CylindricalGearWormGrinderShape")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearWormGrinderShape._Cast_CylindricalGearWormGrinderShape",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearWormGrinderShape",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearWormGrinderShape:
    """Special nested class for casting CylindricalGearWormGrinderShape to subclasses."""

    __parent__: "CylindricalGearWormGrinderShape"

    @property
    def rack_shape(self: "CastSelf") -> "_833.RackShape":
        return self.__parent__._cast(_833.RackShape)

    @property
    def cutter_shape_definition(self: "CastSelf") -> "_826.CutterShapeDefinition":
        from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
            _826,
        )

        return self.__parent__._cast(_826.CutterShapeDefinition)

    @property
    def cylindrical_gear_worm_grinder_shape(
        self: "CastSelf",
    ) -> "CylindricalGearWormGrinderShape":
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
class CylindricalGearWormGrinderShape(_833.RackShape):
    """CylindricalGearWormGrinderShape

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_WORM_GRINDER_SHAPE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def design(self: "Self") -> "_811.CylindricalGearGrindingWorm":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearGrindingWorm

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Design")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearWormGrinderShape":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearWormGrinderShape
        """
        return _Cast_CylindricalGearWormGrinderShape(self)
