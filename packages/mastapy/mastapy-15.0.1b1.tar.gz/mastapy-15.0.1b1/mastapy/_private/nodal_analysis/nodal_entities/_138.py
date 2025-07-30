"""BearingAxialMountingClearance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _131

_BEARING_AXIAL_MOUNTING_CLEARANCE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "BearingAxialMountingClearance"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _153, _155

    Self = TypeVar("Self", bound="BearingAxialMountingClearance")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingAxialMountingClearance._Cast_BearingAxialMountingClearance",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingAxialMountingClearance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingAxialMountingClearance:
    """Special nested class for casting BearingAxialMountingClearance to subclasses."""

    __parent__: "BearingAxialMountingClearance"

    @property
    def arbitrary_nodal_component_base(
        self: "CastSelf",
    ) -> "_131.ArbitraryNodalComponentBase":
        return self.__parent__._cast(_131.ArbitraryNodalComponentBase)

    @property
    def nodal_component(self: "CastSelf") -> "_153.NodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _153

        return self.__parent__._cast(_153.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def bearing_axial_mounting_clearance(
        self: "CastSelf",
    ) -> "BearingAxialMountingClearance":
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
class BearingAxialMountingClearance(_131.ArbitraryNodalComponentBase):
    """BearingAxialMountingClearance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_AXIAL_MOUNTING_CLEARANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BearingAxialMountingClearance":
        """Cast to another type.

        Returns:
            _Cast_BearingAxialMountingClearance
        """
        return _Cast_BearingAxialMountingClearance(self)
