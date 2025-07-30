"""BoltMaterial"""

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
from mastapy._private.bolts import _1651

_BOLT_MATERIAL = python_net_import("SMT.MastaAPI.Bolts", "BoltMaterial")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bolts import _1670
    from mastapy._private.materials import _358
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="BoltMaterial")
    CastSelf = TypeVar("CastSelf", bound="BoltMaterial._Cast_BoltMaterial")


__docformat__ = "restructuredtext en"
__all__ = ("BoltMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BoltMaterial:
    """Special nested class for casting BoltMaterial to subclasses."""

    __parent__: "BoltMaterial"

    @property
    def bolted_joint_material(self: "CastSelf") -> "_1651.BoltedJointMaterial":
        return self.__parent__._cast(_1651.BoltedJointMaterial)

    @property
    def material(self: "CastSelf") -> "_358.Material":
        from mastapy._private.materials import _358

        return self.__parent__._cast(_358.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def bolt_material(self: "CastSelf") -> "BoltMaterial":
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
class BoltMaterial(_1651.BoltedJointMaterial):
    """BoltMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BOLT_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def minimum_tensile_strength(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumTensileStrength")

        if temp is None:
            return 0.0

        return temp

    @minimum_tensile_strength.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_tensile_strength(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumTensileStrength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def proof_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProofStress")

        if temp is None:
            return 0.0

        return temp

    @proof_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def proof_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ProofStress", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def shearing_strength(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShearingStrength")

        if temp is None:
            return 0.0

        return temp

    @shearing_strength.setter
    @exception_bridge
    @enforce_parameter_types
    def shearing_strength(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShearingStrength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def strength_grade(self: "Self") -> "_1670.StrengthGrades":
        """mastapy.bolts.StrengthGrades"""
        temp = pythonnet_property_get(self.wrapped, "StrengthGrade")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bolts.StrengthGrades")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bolts._1670", "StrengthGrades"
        )(value)

    @strength_grade.setter
    @exception_bridge
    @enforce_parameter_types
    def strength_grade(self: "Self", value: "_1670.StrengthGrades") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Bolts.StrengthGrades")
        pythonnet_property_set(self.wrapped, "StrengthGrade", value)

    @property
    def cast_to(self: "Self") -> "_Cast_BoltMaterial":
        """Cast to another type.

        Returns:
            _Cast_BoltMaterial
        """
        return _Cast_BoltMaterial(self)
