"""ElementPropertiesSpringDashpot"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import _294

_ELEMENT_PROPERTIES_SPRING_DASHPOT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ElementPropertiesSpringDashpot",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElementPropertiesSpringDashpot")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElementPropertiesSpringDashpot._Cast_ElementPropertiesSpringDashpot",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesSpringDashpot",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementPropertiesSpringDashpot:
    """Special nested class for casting ElementPropertiesSpringDashpot to subclasses."""

    __parent__: "ElementPropertiesSpringDashpot"

    @property
    def element_properties_base(self: "CastSelf") -> "_294.ElementPropertiesBase":
        return self.__parent__._cast(_294.ElementPropertiesBase)

    @property
    def element_properties_spring_dashpot(
        self: "CastSelf",
    ) -> "ElementPropertiesSpringDashpot":
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
class ElementPropertiesSpringDashpot(_294.ElementPropertiesBase):
    """ElementPropertiesSpringDashpot

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_PROPERTIES_SPRING_DASHPOT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def degree_of_freedom_1(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DegreeOfFreedom1")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def degree_of_freedom_2(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DegreeOfFreedom2")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def rotational_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationalStiffness")

        if temp is None:
            return 0.0

        return temp

    @rotational_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def rotational_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotationalStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Stiffness")

        if temp is None:
            return 0.0

        return temp

    @stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Stiffness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def stiffness_matrix_lower_triangle(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessMatrixLowerTriangle")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def translational_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TranslationalStiffness")

        if temp is None:
            return 0.0

        return temp

    @translational_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def translational_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TranslationalStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rotational_stiffness_vector(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotationalStiffnessVector")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def translational_stiffness_vector(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TranslationalStiffnessVector")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ElementPropertiesSpringDashpot":
        """Cast to another type.

        Returns:
            _Cast_ElementPropertiesSpringDashpot
        """
        return _Cast_ElementPropertiesSpringDashpot(self)
