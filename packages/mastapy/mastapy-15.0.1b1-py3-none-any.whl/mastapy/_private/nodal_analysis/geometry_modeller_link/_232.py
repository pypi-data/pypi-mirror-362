"""GeometryModellerCountDimension"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.nodal_analysis.geometry_modeller_link import _229

_GEOMETRY_MODELLER_COUNT_DIMENSION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "GeometryModellerCountDimension"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GeometryModellerCountDimension")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeometryModellerCountDimension._Cast_GeometryModellerCountDimension",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometryModellerCountDimension",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeometryModellerCountDimension:
    """Special nested class for casting GeometryModellerCountDimension to subclasses."""

    __parent__: "GeometryModellerCountDimension"

    @property
    def base_geometry_modeller_dimension(
        self: "CastSelf",
    ) -> "_229.BaseGeometryModellerDimension":
        return self.__parent__._cast(_229.BaseGeometryModellerDimension)

    @property
    def geometry_modeller_count_dimension(
        self: "CastSelf",
    ) -> "GeometryModellerCountDimension":
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
class GeometryModellerCountDimension(_229.BaseGeometryModellerDimension):
    """GeometryModellerCountDimension

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEOMETRY_MODELLER_COUNT_DIMENSION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def count(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Count")

        if temp is None:
            return 0

        return temp

    @count.setter
    @exception_bridge
    @enforce_parameter_types
    def count(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Count", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GeometryModellerCountDimension":
        """Cast to another type.

        Returns:
            _Cast_GeometryModellerCountDimension
        """
        return _Cast_GeometryModellerCountDimension(self)
