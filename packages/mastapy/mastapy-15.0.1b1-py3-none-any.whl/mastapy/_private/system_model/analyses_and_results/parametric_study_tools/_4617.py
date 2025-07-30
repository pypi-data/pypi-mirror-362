"""DutyCycleResultsForRootAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_DUTY_CYCLE_RESULTS_FOR_ROOT_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "DutyCycleResultsForRootAssembly",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3146,
    )

    Self = TypeVar("Self", bound="DutyCycleResultsForRootAssembly")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DutyCycleResultsForRootAssembly._Cast_DutyCycleResultsForRootAssembly",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DutyCycleResultsForRootAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DutyCycleResultsForRootAssembly:
    """Special nested class for casting DutyCycleResultsForRootAssembly to subclasses."""

    __parent__: "DutyCycleResultsForRootAssembly"

    @property
    def duty_cycle_results_for_root_assembly(
        self: "CastSelf",
    ) -> "DutyCycleResultsForRootAssembly":
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
class DutyCycleResultsForRootAssembly(_0.APIBase):
    """DutyCycleResultsForRootAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DUTY_CYCLE_RESULTS_FOR_ROOT_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def duty_cycle_efficiency_results(
        self: "Self",
    ) -> "_3146.DutyCycleEfficiencyResults":
        """mastapy.system_model.analyses_and_results.system_deflections.compound.DutyCycleEfficiencyResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DutyCycleEfficiencyResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_DutyCycleResultsForRootAssembly":
        """Cast to another type.

        Returns:
            _Cast_DutyCycleResultsForRootAssembly
        """
        return _Cast_DutyCycleResultsForRootAssembly(self)
