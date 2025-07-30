"""SteadyStateSynchronousResponseViewable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.drawing import _2476

_STEADY_STATE_SYNCHRONOUS_RESPONSE_VIEWABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "SteadyStateSynchronousResponseViewable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SteadyStateSynchronousResponseViewable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SteadyStateSynchronousResponseViewable._Cast_SteadyStateSynchronousResponseViewable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SteadyStateSynchronousResponseViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SteadyStateSynchronousResponseViewable:
    """Special nested class for casting SteadyStateSynchronousResponseViewable to subclasses."""

    __parent__: "SteadyStateSynchronousResponseViewable"

    @property
    def rotor_dynamics_viewable(self: "CastSelf") -> "_2476.RotorDynamicsViewable":
        return self.__parent__._cast(_2476.RotorDynamicsViewable)

    @property
    def steady_state_synchronous_response_viewable(
        self: "CastSelf",
    ) -> "SteadyStateSynchronousResponseViewable":
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
class SteadyStateSynchronousResponseViewable(_2476.RotorDynamicsViewable):
    """SteadyStateSynchronousResponseViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STEADY_STATE_SYNCHRONOUS_RESPONSE_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SteadyStateSynchronousResponseViewable":
        """Cast to another type.

        Returns:
            _Cast_SteadyStateSynchronousResponseViewable
        """
        return _Cast_SteadyStateSynchronousResponseViewable(self)
