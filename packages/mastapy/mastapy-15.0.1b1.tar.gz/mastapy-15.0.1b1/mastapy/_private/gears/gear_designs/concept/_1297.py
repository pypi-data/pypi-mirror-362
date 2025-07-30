"""ConceptGearMeshDesign"""

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
from mastapy._private.gears.gear_designs import _1053

_CONCEPT_GEAR_MESH_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Concept", "ConceptGearMeshDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1052
    from mastapy._private.gears.gear_designs.concept import _1296, _1298

    Self = TypeVar("Self", bound="ConceptGearMeshDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="ConceptGearMeshDesign._Cast_ConceptGearMeshDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearMeshDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearMeshDesign:
    """Special nested class for casting ConceptGearMeshDesign to subclasses."""

    __parent__: "ConceptGearMeshDesign"

    @property
    def gear_mesh_design(self: "CastSelf") -> "_1053.GearMeshDesign":
        return self.__parent__._cast(_1053.GearMeshDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def concept_gear_mesh_design(self: "CastSelf") -> "ConceptGearMeshDesign":
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
class ConceptGearMeshDesign(_1053.GearMeshDesign):
    """ConceptGearMeshDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_MESH_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    @exception_bridge
    @enforce_parameter_types
    def offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Offset", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def shaft_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftAngle")

        if temp is None:
            return 0.0

        return temp

    @shaft_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShaftAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def concept_gear_set(self: "Self") -> "_1298.ConceptGearSetDesign":
        """mastapy.gears.gear_designs.concept.ConceptGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptGearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def concept_gears(self: "Self") -> "List[_1296.ConceptGearDesign]":
        """List[mastapy.gears.gear_designs.concept.ConceptGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearMeshDesign":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearMeshDesign
        """
        return _Cast_ConceptGearMeshDesign(self)
