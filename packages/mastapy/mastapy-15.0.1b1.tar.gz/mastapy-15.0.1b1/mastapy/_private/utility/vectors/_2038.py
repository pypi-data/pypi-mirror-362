"""PlaneScalarFieldData"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _7895
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ARRAY = python_net_import("System", "Array")
_PLANE_SCALAR_FIELD_DATA = python_net_import(
    "SMT.MastaAPI.Utility.Vectors", "PlaneScalarFieldData"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="PlaneScalarFieldData")
    CastSelf = TypeVar(
        "CastSelf", bound="PlaneScalarFieldData._Cast_PlaneScalarFieldData"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlaneScalarFieldData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlaneScalarFieldData:
    """Special nested class for casting PlaneScalarFieldData to subclasses."""

    __parent__: "PlaneScalarFieldData"

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7895.MarshalByRefObjectPermanent":
        return self.__parent__._cast(_7895.MarshalByRefObjectPermanent)

    @property
    def plane_scalar_field_data(self: "CastSelf") -> "PlaneScalarFieldData":
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
class PlaneScalarFieldData(_7895.MarshalByRefObjectPermanent):
    """PlaneScalarFieldData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANE_SCALAR_FIELD_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def x_title(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XTitle")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def y_title(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YTitle")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def z_title(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZTitle")

        if temp is None:
            return ""

        return temp

    @exception_bridge
    @enforce_parameter_types
    def to_regular_gridded_points(
        self: "Self", extrapolate: "bool"
    ) -> "List[List[float]]":
        """List[List[float]]

        Args:
            extrapolate (bool)
        """
        extrapolate = bool(extrapolate)
        return conversion.pn_to_mp_list_float_2d(
            pythonnet_method_call(
                self.wrapped,
                "ToRegularGriddedPoints",
                extrapolate if extrapolate else False,
            )
        )

    @exception_bridge
    def to_irregular_points(self: "Self") -> "List[List[float]]":
        """List[List[float]]"""
        return conversion.pn_to_mp_list_float_2d(
            pythonnet_method_call(self.wrapped, "ToIrregularPoints")
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PlaneScalarFieldData":
        """Cast to another type.

        Returns:
            _Cast_PlaneScalarFieldData
        """
        return _Cast_PlaneScalarFieldData(self)
