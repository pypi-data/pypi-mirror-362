"""GeneralPeriodicExcitationDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6105

_GENERAL_PERIODIC_EXCITATION_DETAIL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "GeneralPeriodicExcitationDetail",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5969,
        _6088,
    )

    Self = TypeVar("Self", bound="GeneralPeriodicExcitationDetail")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeneralPeriodicExcitationDetail._Cast_GeneralPeriodicExcitationDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeneralPeriodicExcitationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeneralPeriodicExcitationDetail:
    """Special nested class for casting GeneralPeriodicExcitationDetail to subclasses."""

    __parent__: "GeneralPeriodicExcitationDetail"

    @property
    def single_node_periodic_excitation_with_reference_shaft(
        self: "CastSelf",
    ) -> "_6105.SingleNodePeriodicExcitationWithReferenceShaft":
        return self.__parent__._cast(
            _6105.SingleNodePeriodicExcitationWithReferenceShaft
        )

    @property
    def periodic_excitation_with_reference_shaft(
        self: "CastSelf",
    ) -> "_6088.PeriodicExcitationWithReferenceShaft":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6088,
        )

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
    def general_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "GeneralPeriodicExcitationDetail":
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
class GeneralPeriodicExcitationDetail(
    _6105.SingleNodePeriodicExcitationWithReferenceShaft
):
    """GeneralPeriodicExcitationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GENERAL_PERIODIC_EXCITATION_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GeneralPeriodicExcitationDetail":
        """Cast to another type.

        Returns:
            _Cast_GeneralPeriodicExcitationDetail
        """
        return _Cast_GeneralPeriodicExcitationDetail(self)
