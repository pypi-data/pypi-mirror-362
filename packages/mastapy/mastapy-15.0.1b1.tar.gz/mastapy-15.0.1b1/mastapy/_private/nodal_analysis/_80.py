"""MeshingOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis import _64

_MESHING_OPTIONS = python_net_import("SMT.MastaAPI.NodalAnalysis", "MeshingOptions")

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="MeshingOptions")
    CastSelf = TypeVar("CastSelf", bound="MeshingOptions._Cast_MeshingOptions")


__docformat__ = "restructuredtext en"
__all__ = ("MeshingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshingOptions:
    """Special nested class for casting MeshingOptions to subclasses."""

    __parent__: "MeshingOptions"

    @property
    def fe_meshing_options(self: "CastSelf") -> "_64.FEMeshingOptions":
        return self.__parent__._cast(_64.FEMeshingOptions)

    @property
    def meshing_options(self: "CastSelf") -> "MeshingOptions":
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
class MeshingOptions(_64.FEMeshingOptions):
    """MeshingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESHING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def element_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_size.setter
    @exception_bridge
    @enforce_parameter_types
    def element_size(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementSize", value)

    @property
    def cast_to(self: "Self") -> "_Cast_MeshingOptions":
        """Cast to another type.

        Returns:
            _Cast_MeshingOptions
        """
        return _Cast_MeshingOptions(self)
