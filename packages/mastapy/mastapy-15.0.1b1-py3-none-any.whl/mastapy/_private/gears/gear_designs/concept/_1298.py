"""ConceptGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _1054

_CONCEPT_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Concept", "ConceptGearSetDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1052
    from mastapy._private.gears.gear_designs.concept import _1296, _1297

    Self = TypeVar("Self", bound="ConceptGearSetDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="ConceptGearSetDesign._Cast_ConceptGearSetDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearSetDesign:
    """Special nested class for casting ConceptGearSetDesign to subclasses."""

    __parent__: "ConceptGearSetDesign"

    @property
    def gear_set_design(self: "CastSelf") -> "_1054.GearSetDesign":
        return self.__parent__._cast(_1054.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def concept_gear_set_design(self: "CastSelf") -> "ConceptGearSetDesign":
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
class ConceptGearSetDesign(_1054.GearSetDesign):
    """ConceptGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def working_normal_pressure_angle_gear_a_concave_flank(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "WorkingNormalPressureAngleGearAConcaveFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @working_normal_pressure_angle_gear_a_concave_flank.setter
    @exception_bridge
    @enforce_parameter_types
    def working_normal_pressure_angle_gear_a_concave_flank(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "WorkingNormalPressureAngleGearAConcaveFlank",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def working_normal_pressure_angle_gear_a_convex_flank(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "WorkingNormalPressureAngleGearAConvexFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @working_normal_pressure_angle_gear_a_convex_flank.setter
    @exception_bridge
    @enforce_parameter_types
    def working_normal_pressure_angle_gear_a_convex_flank(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "WorkingNormalPressureAngleGearAConvexFlank",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def gears(self: "Self") -> "List[_1296.ConceptGearDesign]":
        """List[mastapy.gears.gear_designs.concept.ConceptGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    @exception_bridge
    def concept_meshes(self: "Self") -> "List[_1297.ConceptGearMeshDesign]":
        """List[mastapy.gears.gear_designs.concept.ConceptGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearSetDesign
        """
        return _Cast_ConceptGearSetDesign(self)
