"""BevelMeshedGearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.agma_gleason_conical import _1316

_BEVEL_MESHED_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "BevelMeshedGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1052
    from mastapy._private.gears.gear_designs.conical import _1279
    from mastapy._private.gears.gear_designs.spiral_bevel import _1076
    from mastapy._private.gears.gear_designs.straight_bevel import _1068
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _1072
    from mastapy._private.gears.gear_designs.zerol_bevel import _1059

    Self = TypeVar("Self", bound="BevelMeshedGearDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="BevelMeshedGearDesign._Cast_BevelMeshedGearDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelMeshedGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelMeshedGearDesign:
    """Special nested class for casting BevelMeshedGearDesign to subclasses."""

    __parent__: "BevelMeshedGearDesign"

    @property
    def agma_gleason_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1316.AGMAGleasonConicalMeshedGearDesign":
        return self.__parent__._cast(_1316.AGMAGleasonConicalMeshedGearDesign)

    @property
    def conical_meshed_gear_design(self: "CastSelf") -> "_1279.ConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1279

        return self.__parent__._cast(_1279.ConicalMeshedGearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def zerol_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1059.ZerolBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1059

        return self.__parent__._cast(_1059.ZerolBevelMeshedGearDesign)

    @property
    def straight_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1068.StraightBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1068

        return self.__parent__._cast(_1068.StraightBevelMeshedGearDesign)

    @property
    def straight_bevel_diff_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1072.StraightBevelDiffMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1072

        return self.__parent__._cast(_1072.StraightBevelDiffMeshedGearDesign)

    @property
    def spiral_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1076.SpiralBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1076

        return self.__parent__._cast(_1076.SpiralBevelMeshedGearDesign)

    @property
    def bevel_meshed_gear_design(self: "CastSelf") -> "BevelMeshedGearDesign":
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
class BevelMeshedGearDesign(_1316.AGMAGleasonConicalMeshedGearDesign):
    """BevelMeshedGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_MESHED_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bending_strength_geometry_factor_concave(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BendingStrengthGeometryFactorConcave"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bending_strength_geometry_factor_convex(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BendingStrengthGeometryFactorConvex"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DistanceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def durability_factor_agma(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DurabilityFactorAGMA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def durability_factor_gleason(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DurabilityFactorGleason")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def geometry_factor_j_concave(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorJConcave")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def geometry_factor_j_convex(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorJConvex")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_root_fillet_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumRootFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_chordal_thickness_at_mean_of_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalChordalThicknessAtMeanOfContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def strength_factor_concave(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthFactorConcave")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def strength_factor_convex(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthFactorConvex")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_BevelMeshedGearDesign":
        """Cast to another type.

        Returns:
            _Cast_BevelMeshedGearDesign
        """
        return _Cast_BevelMeshedGearDesign(self)
