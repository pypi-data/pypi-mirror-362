"""DistributedRigidBarCoupling"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _153

_DISTRIBUTED_RIGID_BAR_COUPLING = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "DistributedRigidBarCoupling"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _155

    Self = TypeVar("Self", bound="DistributedRigidBarCoupling")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DistributedRigidBarCoupling._Cast_DistributedRigidBarCoupling",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DistributedRigidBarCoupling",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DistributedRigidBarCoupling:
    """Special nested class for casting DistributedRigidBarCoupling to subclasses."""

    __parent__: "DistributedRigidBarCoupling"

    @property
    def nodal_component(self: "CastSelf") -> "_153.NodalComponent":
        return self.__parent__._cast(_153.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def distributed_rigid_bar_coupling(
        self: "CastSelf",
    ) -> "DistributedRigidBarCoupling":
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
class DistributedRigidBarCoupling(_153.NodalComponent):
    """DistributedRigidBarCoupling

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DISTRIBUTED_RIGID_BAR_COUPLING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DistributedRigidBarCoupling":
        """Cast to another type.

        Returns:
            _Cast_DistributedRigidBarCoupling
        """
        return _Cast_DistributedRigidBarCoupling(self)
