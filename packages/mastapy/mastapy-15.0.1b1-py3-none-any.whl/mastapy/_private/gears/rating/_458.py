"""RateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_RATEABLE_MESH = python_net_import("SMT.MastaAPI.Gears.Rating", "RateableMesh")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.agma_gleason_conical import _659
    from mastapy._private.gears.rating.bevel.standards import _655
    from mastapy._private.gears.rating.conical import _638
    from mastapy._private.gears.rating.cylindrical import _562
    from mastapy._private.gears.rating.cylindrical.agma import _627
    from mastapy._private.gears.rating.cylindrical.iso6336 import _613, _614
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _584,
        _589,
        _590,
        _591,
    )
    from mastapy._private.gears.rating.hypoid.standards import _535
    from mastapy._private.gears.rating.iso_10300 import _518
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _506

    Self = TypeVar("Self", bound="RateableMesh")
    CastSelf = TypeVar("CastSelf", bound="RateableMesh._Cast_RateableMesh")


__docformat__ = "restructuredtext en"
__all__ = ("RateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RateableMesh:
    """Special nested class for casting RateableMesh to subclasses."""

    __parent__: "RateableMesh"

    @property
    def klingelnberg_conical_rateable_mesh(
        self: "CastSelf",
    ) -> "_506.KlingelnbergConicalRateableMesh":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _506

        return self.__parent__._cast(_506.KlingelnbergConicalRateableMesh)

    @property
    def iso10300_rateable_mesh(self: "CastSelf") -> "_518.ISO10300RateableMesh":
        from mastapy._private.gears.rating.iso_10300 import _518

        return self.__parent__._cast(_518.ISO10300RateableMesh)

    @property
    def hypoid_rateable_mesh(self: "CastSelf") -> "_535.HypoidRateableMesh":
        from mastapy._private.gears.rating.hypoid.standards import _535

        return self.__parent__._cast(_535.HypoidRateableMesh)

    @property
    def cylindrical_rateable_mesh(self: "CastSelf") -> "_562.CylindricalRateableMesh":
        from mastapy._private.gears.rating.cylindrical import _562

        return self.__parent__._cast(_562.CylindricalRateableMesh)

    @property
    def plastic_gear_vdi2736_abstract_rateable_mesh(
        self: "CastSelf",
    ) -> "_584.PlasticGearVDI2736AbstractRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _584

        return self.__parent__._cast(_584.PlasticGearVDI2736AbstractRateableMesh)

    @property
    def vdi2736_metal_plastic_rateable_mesh(
        self: "CastSelf",
    ) -> "_589.VDI2736MetalPlasticRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _589

        return self.__parent__._cast(_589.VDI2736MetalPlasticRateableMesh)

    @property
    def vdi2736_plastic_metal_rateable_mesh(
        self: "CastSelf",
    ) -> "_590.VDI2736PlasticMetalRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _590

        return self.__parent__._cast(_590.VDI2736PlasticMetalRateableMesh)

    @property
    def vdi2736_plastic_plastic_rateable_mesh(
        self: "CastSelf",
    ) -> "_591.VDI2736PlasticPlasticRateableMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _591

        return self.__parent__._cast(_591.VDI2736PlasticPlasticRateableMesh)

    @property
    def iso6336_metal_rateable_mesh(
        self: "CastSelf",
    ) -> "_613.ISO6336MetalRateableMesh":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _613

        return self.__parent__._cast(_613.ISO6336MetalRateableMesh)

    @property
    def iso6336_rateable_mesh(self: "CastSelf") -> "_614.ISO6336RateableMesh":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _614

        return self.__parent__._cast(_614.ISO6336RateableMesh)

    @property
    def agma2101_rateable_mesh(self: "CastSelf") -> "_627.AGMA2101RateableMesh":
        from mastapy._private.gears.rating.cylindrical.agma import _627

        return self.__parent__._cast(_627.AGMA2101RateableMesh)

    @property
    def conical_rateable_mesh(self: "CastSelf") -> "_638.ConicalRateableMesh":
        from mastapy._private.gears.rating.conical import _638

        return self.__parent__._cast(_638.ConicalRateableMesh)

    @property
    def spiral_bevel_rateable_mesh(self: "CastSelf") -> "_655.SpiralBevelRateableMesh":
        from mastapy._private.gears.rating.bevel.standards import _655

        return self.__parent__._cast(_655.SpiralBevelRateableMesh)

    @property
    def agma_gleason_conical_rateable_mesh(
        self: "CastSelf",
    ) -> "_659.AGMAGleasonConicalRateableMesh":
        from mastapy._private.gears.rating.agma_gleason_conical import _659

        return self.__parent__._cast(_659.AGMAGleasonConicalRateableMesh)

    @property
    def rateable_mesh(self: "CastSelf") -> "RateableMesh":
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
class RateableMesh(_0.APIBase):
    """RateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RateableMesh":
        """Cast to another type.

        Returns:
            _Cast_RateableMesh
        """
        return _Cast_RateableMesh(self)
