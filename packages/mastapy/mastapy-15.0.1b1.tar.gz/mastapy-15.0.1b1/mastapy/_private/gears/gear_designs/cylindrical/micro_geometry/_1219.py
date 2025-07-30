"""CylindricalGearProfileModificationAtFaceWidthPosition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1218

_CYLINDRICAL_GEAR_PROFILE_MODIFICATION_AT_FACE_WIDTH_POSITION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearProfileModificationAtFaceWidthPosition",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.micro_geometry import _670, _673

    Self = TypeVar(
        "Self", bound="CylindricalGearProfileModificationAtFaceWidthPosition"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearProfileModificationAtFaceWidthPosition._Cast_CylindricalGearProfileModificationAtFaceWidthPosition",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearProfileModificationAtFaceWidthPosition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearProfileModificationAtFaceWidthPosition:
    """Special nested class for casting CylindricalGearProfileModificationAtFaceWidthPosition to subclasses."""

    __parent__: "CylindricalGearProfileModificationAtFaceWidthPosition"

    @property
    def cylindrical_gear_profile_modification(
        self: "CastSelf",
    ) -> "_1218.CylindricalGearProfileModification":
        return self.__parent__._cast(_1218.CylindricalGearProfileModification)

    @property
    def profile_modification(self: "CastSelf") -> "_673.ProfileModification":
        from mastapy._private.gears.micro_geometry import _673

        return self.__parent__._cast(_673.ProfileModification)

    @property
    def modification(self: "CastSelf") -> "_670.Modification":
        from mastapy._private.gears.micro_geometry import _670

        return self.__parent__._cast(_670.Modification)

    @property
    def cylindrical_gear_profile_modification_at_face_width_position(
        self: "CastSelf",
    ) -> "CylindricalGearProfileModificationAtFaceWidthPosition":
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
class CylindricalGearProfileModificationAtFaceWidthPosition(
    _1218.CylindricalGearProfileModification
):
    """CylindricalGearProfileModificationAtFaceWidthPosition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYLINDRICAL_GEAR_PROFILE_MODIFICATION_AT_FACE_WIDTH_POSITION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face_width_position(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidthPosition")

        if temp is None:
            return 0.0

        return temp

    @face_width_position.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width_position(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FaceWidthPosition",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def face_width_position_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidthPositionFactor")

        if temp is None:
            return 0.0

        return temp

    @face_width_position_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width_position_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FaceWidthPositionFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CylindricalGearProfileModificationAtFaceWidthPosition":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearProfileModificationAtFaceWidthPosition
        """
        return _Cast_CylindricalGearProfileModificationAtFaceWidthPosition(self)
