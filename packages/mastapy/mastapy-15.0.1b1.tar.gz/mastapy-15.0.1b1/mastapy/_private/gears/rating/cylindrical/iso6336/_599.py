"""CylindricalGearToothFatigueFractureResults"""

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

_CYLINDRICAL_GEAR_TOOTH_FATIGUE_FRACTURE_RESULTS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "CylindricalGearToothFatigueFractureResults",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical.iso6336 import _615

    Self = TypeVar("Self", bound="CylindricalGearToothFatigueFractureResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearToothFatigueFractureResults._Cast_CylindricalGearToothFatigueFractureResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearToothFatigueFractureResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearToothFatigueFractureResults:
    """Special nested class for casting CylindricalGearToothFatigueFractureResults to subclasses."""

    __parent__: "CylindricalGearToothFatigueFractureResults"

    @property
    def cylindrical_gear_tooth_fatigue_fracture_results(
        self: "CastSelf",
    ) -> "CylindricalGearToothFatigueFractureResults":
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
class CylindricalGearToothFatigueFractureResults(_0.APIBase):
    """CylindricalGearToothFatigueFractureResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_TOOTH_FATIGUE_FRACTURE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_material_exposure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumMaterialExposure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def witzigs_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WitzigsSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def critical_section(self: "Self") -> "_615.ToothFlankFractureAnalysisContactPoint":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPoint

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
    ) -> "_615.ToothFlankFractureAnalysisContactPoint":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPoint

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
    ) -> "_615.ToothFlankFractureAnalysisContactPoint":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPoint

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
    ) -> "_615.ToothFlankFractureAnalysisContactPoint":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPoint

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
    ) -> "_615.ToothFlankFractureAnalysisContactPoint":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPoint

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
    ) -> "_615.ToothFlankFractureAnalysisContactPoint":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPoint

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
    ) -> "_615.ToothFlankFractureAnalysisContactPoint":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPoint

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
    ) -> "_615.ToothFlankFractureAnalysisContactPoint":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPoint

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
    def analysis_rows(
        self: "Self",
    ) -> "List[_615.ToothFlankFractureAnalysisContactPoint]":
        """List[mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPoint]

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
    def cast_to(self: "Self") -> "_Cast_CylindricalGearToothFatigueFractureResults":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearToothFatigueFractureResults
        """
        return _Cast_CylindricalGearToothFatigueFractureResults(self)
