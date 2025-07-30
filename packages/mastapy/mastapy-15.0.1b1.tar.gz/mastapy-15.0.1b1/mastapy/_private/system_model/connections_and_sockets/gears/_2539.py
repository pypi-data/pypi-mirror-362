"""KlingelnbergCycloPalloidConicalGearMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.gears import _2528

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidConicalGearMesh",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import _2493, _2502
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2534,
        _2540,
        _2541,
    )

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGearMesh")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearMesh._Cast_KlingelnbergCycloPalloidConicalGearMesh",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearMesh:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearMesh to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearMesh"

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2528.ConicalGearMesh":
        return self.__parent__._cast(_2528.ConicalGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2534.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2534

        return self.__parent__._cast(_2534.GearMesh)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2502.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2502

        return self.__parent__._cast(_2502.InterMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2493.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2493

        return self.__parent__._cast(_2493.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2540.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2540

        return self.__parent__._cast(_2540.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2541.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2541

        return self.__parent__._cast(_2541.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearMesh":
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
class KlingelnbergCycloPalloidConicalGearMesh(_2528.ConicalGearMesh):
    """KlingelnbergCycloPalloidConicalGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidConicalGearMesh":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearMesh
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearMesh(self)
