"""ConicalMeshedGearLoadDistributionAnalysis"""

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

_CONICAL_MESHED_GEAR_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Conical", "ConicalMeshedGearLoadDistributionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.cylindrical import _1332, _1333
    from mastapy._private.gears.ltca.conical import _970

    Self = TypeVar("Self", bound="ConicalMeshedGearLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshedGearLoadDistributionAnalysis._Cast_ConicalMeshedGearLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshedGearLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshedGearLoadDistributionAnalysis:
    """Special nested class for casting ConicalMeshedGearLoadDistributionAnalysis to subclasses."""

    __parent__: "ConicalMeshedGearLoadDistributionAnalysis"

    @property
    def conical_meshed_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "ConicalMeshedGearLoadDistributionAnalysis":
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
class ConicalMeshedGearLoadDistributionAnalysis(_0.APIBase):
    """ConicalMeshedGearLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESHED_GEAR_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def estimated_gear_stiffness_from_fe_model(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EstimatedGearStiffnessFromFEModel")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def max_tensile_principal_root_stress_compression_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaxTensilePrincipalRootStressCompressionSide"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def max_tensile_principal_root_stress_tension_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaxTensilePrincipalRootStressTensionSide"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_von_mises_root_stress_compression_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumVonMisesRootStressCompressionSide"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_von_mises_root_stress_tension_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumVonMisesRootStressTensionSide"
        )

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
    def torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Torque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_charts(self: "Self") -> "_1333.GearLTCAContactCharts":
        """mastapy.gears.cylindrical.GearLTCAContactCharts

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactCharts")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_charts_as_text_file(
        self: "Self",
    ) -> "_1332.GearLTCAContactChartDataAsTextFile":
        """mastapy.gears.cylindrical.GearLTCAContactChartDataAsTextFile

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactChartsAsTextFile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_load_distribution_analysis(
        self: "Self",
    ) -> "_970.ConicalGearLoadDistributionAnalysis":
        """mastapy.gears.ltca.conical.ConicalGearLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearLoadDistributionAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshedGearLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshedGearLoadDistributionAnalysis
        """
        return _Cast_ConicalMeshedGearLoadDistributionAnalysis(self)
