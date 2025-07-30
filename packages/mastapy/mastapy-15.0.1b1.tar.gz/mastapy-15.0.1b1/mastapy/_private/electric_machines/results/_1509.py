"""ElectricMachineMechanicalResultsViewable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.elmer import _254

_ELECTRIC_MACHINE_MECHANICAL_RESULTS_VIEWABLE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "ElectricMachineMechanicalResultsViewable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElectricMachineMechanicalResultsViewable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineMechanicalResultsViewable._Cast_ElectricMachineMechanicalResultsViewable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineMechanicalResultsViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineMechanicalResultsViewable:
    """Special nested class for casting ElectricMachineMechanicalResultsViewable to subclasses."""

    __parent__: "ElectricMachineMechanicalResultsViewable"

    @property
    def elmer_results_viewable(self: "CastSelf") -> "_254.ElmerResultsViewable":
        return self.__parent__._cast(_254.ElmerResultsViewable)

    @property
    def electric_machine_mechanical_results_viewable(
        self: "CastSelf",
    ) -> "ElectricMachineMechanicalResultsViewable":
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
class ElectricMachineMechanicalResultsViewable(_254.ElmerResultsViewable):
    """ElectricMachineMechanicalResultsViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_MECHANICAL_RESULTS_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineMechanicalResultsViewable":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineMechanicalResultsViewable
        """
        return _Cast_ElectricMachineMechanicalResultsViewable(self)
