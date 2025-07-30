"""ElasticModulusOrthotropicComponents"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ELASTIC_MODULUS_ORTHOTROPIC_COMPONENTS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ElasticModulusOrthotropicComponents",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElasticModulusOrthotropicComponents")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElasticModulusOrthotropicComponents._Cast_ElasticModulusOrthotropicComponents",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElasticModulusOrthotropicComponents",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElasticModulusOrthotropicComponents:
    """Special nested class for casting ElasticModulusOrthotropicComponents to subclasses."""

    __parent__: "ElasticModulusOrthotropicComponents"

    @property
    def elastic_modulus_orthotropic_components(
        self: "CastSelf",
    ) -> "ElasticModulusOrthotropicComponents":
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
class ElasticModulusOrthotropicComponents(_0.APIBase):
    """ElasticModulusOrthotropicComponents

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELASTIC_MODULUS_ORTHOTROPIC_COMPONENTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ex(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EX")

        if temp is None:
            return 0.0

        return temp

    @ex.setter
    @exception_bridge
    @enforce_parameter_types
    def ex(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EX", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def ey(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EY")

        if temp is None:
            return 0.0

        return temp

    @ey.setter
    @exception_bridge
    @enforce_parameter_types
    def ey(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EY", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def ez(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EZ")

        if temp is None:
            return 0.0

        return temp

    @ez.setter
    @exception_bridge
    @enforce_parameter_types
    def ez(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EZ", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ElasticModulusOrthotropicComponents":
        """Cast to another type.

        Returns:
            _Cast_ElasticModulusOrthotropicComponents
        """
        return _Cast_ElasticModulusOrthotropicComponents(self)
