"""CylindricalGearMeshFlankDesign"""

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

_CYLINDRICAL_GEAR_MESH_FLANK_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearMeshFlankDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="CylindricalGearMeshFlankDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshFlankDesign._Cast_CylindricalGearMeshFlankDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshFlankDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshFlankDesign:
    """Special nested class for casting CylindricalGearMeshFlankDesign to subclasses."""

    __parent__: "CylindricalGearMeshFlankDesign"

    @property
    def cylindrical_gear_mesh_flank_design(
        self: "CastSelf",
    ) -> "CylindricalGearMeshFlankDesign":
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
class CylindricalGearMeshFlankDesign(_0.APIBase):
    """CylindricalGearMeshFlankDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_FLANK_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def degree_of_tooth_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DegreeOfToothLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def flank_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlankName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def iso14179_part_2_tooth_loss_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO14179Part2ToothLossFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def specific_sliding_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpecificSlidingChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sum_of_base_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SumOfBaseRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def virtual_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def working_normal_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingNormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def working_transverse_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingTransversePressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshFlankDesign":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshFlankDesign
        """
        return _Cast_CylindricalGearMeshFlankDesign(self)
