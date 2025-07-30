"""BevelGearMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.connections_and_sockets.gears import _2520

_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelGearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.bevel import _1301
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import _2493, _2502
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2522,
        _2528,
        _2534,
        _2544,
        _2546,
        _2548,
        _2552,
    )

    Self = TypeVar("Self", bound="BevelGearMesh")
    CastSelf = TypeVar("CastSelf", bound="BevelGearMesh._Cast_BevelGearMesh")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMesh:
    """Special nested class for casting BevelGearMesh to subclasses."""

    __parent__: "BevelGearMesh"

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2520.AGMAGleasonConicalGearMesh":
        return self.__parent__._cast(_2520.AGMAGleasonConicalGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2528.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2528

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
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2522.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2522

        return self.__parent__._cast(_2522.BevelDifferentialGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2544.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2544

        return self.__parent__._cast(_2544.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2546.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2546

        return self.__parent__._cast(_2546.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2548.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2548

        return self.__parent__._cast(_2548.StraightBevelGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2552.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2552

        return self.__parent__._cast(_2552.ZerolBevelGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "BevelGearMesh":
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
class BevelGearMesh(_2520.AGMAGleasonConicalGearMesh):
    """BevelGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_gear_mesh_design(self: "Self") -> "_1301.BevelGearMeshDesign":
        """mastapy.gears.gear_designs.bevel.BevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bevel_gear_mesh_design(self: "Self") -> "_1301.BevelGearMeshDesign":
        """mastapy.gears.gear_designs.bevel.BevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearMesh":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMesh
        """
        return _Cast_BevelGearMesh(self)
