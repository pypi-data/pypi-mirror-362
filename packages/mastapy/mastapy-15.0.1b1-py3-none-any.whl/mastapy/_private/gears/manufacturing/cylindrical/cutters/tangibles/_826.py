"""CutterShapeDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CUTTER_SHAPE_DEFINITION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters.Tangibles",
    "CutterShapeDefinition",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _816
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
        _827,
        _828,
        _829,
        _830,
        _831,
        _832,
        _833,
    )

    Self = TypeVar("Self", bound="CutterShapeDefinition")
    CastSelf = TypeVar(
        "CastSelf", bound="CutterShapeDefinition._Cast_CutterShapeDefinition"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CutterShapeDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CutterShapeDefinition:
    """Special nested class for casting CutterShapeDefinition to subclasses."""

    __parent__: "CutterShapeDefinition"

    @property
    def cylindrical_gear_formed_wheel_grinder_tangible(
        self: "CastSelf",
    ) -> "_827.CylindricalGearFormedWheelGrinderTangible":
        from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
            _827,
        )

        return self.__parent__._cast(_827.CylindricalGearFormedWheelGrinderTangible)

    @property
    def cylindrical_gear_hob_shape(self: "CastSelf") -> "_828.CylindricalGearHobShape":
        from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
            _828,
        )

        return self.__parent__._cast(_828.CylindricalGearHobShape)

    @property
    def cylindrical_gear_shaper_tangible(
        self: "CastSelf",
    ) -> "_829.CylindricalGearShaperTangible":
        from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
            _829,
        )

        return self.__parent__._cast(_829.CylindricalGearShaperTangible)

    @property
    def cylindrical_gear_shaver_tangible(
        self: "CastSelf",
    ) -> "_830.CylindricalGearShaverTangible":
        from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
            _830,
        )

        return self.__parent__._cast(_830.CylindricalGearShaverTangible)

    @property
    def cylindrical_gear_worm_grinder_shape(
        self: "CastSelf",
    ) -> "_831.CylindricalGearWormGrinderShape":
        from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
            _831,
        )

        return self.__parent__._cast(_831.CylindricalGearWormGrinderShape)

    @property
    def rack_shape(self: "CastSelf") -> "_833.RackShape":
        from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
            _833,
        )

        return self.__parent__._cast(_833.RackShape)

    @property
    def cutter_shape_definition(self: "CastSelf") -> "CutterShapeDefinition":
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
class CutterShapeDefinition(_0.APIBase):
    """CutterShapeDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUTTER_SHAPE_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def normal_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalModule")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def design(self: "Self") -> "_816.CylindricalGearRealCutterDesign":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearRealCutterDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Design")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def fillet_points(self: "Self") -> "List[_832.NamedPoint]":
        """List[mastapy.gears.manufacturing.cylindrical.cutters.tangibles.NamedPoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FilletPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def main_blade_points(self: "Self") -> "List[_832.NamedPoint]":
        """List[mastapy.gears.manufacturing.cylindrical.cutters.tangibles.NamedPoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MainBladePoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CutterShapeDefinition":
        """Cast to another type.

        Returns:
            _Cast_CutterShapeDefinition
        """
        return _Cast_CutterShapeDefinition(self)
