"""GearInMeshDeflectionResults"""

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
)

_GEAR_IN_MESH_DEFLECTION_RESULTS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting",
    "GearInMeshDeflectionResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearInMeshDeflectionResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearInMeshDeflectionResults._Cast_GearInMeshDeflectionResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearInMeshDeflectionResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearInMeshDeflectionResults:
    """Special nested class for casting GearInMeshDeflectionResults to subclasses."""

    __parent__: "GearInMeshDeflectionResults"

    @property
    def gear_in_mesh_deflection_results(
        self: "CastSelf",
    ) -> "GearInMeshDeflectionResults":
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
class GearInMeshDeflectionResults(_0.APIBase):
    """GearInMeshDeflectionResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_IN_MESH_DEFLECTION_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def change_in_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChangeInCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def deflected_flank_position_normal(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DeflectedFlankPositionNormal")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def deflected_flank_position_transverse(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DeflectedFlankPositionTransverse")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def micro_geometry_relief(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroGeometryRelief")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def normal_deflection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalDeflection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_deflection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseDeflection")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GearInMeshDeflectionResults":
        """Cast to another type.

        Returns:
            _Cast_GearInMeshDeflectionResults
        """
        return _Cast_GearInMeshDeflectionResults(self)
