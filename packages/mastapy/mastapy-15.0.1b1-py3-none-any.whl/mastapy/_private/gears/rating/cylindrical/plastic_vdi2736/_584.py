"""PlasticGearVDI2736AbstractRateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.cylindrical.iso6336 import _614

_PLASTIC_GEAR_VDI2736_ABSTRACT_RATEABLE_MESH = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.PlasticVDI2736",
    "PlasticGearVDI2736AbstractRateableMesh",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _458
    from mastapy._private.gears.rating.cylindrical import _562
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _589,
        _590,
        _591,
    )

    Self = TypeVar("Self", bound="PlasticGearVDI2736AbstractRateableMesh")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlasticGearVDI2736AbstractRateableMesh._Cast_PlasticGearVDI2736AbstractRateableMesh",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlasticGearVDI2736AbstractRateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlasticGearVDI2736AbstractRateableMesh:
    """Special nested class for casting PlasticGearVDI2736AbstractRateableMesh to subclasses."""

    __parent__: "PlasticGearVDI2736AbstractRateableMesh"

    @property
    def iso6336_rateable_mesh(self: "CastSelf") -> "_614.ISO6336RateableMesh":
        return self.__parent__._cast(_614.ISO6336RateableMesh)

    @property
    def cylindrical_rateable_mesh(self: "CastSelf") -> "_562.CylindricalRateableMesh":
        from mastapy._private.gears.rating.cylindrical import _562

        return self.__parent__._cast(_562.CylindricalRateableMesh)

    @property
    def rateable_mesh(self: "CastSelf") -> "_458.RateableMesh":
        from mastapy._private.gears.rating import _458

        return self.__parent__._cast(_458.RateableMesh)

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
    def plastic_gear_vdi2736_abstract_rateable_mesh(
        self: "CastSelf",
    ) -> "PlasticGearVDI2736AbstractRateableMesh":
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
class PlasticGearVDI2736AbstractRateableMesh(_614.ISO6336RateableMesh):
    """PlasticGearVDI2736AbstractRateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLASTIC_GEAR_VDI2736_ABSTRACT_RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PlasticGearVDI2736AbstractRateableMesh":
        """Cast to another type.

        Returns:
            _Cast_PlasticGearVDI2736AbstractRateableMesh
        """
        return _Cast_PlasticGearVDI2736AbstractRateableMesh(self)
