"""GeometryModellerDimension"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEOMETRY_MODELLER_DIMENSION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "GeometryModellerDimension"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.geometry_modeller_link import _236

    Self = TypeVar("Self", bound="GeometryModellerDimension")
    CastSelf = TypeVar(
        "CastSelf", bound="GeometryModellerDimension._Cast_GeometryModellerDimension"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometryModellerDimension",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeometryModellerDimension:
    """Special nested class for casting GeometryModellerDimension to subclasses."""

    __parent__: "GeometryModellerDimension"

    @property
    def geometry_modeller_dimension(self: "CastSelf") -> "GeometryModellerDimension":
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
class GeometryModellerDimension(_0.APIBase):
    """GeometryModellerDimension

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEOMETRY_MODELLER_DIMENSION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def type_(self: "Self") -> "_236.GeometryModellerDimensionType":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimensionType"""
        temp = pythonnet_property_get(self.wrapped, "Type")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink.GeometryModellerDimensionType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis.geometry_modeller_link._236",
            "GeometryModellerDimensionType",
        )(value)

    @type_.setter
    @exception_bridge
    @enforce_parameter_types
    def type_(self: "Self", value: "_236.GeometryModellerDimensionType") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink.GeometryModellerDimensionType",
        )
        pythonnet_property_set(self.wrapped, "Type", value)

    @property
    @exception_bridge
    def value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Value")

        if temp is None:
            return 0.0

        return temp

    @value.setter
    @exception_bridge
    @enforce_parameter_types
    def value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Value", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GeometryModellerDimension":
        """Cast to another type.

        Returns:
            _Cast_GeometryModellerDimension
        """
        return _Cast_GeometryModellerDimension(self)
