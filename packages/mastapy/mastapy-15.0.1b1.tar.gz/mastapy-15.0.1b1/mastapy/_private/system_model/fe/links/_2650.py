"""MultiNodeFELink"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe.links import _2643

_MULTI_NODE_FE_LINK = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "MultiNodeFELink"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe.links import (
        _2644,
        _2646,
        _2647,
        _2648,
        _2649,
        _2651,
        _2652,
        _2653,
        _2654,
        _2655,
        _2656,
    )

    Self = TypeVar("Self", bound="MultiNodeFELink")
    CastSelf = TypeVar("CastSelf", bound="MultiNodeFELink._Cast_MultiNodeFELink")


__docformat__ = "restructuredtext en"
__all__ = ("MultiNodeFELink",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MultiNodeFELink:
    """Special nested class for casting MultiNodeFELink to subclasses."""

    __parent__: "MultiNodeFELink"

    @property
    def fe_link(self: "CastSelf") -> "_2643.FELink":
        return self.__parent__._cast(_2643.FELink)

    @property
    def electric_machine_stator_fe_link(
        self: "CastSelf",
    ) -> "_2644.ElectricMachineStatorFELink":
        from mastapy._private.system_model.fe.links import _2644

        return self.__parent__._cast(_2644.ElectricMachineStatorFELink)

    @property
    def gear_mesh_fe_link(self: "CastSelf") -> "_2646.GearMeshFELink":
        from mastapy._private.system_model.fe.links import _2646

        return self.__parent__._cast(_2646.GearMeshFELink)

    @property
    def gear_with_duplicated_meshes_fe_link(
        self: "CastSelf",
    ) -> "_2647.GearWithDuplicatedMeshesFELink":
        from mastapy._private.system_model.fe.links import _2647

        return self.__parent__._cast(_2647.GearWithDuplicatedMeshesFELink)

    @property
    def multi_angle_connection_fe_link(
        self: "CastSelf",
    ) -> "_2648.MultiAngleConnectionFELink":
        from mastapy._private.system_model.fe.links import _2648

        return self.__parent__._cast(_2648.MultiAngleConnectionFELink)

    @property
    def multi_node_connector_fe_link(
        self: "CastSelf",
    ) -> "_2649.MultiNodeConnectorFELink":
        from mastapy._private.system_model.fe.links import _2649

        return self.__parent__._cast(_2649.MultiNodeConnectorFELink)

    @property
    def planetary_connector_multi_node_fe_link(
        self: "CastSelf",
    ) -> "_2651.PlanetaryConnectorMultiNodeFELink":
        from mastapy._private.system_model.fe.links import _2651

        return self.__parent__._cast(_2651.PlanetaryConnectorMultiNodeFELink)

    @property
    def planet_based_fe_link(self: "CastSelf") -> "_2652.PlanetBasedFELink":
        from mastapy._private.system_model.fe.links import _2652

        return self.__parent__._cast(_2652.PlanetBasedFELink)

    @property
    def planet_carrier_fe_link(self: "CastSelf") -> "_2653.PlanetCarrierFELink":
        from mastapy._private.system_model.fe.links import _2653

        return self.__parent__._cast(_2653.PlanetCarrierFELink)

    @property
    def point_load_fe_link(self: "CastSelf") -> "_2654.PointLoadFELink":
        from mastapy._private.system_model.fe.links import _2654

        return self.__parent__._cast(_2654.PointLoadFELink)

    @property
    def rolling_ring_connection_fe_link(
        self: "CastSelf",
    ) -> "_2655.RollingRingConnectionFELink":
        from mastapy._private.system_model.fe.links import _2655

        return self.__parent__._cast(_2655.RollingRingConnectionFELink)

    @property
    def shaft_hub_connection_fe_link(
        self: "CastSelf",
    ) -> "_2656.ShaftHubConnectionFELink":
        from mastapy._private.system_model.fe.links import _2656

        return self.__parent__._cast(_2656.ShaftHubConnectionFELink)

    @property
    def multi_node_fe_link(self: "CastSelf") -> "MultiNodeFELink":
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
class MultiNodeFELink(_2643.FELink):
    """MultiNodeFELink

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MULTI_NODE_FE_LINK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MultiNodeFELink":
        """Cast to another type.

        Returns:
            _Cast_MultiNodeFELink
        """
        return _Cast_MultiNodeFELink(self)
