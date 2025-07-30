"""StraightBevelMeshedGearDesign"""

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
from mastapy._private.gears.gear_designs.bevel import _1303

_STRAIGHT_BEVEL_MESHED_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.StraightBevel", "StraightBevelMeshedGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1052
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1316
    from mastapy._private.gears.gear_designs.conical import _1279

    Self = TypeVar("Self", bound="StraightBevelMeshedGearDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelMeshedGearDesign._Cast_StraightBevelMeshedGearDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelMeshedGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelMeshedGearDesign:
    """Special nested class for casting StraightBevelMeshedGearDesign to subclasses."""

    __parent__: "StraightBevelMeshedGearDesign"

    @property
    def bevel_meshed_gear_design(self: "CastSelf") -> "_1303.BevelMeshedGearDesign":
        return self.__parent__._cast(_1303.BevelMeshedGearDesign)

    @property
    def agma_gleason_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1316.AGMAGleasonConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1316

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
    def straight_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "StraightBevelMeshedGearDesign":
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
class StraightBevelMeshedGearDesign(_1303.BevelMeshedGearDesign):
    """StraightBevelMeshedGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_MESHED_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def geometry_factor_j(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorJ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def strength_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelMeshedGearDesign":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelMeshedGearDesign
        """
        return _Cast_StraightBevelMeshedGearDesign(self)
