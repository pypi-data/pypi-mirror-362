"""SingularValuesAnalysis"""

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

_SINGULAR_VALUES_ANALYSIS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "SingularValuesAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis.system_solvers import _118

    Self = TypeVar("Self", bound="SingularValuesAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="SingularValuesAnalysis._Cast_SingularValuesAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SingularValuesAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SingularValuesAnalysis:
    """Special nested class for casting SingularValuesAnalysis to subclasses."""

    __parent__: "SingularValuesAnalysis"

    @property
    def singular_values_analysis(self: "CastSelf") -> "SingularValuesAnalysis":
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
class SingularValuesAnalysis(_0.APIBase):
    """SingularValuesAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SINGULAR_VALUES_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def condition_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConditionNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stiffness_matrix_degrees_of_freedom(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessMatrixDegreesOfFreedom")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def stiffness_matrix_rank(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessMatrixRank")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def largest_singular_vectors(self: "Self") -> "List[_118.SingularVectorAnalysis]":
        """List[mastapy.nodal_analysis.system_solvers.SingularVectorAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LargestSingularVectors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def smallest_singular_vectors(self: "Self") -> "List[_118.SingularVectorAnalysis]":
        """List[mastapy.nodal_analysis.system_solvers.SingularVectorAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallestSingularVectors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SingularValuesAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SingularValuesAnalysis
        """
        return _Cast_SingularValuesAnalysis(self)
