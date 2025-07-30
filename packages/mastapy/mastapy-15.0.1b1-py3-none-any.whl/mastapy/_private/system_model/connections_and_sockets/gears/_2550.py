"""WormGearMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets.gears import _2534

_WORM_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "WormGearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.worm import _1062
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import _2493, _2502

    Self = TypeVar("Self", bound="WormGearMesh")
    CastSelf = TypeVar("CastSelf", bound="WormGearMesh._Cast_WormGearMesh")


__docformat__ = "restructuredtext en"
__all__ = ("WormGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearMesh:
    """Special nested class for casting WormGearMesh to subclasses."""

    __parent__: "WormGearMesh"

    @property
    def gear_mesh(self: "CastSelf") -> "_2534.GearMesh":
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
    def worm_gear_mesh(self: "CastSelf") -> "WormGearMesh":
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
class WormGearMesh(_2534.GearMesh):
    """WormGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def meshing_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeshingAngle")

        if temp is None:
            return 0.0

        return temp

    @meshing_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def meshing_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeshingAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def active_gear_mesh_design(self: "Self") -> "_1062.WormGearMeshDesign":
        """mastapy.gears.gear_designs.worm.WormGearMeshDesign

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
    def worm_gear_mesh_design(self: "Self") -> "_1062.WormGearMeshDesign":
        """mastapy.gears.gear_designs.worm.WormGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearMesh":
        """Cast to another type.

        Returns:
            _Cast_WormGearMesh
        """
        return _Cast_WormGearMesh(self)
