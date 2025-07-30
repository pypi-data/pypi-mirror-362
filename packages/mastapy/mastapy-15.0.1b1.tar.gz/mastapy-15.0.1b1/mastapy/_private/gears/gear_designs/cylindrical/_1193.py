"""TiffAnalysisSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1779

_TIFF_ANALYSIS_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "TiffAnalysisSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1161
    from mastapy._private.math_utility import _1718

    Self = TypeVar("Self", bound="TiffAnalysisSettings")
    CastSelf = TypeVar(
        "CastSelf", bound="TiffAnalysisSettings._Cast_TiffAnalysisSettings"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TiffAnalysisSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TiffAnalysisSettings:
    """Special nested class for casting TiffAnalysisSettings to subclasses."""

    __parent__: "TiffAnalysisSettings"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def tiff_analysis_settings(self: "CastSelf") -> "TiffAnalysisSettings":
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
class TiffAnalysisSettings(
    _1779.IndependentReportablePropertiesBase["TiffAnalysisSettings"]
):
    """TiffAnalysisSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TIFF_ANALYSIS_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def include_findley_analysis(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeFindleyAnalysis")

        if temp is None:
            return False

        return temp

    @include_findley_analysis.setter
    @exception_bridge
    @enforce_parameter_types
    def include_findley_analysis(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeFindleyAnalysis",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_residual_stresses(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeResidualStresses")

        if temp is None:
            return False

        return temp

    @include_residual_stresses.setter
    @exception_bridge
    @enforce_parameter_types
    def include_residual_stresses(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeResidualStresses",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_shot_peening(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeShotPeening")

        if temp is None:
            return False

        return temp

    @include_shot_peening.setter
    @exception_bridge
    @enforce_parameter_types
    def include_shot_peening(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeShotPeening",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def measured_residual_stress_profile_property(
        self: "Self",
    ) -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(
            self.wrapped, "MeasuredResidualStressProfileProperty"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @measured_residual_stress_profile_property.setter
    @exception_bridge
    @enforce_parameter_types
    def measured_residual_stress_profile_property(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "MeasuredResidualStressProfileProperty", value.wrapped
        )

    @property
    @exception_bridge
    def number_of_rotations_for_findley(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfRotationsForFindley")

        if temp is None:
            return 0

        return temp

    @number_of_rotations_for_findley.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_rotations_for_findley(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfRotationsForFindley",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def shot_peening_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShotPeeningDepth")

        if temp is None:
            return 0.0

        return temp

    @shot_peening_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def shot_peening_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShotPeeningDepth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def shot_peening_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShotPeeningFactor")

        if temp is None:
            return 0.0

        return temp

    @shot_peening_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def shot_peening_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShotPeeningFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def strain_at_mid_case_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StrainAtMidCaseDepth")

        if temp is None:
            return 0.0

        return temp

    @strain_at_mid_case_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def strain_at_mid_case_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StrainAtMidCaseDepth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def strain_at_surface(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StrainAtSurface")

        if temp is None:
            return 0.0

        return temp

    @strain_at_surface.setter
    @exception_bridge
    @enforce_parameter_types
    def strain_at_surface(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StrainAtSurface", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def core_material_properties(self: "Self") -> "_1161.HardenedMaterialProperties":
        """mastapy.gears.gear_designs.cylindrical.HardenedMaterialProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoreMaterialProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def surface_material_properties(self: "Self") -> "_1161.HardenedMaterialProperties":
        """mastapy.gears.gear_designs.cylindrical.HardenedMaterialProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceMaterialProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_TiffAnalysisSettings":
        """Cast to another type.

        Returns:
            _Cast_TiffAnalysisSettings
        """
        return _Cast_TiffAnalysisSettings(self)
