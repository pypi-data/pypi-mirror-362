"""CompoundDynamicModelForStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results import _2888

_COMPOUND_DYNAMIC_MODEL_FOR_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults",
    "CompoundDynamicModelForStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7895

    Self = TypeVar("Self", bound="CompoundDynamicModelForStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CompoundDynamicModelForStabilityAnalysis._Cast_CompoundDynamicModelForStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CompoundDynamicModelForStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CompoundDynamicModelForStabilityAnalysis:
    """Special nested class for casting CompoundDynamicModelForStabilityAnalysis to subclasses."""

    __parent__: "CompoundDynamicModelForStabilityAnalysis"

    @property
    def compound_analysis(self: "CastSelf") -> "_2888.CompoundAnalysis":
        return self.__parent__._cast(_2888.CompoundAnalysis)

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7895.MarshalByRefObjectPermanent":
        from mastapy._private import _7895

        return self.__parent__._cast(_7895.MarshalByRefObjectPermanent)

    @property
    def compound_dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "CompoundDynamicModelForStabilityAnalysis":
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
class CompoundDynamicModelForStabilityAnalysis(_2888.CompoundAnalysis):
    """CompoundDynamicModelForStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPOUND_DYNAMIC_MODEL_FOR_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CompoundDynamicModelForStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CompoundDynamicModelForStabilityAnalysis
        """
        return _Cast_CompoundDynamicModelForStabilityAnalysis(self)
