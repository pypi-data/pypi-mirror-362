"""CylindricalPlanetGearDesign"""

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
from mastapy._private.gears.gear_designs.cylindrical import _1122

_CYLINDRICAL_PLANET_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalPlanetGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _430
    from mastapy._private.gears.gear_designs import _1051, _1052
    from mastapy._private.gears.gear_designs.cylindrical import _1175, _1176
    from mastapy._private.geometry.two_d import _401

    Self = TypeVar("Self", bound="CylindricalPlanetGearDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalPlanetGearDesign._Cast_CylindricalPlanetGearDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalPlanetGearDesign:
    """Special nested class for casting CylindricalPlanetGearDesign to subclasses."""

    __parent__: "CylindricalPlanetGearDesign"

    @property
    def cylindrical_gear_design(self: "CastSelf") -> "_1122.CylindricalGearDesign":
        return self.__parent__._cast(_1122.CylindricalGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "_1051.GearDesign":
        from mastapy._private.gears.gear_designs import _1051

        return self.__parent__._cast(_1051.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def cylindrical_planet_gear_design(
        self: "CastSelf",
    ) -> "CylindricalPlanetGearDesign":
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
class CylindricalPlanetGearDesign(_1122.CylindricalGearDesign):
    """CylindricalPlanetGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_PLANET_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def has_factorising_annulus(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasFactorisingAnnulus")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def has_factorising_sun(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasFactorisingSun")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def internal_external(self: "Self") -> "_401.InternalExternalType":
        """mastapy.geometry.two_d.InternalExternalType"""
        temp = pythonnet_property_get(self.wrapped, "InternalExternal")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Geometry.TwoD.InternalExternalType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.geometry.two_d._401", "InternalExternalType"
        )(value)

    @internal_external.setter
    @exception_bridge
    @enforce_parameter_types
    def internal_external(self: "Self", value: "_401.InternalExternalType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Geometry.TwoD.InternalExternalType"
        )
        pythonnet_property_set(self.wrapped, "InternalExternal", value)

    @property
    @exception_bridge
    def suggested_maximum_number_of_planets(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SuggestedMaximumNumberOfPlanets")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def planetary_details(self: "Self") -> "_430.PlanetaryDetail":
        """mastapy.gears.PlanetaryDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetaryDetails")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def planet_assembly_indices(self: "Self") -> "List[_1175.NamedPlanetAssemblyIndex]":
        """List[mastapy.gears.gear_designs.cylindrical.NamedPlanetAssemblyIndex]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetAssemblyIndices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def planetary_sidebands_amplitude_factors(
        self: "Self",
    ) -> "List[_1176.NamedPlanetSideBandAmplitudeFactor]":
        """List[mastapy.gears.gear_designs.cylindrical.NamedPlanetSideBandAmplitudeFactor]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PlanetarySidebandsAmplitudeFactors"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalPlanetGearDesign":
        """Cast to another type.

        Returns:
            _Cast_CylindricalPlanetGearDesign
        """
        return _Cast_CylindricalPlanetGearDesign(self)
