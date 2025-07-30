"""FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_FACE_GEAR_MESH_MISALIGNMENTS_WITH_RESPECT_TO_CROSS_POINT_CALCULATOR = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
        "FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1280

    Self = TypeVar(
        "Self", bound="FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator._Cast_FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator:
    """Special nested class for casting FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator to subclasses."""

    __parent__: "FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator"

    @property
    def face_gear_mesh_misalignments_with_respect_to_cross_point_calculator(
        self: "CastSelf",
    ) -> "FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator":
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
class FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator(_0.APIBase):
    """FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _FACE_GEAR_MESH_MISALIGNMENTS_WITH_RESPECT_TO_CROSS_POINT_CALCULATOR
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def misalignments_pinion(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsPinion")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_total(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsTotal")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignments_wheel(self: "Self") -> "_1280.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsWheel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator":
        """Cast to another type.

        Returns:
            _Cast_FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator
        """
        return _Cast_FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator(self)
