"""ShearModulusOrthotropicComponents"""

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

_SHEAR_MODULUS_ORTHOTROPIC_COMPONENTS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "ShearModulusOrthotropicComponents",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShearModulusOrthotropicComponents")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShearModulusOrthotropicComponents._Cast_ShearModulusOrthotropicComponents",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShearModulusOrthotropicComponents",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShearModulusOrthotropicComponents:
    """Special nested class for casting ShearModulusOrthotropicComponents to subclasses."""

    __parent__: "ShearModulusOrthotropicComponents"

    @property
    def shear_modulus_orthotropic_components(
        self: "CastSelf",
    ) -> "ShearModulusOrthotropicComponents":
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
class ShearModulusOrthotropicComponents(_0.APIBase):
    """ShearModulusOrthotropicComponents

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHEAR_MODULUS_ORTHOTROPIC_COMPONENTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gxy(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GXY")

        if temp is None:
            return 0.0

        return temp

    @gxy.setter
    @exception_bridge
    @enforce_parameter_types
    def gxy(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "GXY", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def gxz(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GXZ")

        if temp is None:
            return 0.0

        return temp

    @gxz.setter
    @exception_bridge
    @enforce_parameter_types
    def gxz(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "GXZ", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def gyz(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GYZ")

        if temp is None:
            return 0.0

        return temp

    @gyz.setter
    @exception_bridge
    @enforce_parameter_types
    def gyz(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "GYZ", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ShearModulusOrthotropicComponents":
        """Cast to another type.

        Returns:
            _Cast_ShearModulusOrthotropicComponents
        """
        return _Cast_ShearModulusOrthotropicComponents(self)
