"""ComplianceAndForceData"""

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

_COMPLIANCE_AND_FORCE_DATA = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "ComplianceAndForceData",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="ComplianceAndForceData")
    CastSelf = TypeVar(
        "CastSelf", bound="ComplianceAndForceData._Cast_ComplianceAndForceData"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComplianceAndForceData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComplianceAndForceData:
    """Special nested class for casting ComplianceAndForceData to subclasses."""

    __parent__: "ComplianceAndForceData"

    @property
    def compliance_and_force_data(self: "CastSelf") -> "ComplianceAndForceData":
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
class ComplianceAndForceData(_0.APIBase):
    """ComplianceAndForceData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPLIANCE_AND_FORCE_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def frequencies_for_compliances(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequenciesForCompliances")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def frequencies_for_mesh_forces(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequenciesForMeshForces")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_a_compliance(self: "Self") -> "List[complex]":
        """List[complex]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearACompliance")

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_b_compliance(self: "Self") -> "List[complex]":
        """List[complex]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBCompliance")

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def mesh_forces_per_unit_te(self: "Self") -> "List[complex]":
        """List[complex]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshForcesPerUnitTE")

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ComplianceAndForceData":
        """Cast to another type.

        Returns:
            _Cast_ComplianceAndForceData
        """
        return _Cast_ComplianceAndForceData(self)
