"""NewtonRaphsonAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_NEWTON_RAPHSON_ANALYSIS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "NewtonRaphsonAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis.system_solvers import _114

    Self = TypeVar("Self", bound="NewtonRaphsonAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="NewtonRaphsonAnalysis._Cast_NewtonRaphsonAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("NewtonRaphsonAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NewtonRaphsonAnalysis:
    """Special nested class for casting NewtonRaphsonAnalysis to subclasses."""

    __parent__: "NewtonRaphsonAnalysis"

    @property
    def newton_raphson_analysis(self: "CastSelf") -> "NewtonRaphsonAnalysis":
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
class NewtonRaphsonAnalysis(_0.APIBase):
    """NewtonRaphsonAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NEWTON_RAPHSON_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def sorted_errors(self: "Self") -> "List[_114.NewtonRaphsonDegreeOfFreedomError]":
        """List[mastapy.nodal_analysis.system_solvers.NewtonRaphsonDegreeOfFreedomError]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SortedErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_NewtonRaphsonAnalysis":
        """Cast to another type.

        Returns:
            _Cast_NewtonRaphsonAnalysis
        """
        return _Cast_NewtonRaphsonAnalysis(self)
