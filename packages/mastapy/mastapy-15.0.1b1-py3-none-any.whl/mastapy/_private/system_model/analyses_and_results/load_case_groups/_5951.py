"""ClutchEngagementStatus"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5955
from mastapy._private.system_model.connections_and_sockets.couplings import _2563

_CLUTCH_ENGAGEMENT_STATUS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "ClutchEngagementStatus",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ClutchEngagementStatus")
    CastSelf = TypeVar(
        "CastSelf", bound="ClutchEngagementStatus._Cast_ClutchEngagementStatus"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ClutchEngagementStatus",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ClutchEngagementStatus:
    """Special nested class for casting ClutchEngagementStatus to subclasses."""

    __parent__: "ClutchEngagementStatus"

    @property
    def generic_clutch_engagement_status(
        self: "CastSelf",
    ) -> "_5955.GenericClutchEngagementStatus":
        return self.__parent__._cast(_5955.GenericClutchEngagementStatus)

    @property
    def clutch_engagement_status(self: "CastSelf") -> "ClutchEngagementStatus":
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
class ClutchEngagementStatus(
    _5955.GenericClutchEngagementStatus[_2563.ClutchConnection]
):
    """ClutchEngagementStatus

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLUTCH_ENGAGEMENT_STATUS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ClutchEngagementStatus":
        """Cast to another type.

        Returns:
            _Cast_ClutchEngagementStatus
        """
        return _Cast_ClutchEngagementStatus(self)
