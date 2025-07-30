"""CouplingConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2502

_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "CouplingConnection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import _2493
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2563,
        _2565,
        _2569,
        _2571,
        _2573,
    )

    Self = TypeVar("Self", bound="CouplingConnection")
    CastSelf = TypeVar("CastSelf", bound="CouplingConnection._Cast_CouplingConnection")


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnection:
    """Special nested class for casting CouplingConnection to subclasses."""

    __parent__: "CouplingConnection"

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2502.InterMountableComponentConnection":
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
    def clutch_connection(self: "CastSelf") -> "_2563.ClutchConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2563,
        )

        return self.__parent__._cast(_2563.ClutchConnection)

    @property
    def concept_coupling_connection(
        self: "CastSelf",
    ) -> "_2565.ConceptCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2565,
        )

        return self.__parent__._cast(_2565.ConceptCouplingConnection)

    @property
    def part_to_part_shear_coupling_connection(
        self: "CastSelf",
    ) -> "_2569.PartToPartShearCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2569,
        )

        return self.__parent__._cast(_2569.PartToPartShearCouplingConnection)

    @property
    def spring_damper_connection(self: "CastSelf") -> "_2571.SpringDamperConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2571,
        )

        return self.__parent__._cast(_2571.SpringDamperConnection)

    @property
    def torque_converter_connection(
        self: "CastSelf",
    ) -> "_2573.TorqueConverterConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2573,
        )

        return self.__parent__._cast(_2573.TorqueConverterConnection)

    @property
    def coupling_connection(self: "CastSelf") -> "CouplingConnection":
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
class CouplingConnection(_2502.InterMountableComponentConnection):
    """CouplingConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingConnection":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnection
        """
        return _Cast_CouplingConnection(self)
