"""SingularVectorAnalysis"""

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

_SINGULAR_VECTOR_ANALYSIS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "SingularVectorAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis.system_solvers import _116

    Self = TypeVar("Self", bound="SingularVectorAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="SingularVectorAnalysis._Cast_SingularVectorAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SingularVectorAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SingularVectorAnalysis:
    """Special nested class for casting SingularVectorAnalysis to subclasses."""

    __parent__: "SingularVectorAnalysis"

    @property
    def singular_vector_analysis(self: "CastSelf") -> "SingularVectorAnalysis":
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
class SingularVectorAnalysis(_0.APIBase):
    """SingularVectorAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SINGULAR_VECTOR_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def singular_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SingularValue")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def largest_singular_vector_components(
        self: "Self",
    ) -> "List[_116.SingularDegreeOfFreedomAnalysis]":
        """List[mastapy.nodal_analysis.system_solvers.SingularDegreeOfFreedomAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LargestSingularVectorComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SingularVectorAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SingularVectorAnalysis
        """
        return _Cast_SingularVectorAnalysis(self)
