"""GeometryModellerDesignInformation"""

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

_GEOMETRY_MODELLER_DESIGN_INFORMATION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink",
    "GeometryModellerDesignInformation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GeometryModellerDesignInformation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeometryModellerDesignInformation._Cast_GeometryModellerDesignInformation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometryModellerDesignInformation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeometryModellerDesignInformation:
    """Special nested class for casting GeometryModellerDesignInformation to subclasses."""

    __parent__: "GeometryModellerDesignInformation"

    @property
    def geometry_modeller_design_information(
        self: "CastSelf",
    ) -> "GeometryModellerDesignInformation":
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
class GeometryModellerDesignInformation(_0.APIBase):
    """GeometryModellerDesignInformation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEOMETRY_MODELLER_DESIGN_INFORMATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def file_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "FileName")

        if temp is None:
            return ""

        return temp

    @file_name.setter
    @exception_bridge
    @enforce_parameter_types
    def file_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "FileName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def tab_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TabName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def main_part_moniker(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MainPartMoniker")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GeometryModellerDesignInformation":
        """Cast to another type.

        Returns:
            _Cast_GeometryModellerDesignInformation
        """
        return _Cast_GeometryModellerDesignInformation(self)
