"""ShaftMaterial"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.materials import _358

_SHAFT_MATERIAL = python_net_import("SMT.MastaAPI.Shafts", "ShaftMaterial")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials import _335
    from mastapy._private.shafts import _6
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="ShaftMaterial")
    CastSelf = TypeVar("CastSelf", bound="ShaftMaterial._Cast_ShaftMaterial")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftMaterial:
    """Special nested class for casting ShaftMaterial to subclasses."""

    __parent__: "ShaftMaterial"

    @property
    def material(self: "CastSelf") -> "_358.Material":
        return self.__parent__._cast(_358.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def shaft_material(self: "CastSelf") -> "ShaftMaterial":
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
class ShaftMaterial(_358.Material):
    """ShaftMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def hardening_type_for_agma60016101e08(self: "Self") -> "_6.AGMAHardeningType":
        """mastapy.shafts.AGMAHardeningType"""
        temp = pythonnet_property_get(self.wrapped, "HardeningTypeForAGMA60016101E08")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Shafts.AGMAHardeningType")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._6", "AGMAHardeningType"
        )(value)

    @hardening_type_for_agma60016101e08.setter
    @exception_bridge
    @enforce_parameter_types
    def hardening_type_for_agma60016101e08(
        self: "Self", value: "_6.AGMAHardeningType"
    ) -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Shafts.AGMAHardeningType")
        pythonnet_property_set(self.wrapped, "HardeningTypeForAGMA60016101E08", value)

    @property
    @exception_bridge
    def specified_endurance_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedEnduranceLimit")

        if temp is None:
            return 0.0

        return temp

    @specified_endurance_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_endurance_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedEnduranceLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_custom_sn_curve(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseCustomSNCurve")

        if temp is None:
            return False

        return temp

    @use_custom_sn_curve.setter
    @exception_bridge
    @enforce_parameter_types
    def use_custom_sn_curve(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseCustomSNCurve",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def bh_curve_specification(self: "Self") -> "_335.BHCurveSpecification":
        """mastapy.materials.BHCurveSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BHCurveSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftMaterial":
        """Cast to another type.

        Returns:
            _Cast_ShaftMaterial
        """
        return _Cast_ShaftMaterial(self)
