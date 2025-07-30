"""CylindricalGearFilletNodeStressResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.gears.ltca import _940

_CYLINDRICAL_GEAR_FILLET_NODE_STRESS_RESULTS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "CylindricalGearFilletNodeStressResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearFilletNodeStressResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearFilletNodeStressResults._Cast_CylindricalGearFilletNodeStressResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFilletNodeStressResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFilletNodeStressResults:
    """Special nested class for casting CylindricalGearFilletNodeStressResults to subclasses."""

    __parent__: "CylindricalGearFilletNodeStressResults"

    @property
    def gear_fillet_node_stress_results(
        self: "CastSelf",
    ) -> "_940.GearFilletNodeStressResults":
        return self.__parent__._cast(_940.GearFilletNodeStressResults)

    @property
    def cylindrical_gear_fillet_node_stress_results(
        self: "CastSelf",
    ) -> "CylindricalGearFilletNodeStressResults":
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
class CylindricalGearFilletNodeStressResults(_940.GearFilletNodeStressResults):
    """CylindricalGearFilletNodeStressResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FILLET_NODE_STRESS_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_along_fillet(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DistanceAlongFillet")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_width_position(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidthPosition")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Radius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def position(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Position")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFilletNodeStressResults":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFilletNodeStressResults
        """
        return _Cast_CylindricalGearFilletNodeStressResults(self)
