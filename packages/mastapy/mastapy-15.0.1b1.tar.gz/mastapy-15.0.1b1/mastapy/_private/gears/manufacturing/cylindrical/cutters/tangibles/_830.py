"""CylindricalGearShaverTangible"""

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

_CYLINDRICAL_GEAR_SHAVER_TANGIBLE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters.Tangibles",
    "CylindricalGearShaverTangible",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _818

    Self = TypeVar("Self", bound="CylindricalGearShaverTangible")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearShaverTangible._Cast_CylindricalGearShaverTangible",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearShaverTangible",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearShaverTangible:
    """Special nested class for casting CylindricalGearShaverTangible to subclasses."""

    __parent__: "CylindricalGearShaverTangible"

    @property
    def cutter_shape_definition(self: "CastSelf") -> "_826.CutterShapeDefinition":
        return self.__parent__._cast(_826.CutterShapeDefinition)

    @property
    def cylindrical_gear_shaver_tangible(
        self: "CastSelf",
    ) -> "CylindricalGearShaverTangible":
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
class CylindricalGearShaverTangible(_826.CutterShapeDefinition):
    """CylindricalGearShaverTangible

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SHAVER_TANGIBLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def design(self: "Self") -> "_818.CylindricalGearShaver":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaver

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Design")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearShaverTangible":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearShaverTangible
        """
        return _Cast_CylindricalGearShaverTangible(self)
