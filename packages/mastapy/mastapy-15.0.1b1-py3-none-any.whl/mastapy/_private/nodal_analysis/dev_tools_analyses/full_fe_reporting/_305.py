"""PoissonRatioOrthotropicComponents"""

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

_POISSON_RATIO_ORTHOTROPIC_COMPONENTS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting",
    "PoissonRatioOrthotropicComponents",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PoissonRatioOrthotropicComponents")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PoissonRatioOrthotropicComponents._Cast_PoissonRatioOrthotropicComponents",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PoissonRatioOrthotropicComponents",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PoissonRatioOrthotropicComponents:
    """Special nested class for casting PoissonRatioOrthotropicComponents to subclasses."""

    __parent__: "PoissonRatioOrthotropicComponents"

    @property
    def poisson_ratio_orthotropic_components(
        self: "CastSelf",
    ) -> "PoissonRatioOrthotropicComponents":
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
class PoissonRatioOrthotropicComponents(_0.APIBase):
    """PoissonRatioOrthotropicComponents

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POISSON_RATIO_ORTHOTROPIC_COMPONENTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def nu_xy(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NuXY")

        if temp is None:
            return 0.0

        return temp

    @nu_xy.setter
    @exception_bridge
    @enforce_parameter_types
    def nu_xy(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NuXY", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def nu_xz(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NuXZ")

        if temp is None:
            return 0.0

        return temp

    @nu_xz.setter
    @exception_bridge
    @enforce_parameter_types
    def nu_xz(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NuXZ", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def nu_yz(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NuYZ")

        if temp is None:
            return 0.0

        return temp

    @nu_yz.setter
    @exception_bridge
    @enforce_parameter_types
    def nu_yz(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NuYZ", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PoissonRatioOrthotropicComponents":
        """Cast to another type.

        Returns:
            _Cast_PoissonRatioOrthotropicComponents
        """
        return _Cast_PoissonRatioOrthotropicComponents(self)
