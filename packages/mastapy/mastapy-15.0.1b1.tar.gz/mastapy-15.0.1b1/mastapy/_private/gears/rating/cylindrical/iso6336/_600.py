"""CylindricalGearToothFatigueFractureResultsN1457"""

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

_CYLINDRICAL_GEAR_TOOTH_FATIGUE_FRACTURE_RESULTS_N1457 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "CylindricalGearToothFatigueFractureResultsN1457",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical.iso6336 import _618, _621
    from mastapy._private.utility_gui.charts import _2068

    Self = TypeVar("Self", bound="CylindricalGearToothFatigueFractureResultsN1457")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearToothFatigueFractureResultsN1457._Cast_CylindricalGearToothFatigueFractureResultsN1457",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearToothFatigueFractureResultsN1457",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearToothFatigueFractureResultsN1457:
    """Special nested class for casting CylindricalGearToothFatigueFractureResultsN1457 to subclasses."""

    __parent__: "CylindricalGearToothFatigueFractureResultsN1457"

    @property
    def cylindrical_gear_tooth_fatigue_fracture_results_n1457(
        self: "CastSelf",
    ) -> "CylindricalGearToothFatigueFractureResultsN1457":
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
class CylindricalGearToothFatigueFractureResultsN1457(_0.APIBase):
    """CylindricalGearToothFatigueFractureResultsN1457

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_TOOTH_FATIGUE_FRACTURE_RESULTS_N1457

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fatigue_damage_chart(self: "Self") -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueDamageChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def maximum_fatigue_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumFatigueDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def critical_section(self: "Self") -> "_621.ToothFlankFractureAnalysisRowN1457":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisRowN1457

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CriticalSection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_contact_point_a_section(
        self: "Self",
    ) -> "_621.ToothFlankFractureAnalysisRowN1457":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisRowN1457

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshContactPointASection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_contact_point_ab_section(
        self: "Self",
    ) -> "_618.ToothFlankFractureAnalysisContactPointN1457":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPointN1457

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshContactPointABSection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_contact_point_b_section(
        self: "Self",
    ) -> "_618.ToothFlankFractureAnalysisContactPointN1457":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPointN1457

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshContactPointBSection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_contact_point_c_section(
        self: "Self",
    ) -> "_618.ToothFlankFractureAnalysisContactPointN1457":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPointN1457

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshContactPointCSection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_contact_point_d_section(
        self: "Self",
    ) -> "_618.ToothFlankFractureAnalysisContactPointN1457":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPointN1457

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshContactPointDSection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_contact_point_de_section(
        self: "Self",
    ) -> "_618.ToothFlankFractureAnalysisContactPointN1457":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPointN1457

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshContactPointDESection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_contact_point_e_section(
        self: "Self",
    ) -> "_618.ToothFlankFractureAnalysisContactPointN1457":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPointN1457

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshContactPointESection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def analysis_rows(self: "Self") -> "List[_621.ToothFlankFractureAnalysisRowN1457]":
        """List[mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisRowN1457]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisRows")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_points(
        self: "Self",
    ) -> "List[_618.ToothFlankFractureAnalysisContactPointN1457]":
        """List[mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPointN1457]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CylindricalGearToothFatigueFractureResultsN1457":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearToothFatigueFractureResultsN1457
        """
        return _Cast_CylindricalGearToothFatigueFractureResultsN1457(self)
