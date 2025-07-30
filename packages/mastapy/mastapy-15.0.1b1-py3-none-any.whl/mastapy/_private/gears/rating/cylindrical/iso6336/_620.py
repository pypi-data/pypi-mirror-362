"""ToothFlankFractureAnalysisPointN1457"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_2d import Vector2D

_TOOTH_FLANK_FRACTURE_ANALYSIS_POINT_N1457 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "ToothFlankFractureAnalysisPointN1457",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical.iso6336 import _622

    Self = TypeVar("Self", bound="ToothFlankFractureAnalysisPointN1457")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothFlankFractureAnalysisPointN1457._Cast_ToothFlankFractureAnalysisPointN1457",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothFlankFractureAnalysisPointN1457",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothFlankFractureAnalysisPointN1457:
    """Special nested class for casting ToothFlankFractureAnalysisPointN1457 to subclasses."""

    __parent__: "ToothFlankFractureAnalysisPointN1457"

    @property
    def tooth_flank_fracture_analysis_point_n1457(
        self: "CastSelf",
    ) -> "ToothFlankFractureAnalysisPointN1457":
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
class ToothFlankFractureAnalysisPointN1457(_0.APIBase):
    """ToothFlankFractureAnalysisPointN1457

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_FLANK_FRACTURE_ANALYSIS_POINT_N1457

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def depth_from_surface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DepthFromSurface")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hardness_conversion_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HardnessConversionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_material_hardness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalMaterialHardness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_permissible_shear_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalPermissibleShearStrength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_equivalent_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumEquivalentStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normalised_depth_from_surface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalisedDepthFromSurface")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tangential_component_of_compressive_residual_stresses(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TangentialComponentOfCompressiveResidualStresses"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def coordinates(self: "Self") -> "Vector2D":
        """Vector2D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Coordinates")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def stress_analysis_with_maximum_equivalent_stress(
        self: "Self",
    ) -> "_622.ToothFlankFractureStressStepAtAnalysisPointN1457":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureStressStepAtAnalysisPointN1457

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressAnalysisWithMaximumEquivalentStress"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stress_history(
        self: "Self",
    ) -> "List[_622.ToothFlankFractureStressStepAtAnalysisPointN1457]":
        """List[mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureStressStepAtAnalysisPointN1457]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressHistory")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ToothFlankFractureAnalysisPointN1457":
        """Cast to another type.

        Returns:
            _Cast_ToothFlankFractureAnalysisPointN1457
        """
        return _Cast_ToothFlankFractureAnalysisPointN1457(self)
