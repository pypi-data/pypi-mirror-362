"""SplineMaterial"""

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

_SPLINE_MATERIAL = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "SplineMaterial"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors.splines import _1583
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="SplineMaterial")
    CastSelf = TypeVar("CastSelf", bound="SplineMaterial._Cast_SplineMaterial")


__docformat__ = "restructuredtext en"
__all__ = ("SplineMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SplineMaterial:
    """Special nested class for casting SplineMaterial to subclasses."""

    __parent__: "SplineMaterial"

    @property
    def material(self: "CastSelf") -> "_358.Material":
        return self.__parent__._cast(_358.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def spline_material(self: "CastSelf") -> "SplineMaterial":
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
class SplineMaterial(_358.Material):
    """SplineMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPLINE_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def core_hardness_h_rc(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CoreHardnessHRc")

        if temp is None:
            return 0.0

        return temp

    @core_hardness_h_rc.setter
    @exception_bridge
    @enforce_parameter_types
    def core_hardness_h_rc(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CoreHardnessHRc", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def heat_treatment_type(self: "Self") -> "_1583.HeatTreatmentTypes":
        """mastapy.detailed_rigid_connectors.splines.HeatTreatmentTypes"""
        temp = pythonnet_property_get(self.wrapped, "HeatTreatmentType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.DetailedRigidConnectors.Splines.HeatTreatmentTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.splines._1583",
            "HeatTreatmentTypes",
        )(value)

    @heat_treatment_type.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_treatment_type(self: "Self", value: "_1583.HeatTreatmentTypes") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.DetailedRigidConnectors.Splines.HeatTreatmentTypes"
        )
        pythonnet_property_set(self.wrapped, "HeatTreatmentType", value)

    @property
    def cast_to(self: "Self") -> "_Cast_SplineMaterial":
        """Cast to another type.

        Returns:
            _Cast_SplineMaterial
        """
        return _Cast_SplineMaterial(self)
