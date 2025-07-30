"""TransferPathNodeSingleDegreeofFreedomExcitation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6088

_TRANSFER_PATH_NODE_SINGLE_DEGREEOF_FREEDOM_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.TransferPathAnalyses",
    "TransferPathNodeSingleDegreeofFreedomExcitation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5969,
    )

    Self = TypeVar("Self", bound="TransferPathNodeSingleDegreeofFreedomExcitation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TransferPathNodeSingleDegreeofFreedomExcitation._Cast_TransferPathNodeSingleDegreeofFreedomExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TransferPathNodeSingleDegreeofFreedomExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TransferPathNodeSingleDegreeofFreedomExcitation:
    """Special nested class for casting TransferPathNodeSingleDegreeofFreedomExcitation to subclasses."""

    __parent__: "TransferPathNodeSingleDegreeofFreedomExcitation"

    @property
    def periodic_excitation_with_reference_shaft(
        self: "CastSelf",
    ) -> "_6088.PeriodicExcitationWithReferenceShaft":
        return self.__parent__._cast(_6088.PeriodicExcitationWithReferenceShaft)

    @property
    def abstract_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5969.AbstractPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5969,
        )

        return self.__parent__._cast(_5969.AbstractPeriodicExcitationDetail)

    @property
    def transfer_path_node_single_degreeof_freedom_excitation(
        self: "CastSelf",
    ) -> "TransferPathNodeSingleDegreeofFreedomExcitation":
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
class TransferPathNodeSingleDegreeofFreedomExcitation(
    _6088.PeriodicExcitationWithReferenceShaft
):
    """TransferPathNodeSingleDegreeofFreedomExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRANSFER_PATH_NODE_SINGLE_DEGREEOF_FREEDOM_EXCITATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_TransferPathNodeSingleDegreeofFreedomExcitation":
        """Cast to another type.

        Returns:
            _Cast_TransferPathNodeSingleDegreeofFreedomExcitation
        """
        return _Cast_TransferPathNodeSingleDegreeofFreedomExcitation(self)
