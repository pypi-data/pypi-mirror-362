"""FEStiffnessGeometry"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_FE_STIFFNESS_GEOMETRY = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FEStiffnessGeometry"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEStiffnessGeometry")
    CastSelf = TypeVar(
        "CastSelf", bound="FEStiffnessGeometry._Cast_FEStiffnessGeometry"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEStiffnessGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEStiffnessGeometry:
    """Special nested class for casting FEStiffnessGeometry to subclasses."""

    __parent__: "FEStiffnessGeometry"

    @property
    def fe_stiffness_geometry(self: "CastSelf") -> "FEStiffnessGeometry":
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
class FEStiffnessGeometry(_0.APIBase):
    """FEStiffnessGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_STIFFNESS_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @exception_bridge
    def delete_geometry(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteGeometry")

    @exception_bridge
    def reduce_file_size(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ReduceFileSize")

    @property
    def cast_to(self: "Self") -> "_Cast_FEStiffnessGeometry":
        """Cast to another type.

        Returns:
            _Cast_FEStiffnessGeometry
        """
        return _Cast_FEStiffnessGeometry(self)
