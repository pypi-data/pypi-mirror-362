"""CylindricalMisalignmentCalculator"""

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
from mastapy._private._math.vector_3d import Vector3D

_CYLINDRICAL_MISALIGNMENT_CALCULATOR = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "CylindricalMisalignmentCalculator"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalMisalignmentCalculator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMisalignmentCalculator._Cast_CylindricalMisalignmentCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMisalignmentCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMisalignmentCalculator:
    """Special nested class for casting CylindricalMisalignmentCalculator to subclasses."""

    __parent__: "CylindricalMisalignmentCalculator"

    @property
    def cylindrical_misalignment_calculator(
        self: "CastSelf",
    ) -> "CylindricalMisalignmentCalculator":
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
class CylindricalMisalignmentCalculator(_0.APIBase):
    """CylindricalMisalignmentCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MISALIGNMENT_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_a_equivalent_misalignment_for_rating(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearAEquivalentMisalignmentForRating"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_line_fit_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearALineFitMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_line_fit_misalignment_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearALineFitMisalignmentAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_radial_angular_component_of_rigid_body_misalignment(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearARadialAngularComponentOfRigidBodyMisalignment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_rigid_body_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearARigidBodyMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_rigid_body_misalignment_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearARigidBodyMisalignmentAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_rigid_body_out_of_plane_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearARigidBodyOutOfPlaneMisalignment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_rigid_body_out_of_plane_misalignment_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearARigidBodyOutOfPlaneMisalignmentAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_single_node_misalignment_angle_due_to_tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearASingleNodeMisalignmentAngleDueToTilt"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_single_node_misalignment_due_to_tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearASingleNodeMisalignmentDueToTilt"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_single_node_misalignment_due_to_twist(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearASingleNodeMisalignmentDueToTwist"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_tangential_angular_component_of_rigid_body_misalignment(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearATangentialAngularComponentOfRigidBodyMisalignment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_transverse_separations(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearATransverseSeparations")

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_b_equivalent_misalignment_for_rating(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBEquivalentMisalignmentForRating"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_line_fit_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBLineFitMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_line_fit_misalignment_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBLineFitMisalignmentAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_radial_angular_component_of_rigid_body_misalignment(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBRadialAngularComponentOfRigidBodyMisalignment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_rigid_body_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBRigidBodyMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_rigid_body_misalignment_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBRigidBodyMisalignmentAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_rigid_body_out_of_plane_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBRigidBodyOutOfPlaneMisalignment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_rigid_body_out_of_plane_misalignment_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBRigidBodyOutOfPlaneMisalignmentAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_single_node_misalignment_angle_due_to_tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBSingleNodeMisalignmentAngleDueToTilt"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_single_node_misalignment_due_to_tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBSingleNodeMisalignmentDueToTilt"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_single_node_misalignment_due_to_twist(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBSingleNodeMisalignmentDueToTwist"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_tangential_angular_component_of_rigid_body_misalignment(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBTangentialAngularComponentOfRigidBodyMisalignment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_b_transverse_separations(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBTransverseSeparations")

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def total_equivalent_misalignment_for_rating(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalEquivalentMisalignmentForRating"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_line_fit_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalLineFitMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_line_fit_misalignment_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalLineFitMisalignmentAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_radial_angular_component_of_rigid_body_misalignment(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalRadialAngularComponentOfRigidBodyMisalignment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_rigid_body_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalRigidBodyMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_rigid_body_misalignment_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalRigidBodyMisalignmentAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_rigid_body_out_of_plane_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalRigidBodyOutOfPlaneMisalignment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_rigid_body_out_of_plane_misalignment_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalRigidBodyOutOfPlaneMisalignmentAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_single_node_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalSingleNodeMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_single_node_misalignment_angle_due_to_tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalSingleNodeMisalignmentAngleDueToTilt"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_single_node_misalignment_due_to_tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalSingleNodeMisalignmentDueToTilt"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_single_node_misalignment_due_to_twist(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalSingleNodeMisalignmentDueToTwist"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_tangential_angular_component_of_rigid_body_misalignment(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalTangentialAngularComponentOfRigidBodyMisalignment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rigid_body_coordinate_system_x_axis(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RigidBodyCoordinateSystemXAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def rigid_body_coordinate_system_y_axis(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RigidBodyCoordinateSystemYAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalMisalignmentCalculator":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMisalignmentCalculator
        """
        return _Cast_CylindricalMisalignmentCalculator(self)
