"""ShaftSectionEndResultsSystemDeflection"""

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

_SHAFT_SECTION_END_RESULTS_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "ShaftSectionEndResultsSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1748
    from mastapy._private.shafts import _16

    Self = TypeVar("Self", bound="ShaftSectionEndResultsSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftSectionEndResultsSystemDeflection._Cast_ShaftSectionEndResultsSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSectionEndResultsSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSectionEndResultsSystemDeflection:
    """Special nested class for casting ShaftSectionEndResultsSystemDeflection to subclasses."""

    __parent__: "ShaftSectionEndResultsSystemDeflection"

    @property
    def shaft_section_end_results_system_deflection(
        self: "CastSelf",
    ) -> "ShaftSectionEndResultsSystemDeflection":
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
class ShaftSectionEndResultsSystemDeflection(_0.APIBase):
    """ShaftSectionEndResultsSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SECTION_END_RESULTS_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cross_sectional_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrossSectionalArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

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
    def outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def polar_area_moment_of_inertia(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PolarAreaMomentOfInertia")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_roughness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceRoughness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def din743201212_fatigue_notch_factor_beta_sigma_beta_tau(
        self: "Self",
    ) -> "_16.ShaftAxialBendingTorsionalComponentValues":
        """mastapy.shafts.ShaftAxialBendingTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DIN743201212FatigueNotchFactorBetaSigmaBetaTau"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def din743201212_geometrical_influence_factor_for_size_k2d(
        self: "Self",
    ) -> "_16.ShaftAxialBendingTorsionalComponentValues":
        """mastapy.shafts.ShaftAxialBendingTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DIN743201212GeometricalInfluenceFactorForSizeK2d"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def din743201212_increase_factor_for_yield_point_gamma_f(
        self: "Self",
    ) -> "_16.ShaftAxialBendingTorsionalComponentValues":
        """mastapy.shafts.ShaftAxialBendingTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DIN743201212IncreaseFactorForYieldPointGammaF"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def din743201212_static_support_factor_k2f(
        self: "Self",
    ) -> "_16.ShaftAxialBendingTorsionalComponentValues":
        """mastapy.shafts.ShaftAxialBendingTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DIN743201212StaticSupportFactorK2F"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def din743201212_surface_roughness_influence_factor_kf_sigma_kf_tau(
        self: "Self",
    ) -> "_16.ShaftAxialBendingTorsionalComponentValues":
        """mastapy.shafts.ShaftAxialBendingTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DIN743201212SurfaceRoughnessInfluenceFactorKFSigmaKFTau"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def din743201212_total_influence_factor_k_sigma_k_tau(
        self: "Self",
    ) -> "_16.ShaftAxialBendingTorsionalComponentValues":
        """mastapy.shafts.ShaftAxialBendingTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DIN743201212TotalInfluenceFactorKSigmaKTau"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def displacements(self: "Self") -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Displacements")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def forces(self: "Self") -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Forces")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSectionEndResultsSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ShaftSectionEndResultsSystemDeflection
        """
        return _Cast_ShaftSectionEndResultsSystemDeflection(self)
