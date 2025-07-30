"""GearMeshTEExcitationDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6045

_GEAR_MESH_TE_EXCITATION_DETAIL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "GearMeshTEExcitationDetail",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5969,
    )

    Self = TypeVar("Self", bound="GearMeshTEExcitationDetail")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshTEExcitationDetail._Cast_GearMeshTEExcitationDetail"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshTEExcitationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshTEExcitationDetail:
    """Special nested class for casting GearMeshTEExcitationDetail to subclasses."""

    __parent__: "GearMeshTEExcitationDetail"

    @property
    def gear_mesh_excitation_detail(
        self: "CastSelf",
    ) -> "_6045.GearMeshExcitationDetail":
        return self.__parent__._cast(_6045.GearMeshExcitationDetail)

    @property
    def abstract_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5969.AbstractPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5969,
        )

        return self.__parent__._cast(_5969.AbstractPeriodicExcitationDetail)

    @property
    def gear_mesh_te_excitation_detail(
        self: "CastSelf",
    ) -> "GearMeshTEExcitationDetail":
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
class GearMeshTEExcitationDetail(_6045.GearMeshExcitationDetail):
    """GearMeshTEExcitationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_TE_EXCITATION_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshTEExcitationDetail":
        """Cast to another type.

        Returns:
            _Cast_GearMeshTEExcitationDetail
        """
        return _Cast_GearMeshTEExcitationDetail(self)
