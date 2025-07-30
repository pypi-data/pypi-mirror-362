"""HypoidMeshedGearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.agma_gleason_conical import _1316

_HYPOID_MESHED_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Hypoid", "HypoidMeshedGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1052
    from mastapy._private.gears.gear_designs.conical import _1279

    Self = TypeVar("Self", bound="HypoidMeshedGearDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="HypoidMeshedGearDesign._Cast_HypoidMeshedGearDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidMeshedGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidMeshedGearDesign:
    """Special nested class for casting HypoidMeshedGearDesign to subclasses."""

    __parent__: "HypoidMeshedGearDesign"

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
    def hypoid_meshed_gear_design(self: "CastSelf") -> "HypoidMeshedGearDesign":
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
class HypoidMeshedGearDesign(_1316.AGMAGleasonConicalMeshedGearDesign):
    """HypoidMeshedGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_MESHED_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_HypoidMeshedGearDesign":
        """Cast to another type.

        Returns:
            _Cast_HypoidMeshedGearDesign
        """
        return _Cast_HypoidMeshedGearDesign(self)
