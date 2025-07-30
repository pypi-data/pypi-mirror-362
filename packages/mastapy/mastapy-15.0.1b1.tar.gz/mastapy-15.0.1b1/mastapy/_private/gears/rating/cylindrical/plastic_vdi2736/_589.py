"""VDI2736MetalPlasticRateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _584

_VDI2736_METAL_PLASTIC_RATEABLE_MESH = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.PlasticVDI2736",
    "VDI2736MetalPlasticRateableMesh",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _458
    from mastapy._private.gears.rating.cylindrical import _562
    from mastapy._private.gears.rating.cylindrical.iso6336 import _614

    Self = TypeVar("Self", bound="VDI2736MetalPlasticRateableMesh")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VDI2736MetalPlasticRateableMesh._Cast_VDI2736MetalPlasticRateableMesh",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VDI2736MetalPlasticRateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VDI2736MetalPlasticRateableMesh:
    """Special nested class for casting VDI2736MetalPlasticRateableMesh to subclasses."""

    __parent__: "VDI2736MetalPlasticRateableMesh"

    @property
    def plastic_gear_vdi2736_abstract_rateable_mesh(
        self: "CastSelf",
    ) -> "_584.PlasticGearVDI2736AbstractRateableMesh":
        return self.__parent__._cast(_584.PlasticGearVDI2736AbstractRateableMesh)

    @property
    def iso6336_rateable_mesh(self: "CastSelf") -> "_614.ISO6336RateableMesh":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _614

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
    ) -> "VDI2736MetalPlasticRateableMesh":
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
class VDI2736MetalPlasticRateableMesh(_584.PlasticGearVDI2736AbstractRateableMesh):
    """VDI2736MetalPlasticRateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VDI2736_METAL_PLASTIC_RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_VDI2736MetalPlasticRateableMesh":
        """Cast to another type.

        Returns:
            _Cast_VDI2736MetalPlasticRateableMesh
        """
        return _Cast_VDI2736MetalPlasticRateableMesh(self)
