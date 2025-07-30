"""PlaneVectorFieldData"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _7895
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ARRAY = python_net_import("System", "Array")
_PLANE_VECTOR_FIELD_DATA = python_net_import(
    "SMT.MastaAPI.Utility.Vectors", "PlaneVectorFieldData"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="PlaneVectorFieldData")
    CastSelf = TypeVar(
        "CastSelf", bound="PlaneVectorFieldData._Cast_PlaneVectorFieldData"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlaneVectorFieldData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlaneVectorFieldData:
    """Special nested class for casting PlaneVectorFieldData to subclasses."""

    __parent__: "PlaneVectorFieldData"

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7895.MarshalByRefObjectPermanent":
        return self.__parent__._cast(_7895.MarshalByRefObjectPermanent)

    @property
    def plane_vector_field_data(self: "CastSelf") -> "PlaneVectorFieldData":
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
class PlaneVectorFieldData(_7895.MarshalByRefObjectPermanent):
    """PlaneVectorFieldData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANE_VECTOR_FIELD_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def titles(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Titles")

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def values(self: "Self") -> "List[List[float]]":
        """List[List[float]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Values")

        if temp is None:
            return None

        value = conversion.pn_to_mp_list_float_2d(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PlaneVectorFieldData":
        """Cast to another type.

        Returns:
            _Cast_PlaneVectorFieldData
        """
        return _Cast_PlaneVectorFieldData(self)
