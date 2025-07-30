"""KlingelnbergCycloPalloidHypoidGearDesign"""

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
from mastapy._private.gears.gear_designs.klingelnberg_conical import _1085

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.KlingelnbergHypoid",
    "KlingelnbergCycloPalloidHypoidGearDesign",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1051, _1052
    from mastapy._private.gears.gear_designs.conical import _1274

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidHypoidGearDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearDesign._Cast_KlingelnbergCycloPalloidHypoidGearDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearDesign:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearDesign to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearDesign"

    @property
    def klingelnberg_conical_gear_design(
        self: "CastSelf",
    ) -> "_1085.KlingelnbergConicalGearDesign":
        return self.__parent__._cast(_1085.KlingelnbergConicalGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1274.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1274

        return self.__parent__._cast(_1274.ConicalGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "_1051.GearDesign":
        from mastapy._private.gears.gear_designs import _1051

        return self.__parent__._cast(_1051.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_design(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearDesign":
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
class KlingelnbergCycloPalloidHypoidGearDesign(_1085.KlingelnbergConicalGearDesign):
    """KlingelnbergCycloPalloidHypoidGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def inner_root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inner_tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerTipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_spiral_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterTipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidHypoidGearDesign":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearDesign
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearDesign(self)
