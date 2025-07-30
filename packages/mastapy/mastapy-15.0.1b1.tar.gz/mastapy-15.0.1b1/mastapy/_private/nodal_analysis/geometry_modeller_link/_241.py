"""MeshRequest"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
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
from mastapy._private.nodal_analysis.geometry_modeller_link import _234

_MESH_REQUEST = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "MeshRequest"
)

if TYPE_CHECKING:
    from typing import Any, Dict, List, Type, TypeVar

    from mastapy._private.nodal_analysis.geometry_modeller_link import _233

    Self = TypeVar("Self", bound="MeshRequest")
    CastSelf = TypeVar("CastSelf", bound="MeshRequest._Cast_MeshRequest")


__docformat__ = "restructuredtext en"
__all__ = ("MeshRequest",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshRequest:
    """Special nested class for casting MeshRequest to subclasses."""

    __parent__: "MeshRequest"

    @property
    def mesh_request(self: "CastSelf") -> "MeshRequest":
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
class MeshRequest(_0.APIBase):
    """MeshRequest

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESH_REQUEST

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cad_face_group(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CADFaceGroup")

        if temp is None:
            return False

        return temp

    @cad_face_group.setter
    @exception_bridge
    @enforce_parameter_types
    def cad_face_group(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "CADFaceGroup", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def geometry_modeller_design_information(
        self: "Self",
    ) -> "_233.GeometryModellerDesignInformation":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation"""
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerDesignInformation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @geometry_modeller_design_information.setter
    @exception_bridge
    @enforce_parameter_types
    def geometry_modeller_design_information(
        self: "Self", value: "_233.GeometryModellerDesignInformation"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "GeometryModellerDesignInformation", value.wrapped
        )

    @property
    @exception_bridge
    def monikers(self: "Self") -> "List[str]":
        """List[str]"""
        temp = pythonnet_property_get(self.wrapped, "Monikers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @monikers.setter
    @exception_bridge
    @enforce_parameter_types
    def monikers(self: "Self", value: "List[str]") -> None:
        value = conversion.mp_to_pn_objects_in_list(value)
        pythonnet_property_set(self.wrapped, "Monikers", value)

    @exception_bridge
    def geometry_modeller_dimensions(
        self: "Self",
    ) -> "Dict[str, _234.GeometryModellerDimension]":
        """Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension]"""
        method_result = pythonnet_method_call(
            self.wrapped, "GeometryModellerDimensions"
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_MeshRequest":
        """Cast to another type.

        Returns:
            _Cast_MeshRequest
        """
        return _Cast_MeshRequest(self)
