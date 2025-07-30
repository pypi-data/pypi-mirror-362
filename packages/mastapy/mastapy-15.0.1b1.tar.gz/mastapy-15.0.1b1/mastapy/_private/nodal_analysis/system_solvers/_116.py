"""SingularDegreeOfFreedomAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_SINGULAR_DEGREE_OF_FREEDOM_ANALYSIS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.SystemSolvers", "SingularDegreeOfFreedomAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SingularDegreeOfFreedomAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SingularDegreeOfFreedomAnalysis._Cast_SingularDegreeOfFreedomAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SingularDegreeOfFreedomAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SingularDegreeOfFreedomAnalysis:
    """Special nested class for casting SingularDegreeOfFreedomAnalysis to subclasses."""

    __parent__: "SingularDegreeOfFreedomAnalysis"

    @property
    def singular_degree_of_freedom_analysis(
        self: "CastSelf",
    ) -> "SingularDegreeOfFreedomAnalysis":
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
class SingularDegreeOfFreedomAnalysis(_0.APIBase):
    """SingularDegreeOfFreedomAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SINGULAR_DEGREE_OF_FREEDOM_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def components_using_node(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentsUsingNode")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def global_degree_of_freedom(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GlobalDegreeOfFreedom")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def nodal_entities_using_node(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodalEntitiesUsingNode")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def node_degree_of_freedom(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeDegreeOfFreedom")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def node_id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeID")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def node_names(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeNames")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def vector_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VectorValue")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SingularDegreeOfFreedomAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SingularDegreeOfFreedomAnalysis
        """
        return _Cast_SingularDegreeOfFreedomAnalysis(self)
