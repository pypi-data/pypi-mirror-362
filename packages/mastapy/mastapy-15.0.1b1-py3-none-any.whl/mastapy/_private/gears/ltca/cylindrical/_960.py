"""CylindricalGearMeshLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._math.vector_2d import Vector2D
from mastapy._private.gears.ltca import _944

_CYLINDRICAL_GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Cylindrical", "CylindricalGearMeshLoadDistributionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1336, _1342, _1343
    from mastapy._private.gears.cylindrical import _1334
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1211
    from mastapy._private.gears.load_case.cylindrical import _987
    from mastapy._private.gears.ltca import _935
    from mastapy._private.gears.ltca.cylindrical import _964
    from mastapy._private.gears.rating.cylindrical import _549

    Self = TypeVar("Self", bound="CylindricalGearMeshLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshLoadDistributionAnalysis._Cast_CylindricalGearMeshLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshLoadDistributionAnalysis:
    """Special nested class for casting CylindricalGearMeshLoadDistributionAnalysis to subclasses."""

    __parent__: "CylindricalGearMeshLoadDistributionAnalysis"

    @property
    def gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_944.GearMeshLoadDistributionAnalysis":
        return self.__parent__._cast(_944.GearMeshLoadDistributionAnalysis)

    @property
    def gear_mesh_implementation_analysis(
        self: "CastSelf",
    ) -> "_1343.GearMeshImplementationAnalysis":
        from mastapy._private.gears.analysis import _1343

        return self.__parent__._cast(_1343.GearMeshImplementationAnalysis)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1342.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1342

        return self.__parent__._cast(_1342.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def cylindrical_gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "CylindricalGearMeshLoadDistributionAnalysis":
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
class CylindricalGearMeshLoadDistributionAnalysis(
    _944.GearMeshLoadDistributionAnalysis
):
    """CylindricalGearMeshLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def average_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def calculated_face_load_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedFaceLoadFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def din_scuffing_bulk_tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DINScuffingBulkToothTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso63362006_mesh_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO63362006MeshStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso63362006_mesh_stiffness_across_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO63362006MeshStiffnessAcrossFaceWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso63362006_single_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO63362006SingleStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso63362006_single_stiffness_across_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO63362006SingleStiffnessAcrossFaceWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso_scuffing_bulk_tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISOScuffingBulkToothTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_edge_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumEdgePressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_coefficient_of_friction_from_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanCoefficientOfFrictionFromLTCA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_lubrication_state_d_value_from_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanLubricationStateDValueFromLTCA"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_sliding_power_loss_from_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanSlidingPowerLossFromLTCA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_te(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanTE")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_efficiency_from_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshEfficiencyFromLTCA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Misalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peak_to_peak_te(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakToPeakTE")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def strip_loads_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StripLoadsDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def strip_loads_maximum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StripLoadsMaximum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def strip_loads_minimum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StripLoadsMinimum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def theoretical_total_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TheoreticalTotalContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def utilization_force_per_unit_length_cutoff_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UtilizationForcePerUnitLengthCutoffValue"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cylindrical_mesh_load_case(self: "Self") -> "_987.CylindricalMeshLoadCase":
        """mastapy.gears.load_case.cylindrical.CylindricalMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_a_in_mesh(
        self: "Self",
    ) -> "_935.CylindricalMeshedGearLoadDistributionAnalysis":
        """mastapy.gears.ltca.CylindricalMeshedGearLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearAInMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_b_in_mesh(
        self: "Self",
    ) -> "_935.CylindricalMeshedGearLoadDistributionAnalysis":
        """mastapy.gears.ltca.CylindricalMeshedGearLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBInMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_micro_geometry(self: "Self") -> "_1211.CylindricalGearMeshMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMeshMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def points_with_worst_results(self: "Self") -> "_1334.PointsWithWorstResults":
        """mastapy.gears.cylindrical.PointsWithWorstResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointsWithWorstResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rating(self: "Self") -> "_549.CylindricalGearMeshRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def load_distribution_analyses_at_single_rotation(
        self: "Self",
    ) -> "List[_964.CylindricalMeshLoadDistributionAtRotation]":
        """List[mastapy.gears.ltca.cylindrical.CylindricalMeshLoadDistributionAtRotation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadDistributionAnalysesAtSingleRotation"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshed_gears(
        self: "Self",
    ) -> "List[_935.CylindricalMeshedGearLoadDistributionAnalysis]":
        """List[mastapy.gears.ltca.CylindricalMeshedGearLoadDistributionAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def transmission_error_against_rotation(self: "Self") -> "List[Vector2D]":
        """List[Vector2D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmissionErrorAgainstRotation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector2D)

        if value is None:
            return None

        return value

    @exception_bridge
    def calculate_mesh_stiffness(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateMeshStiffness")

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshLoadDistributionAnalysis
        """
        return _Cast_CylindricalGearMeshLoadDistributionAnalysis(self)
