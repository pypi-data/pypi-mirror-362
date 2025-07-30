"""GearMeshResultsAtOffset"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_GEAR_MESH_RESULTS_AT_OFFSET = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting",
    "GearMeshResultsAtOffset",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3087,
    )

    Self = TypeVar("Self", bound="GearMeshResultsAtOffset")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshResultsAtOffset._Cast_GearMeshResultsAtOffset"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshResultsAtOffset",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshResultsAtOffset:
    """Special nested class for casting GearMeshResultsAtOffset to subclasses."""

    __parent__: "GearMeshResultsAtOffset"

    @property
    def gear_mesh_results_at_offset(self: "CastSelf") -> "GearMeshResultsAtOffset":
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
class GearMeshResultsAtOffset(_0.APIBase):
    """GearMeshResultsAtOffset

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_RESULTS_AT_OFFSET

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
    def initial_gap_due_to_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InitialGapDueToBacklash")

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
    def normal_force_per_unit_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalForcePerUnitFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_stiffness_per_unit_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalStiffnessPerUnitFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def offset(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def operating_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingBacklash")

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
    @exception_bridge
    def transverse_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gears(self: "Self") -> "List[_3087.GearInMeshDeflectionResults]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.reporting.GearInMeshDeflectionResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshResultsAtOffset":
        """Cast to another type.

        Returns:
            _Cast_GearMeshResultsAtOffset
        """
        return _Cast_GearMeshResultsAtOffset(self)
