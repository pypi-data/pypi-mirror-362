"""CylindricalGearTriangularEndModification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.micro_geometry import _670

_CYLINDRICAL_GEAR_TRIANGULAR_END_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearTriangularEndModification",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1224

    Self = TypeVar("Self", bound="CylindricalGearTriangularEndModification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearTriangularEndModification._Cast_CylindricalGearTriangularEndModification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearTriangularEndModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearTriangularEndModification:
    """Special nested class for casting CylindricalGearTriangularEndModification to subclasses."""

    __parent__: "CylindricalGearTriangularEndModification"

    @property
    def modification(self: "CastSelf") -> "_670.Modification":
        return self.__parent__._cast(_670.Modification)

    @property
    def cylindrical_gear_triangular_end_modification(
        self: "CastSelf",
    ) -> "CylindricalGearTriangularEndModification":
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
class CylindricalGearTriangularEndModification(_670.Modification):
    """CylindricalGearTriangularEndModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_TRIANGULAR_END_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def root_left(
        self: "Self",
    ) -> "_1224.CylindricalGearTriangularEndModificationAtOrientation":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearTriangularEndModificationAtOrientation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootLeft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def root_right(
        self: "Self",
    ) -> "_1224.CylindricalGearTriangularEndModificationAtOrientation":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearTriangularEndModificationAtOrientation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootRight")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def tip_left(
        self: "Self",
    ) -> "_1224.CylindricalGearTriangularEndModificationAtOrientation":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearTriangularEndModificationAtOrientation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipLeft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def tip_right(
        self: "Self",
    ) -> "_1224.CylindricalGearTriangularEndModificationAtOrientation":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearTriangularEndModificationAtOrientation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipRight")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def relief_of(self: "Self", face_width: "float", roll_distance: "float") -> "float":
        """float

        Args:
            face_width (float)
            roll_distance (float)
        """
        face_width = float(face_width)
        roll_distance = float(roll_distance)
        method_result = pythonnet_method_call(
            self.wrapped,
            "ReliefOf",
            face_width if face_width else 0.0,
            roll_distance if roll_distance else 0.0,
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearTriangularEndModification":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearTriangularEndModification
        """
        return _Cast_CylindricalGearTriangularEndModification(self)
