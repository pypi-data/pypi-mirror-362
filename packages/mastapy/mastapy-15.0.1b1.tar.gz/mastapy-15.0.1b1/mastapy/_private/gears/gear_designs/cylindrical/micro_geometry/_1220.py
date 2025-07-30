"""CylindricalGearSetMicroGeometry"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears import _408
from mastapy._private.gears.analysis import _1351

_CYLINDRICAL_GEAR_SET_MICRO_GEOMETRY = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearSetMicroGeometry",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.analysis import _1337, _1346
    from mastapy._private.gears.gear_designs.cylindrical import _1122, _1138, _1151
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1211,
        _1214,
    )

    Self = TypeVar("Self", bound="CylindricalGearSetMicroGeometry")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetMicroGeometry._Cast_CylindricalGearSetMicroGeometry",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetMicroGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetMicroGeometry:
    """Special nested class for casting CylindricalGearSetMicroGeometry to subclasses."""

    __parent__: "CylindricalGearSetMicroGeometry"

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1351.GearSetImplementationDetail":
        return self.__parent__._cast(_1351.GearSetImplementationDetail)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1346.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1346

        return self.__parent__._cast(_1346.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

    @property
    def cylindrical_gear_set_micro_geometry(
        self: "CastSelf",
    ) -> "CylindricalGearSetMicroGeometry":
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
class CylindricalGearSetMicroGeometry(_1351.GearSetImplementationDetail):
    """CylindricalGearSetMicroGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_MICRO_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def coefficient_of_friction_method_for_ltca(
        self: "Self",
    ) -> "overridable.Overridable_CoefficientOfFrictionCalculationMethod":
        """Overridable[mastapy.gears.CoefficientOfFrictionCalculationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionMethodForLTCA"
        )

        if temp is None:
            return None

        value = overridable.Overridable_CoefficientOfFrictionCalculationMethod.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @coefficient_of_friction_method_for_ltca.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction_method_for_ltca(
        self: "Self",
        value: "Union[_408.CoefficientOfFrictionCalculationMethod, Tuple[_408.CoefficientOfFrictionCalculationMethod, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_CoefficientOfFrictionCalculationMethod.wrapper_type()
        enclosed_type = overridable.Overridable_CoefficientOfFrictionCalculationMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "CoefficientOfFrictionMethodForLTCA", value
        )

    @property
    @exception_bridge
    def coefficient_of_friction_for_boundary_lubrication(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionForBoundaryLubrication"
        )

        if temp is None:
            return 0.0

        return temp

    @coefficient_of_friction_for_boundary_lubrication.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction_for_boundary_lubrication(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoefficientOfFrictionForBoundaryLubrication",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def coefficient_of_friction_for_fluid_film_lubrication(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionForFluidFilmLubrication"
        )

        if temp is None:
            return 0.0

        return temp

    @coefficient_of_friction_for_fluid_film_lubrication.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction_for_fluid_film_lubrication(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoefficientOfFrictionForFluidFilmLubrication",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def cylindrical_gear_set_design(self: "Self") -> "_1138.CylindricalGearSetDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_micro_geometries(
        self: "Self",
    ) -> "List[_1214.CylindricalGearMicroGeometryBase]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMicroGeometryBase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearMicroGeometries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_mesh_micro_geometries(
        self: "Self",
    ) -> "List[_1211.CylindricalGearMeshMicroGeometry]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMeshMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshMicroGeometries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def duplicate(self: "Self") -> "CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry"""
        method_result = pythonnet_method_call(self.wrapped, "Duplicate")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def duplicate_and_add_to(
        self: "Self", gear_set_design: "_1138.CylindricalGearSetDesign"
    ) -> "CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry

        Args:
            gear_set_design (mastapy.gears.gear_designs.cylindrical.CylindricalGearSetDesign)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "DuplicateAndAddTo",
            gear_set_design.wrapped if gear_set_design else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def duplicate_specifying_separate_micro_geometry_for_each_planet(
        self: "Self",
    ) -> "_1351.GearSetImplementationDetail":
        """mastapy.gears.analysis.GearSetImplementationDetail"""
        method_result = pythonnet_method_call(
            self.wrapped, "DuplicateSpecifyingSeparateMicroGeometryForEachPlanet"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def duplicate_specifying_separate_micro_geometry_for_each_planet_and_add_to(
        self: "Self", gear_set_design: "_1151.CylindricalPlanetaryGearSetDesign"
    ) -> "_1351.GearSetImplementationDetail":
        """mastapy.gears.analysis.GearSetImplementationDetail

        Args:
            gear_set_design (mastapy.gears.gear_designs.cylindrical.CylindricalPlanetaryGearSetDesign)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "DuplicateSpecifyingSeparateMicroGeometryForEachPlanetAndAddTo",
            gear_set_design.wrapped if gear_set_design else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def duplicate_specifying_separate_micro_geometry_for_each_tooth(
        self: "Self",
    ) -> "CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry"""
        method_result = pythonnet_method_call(
            self.wrapped, "DuplicateSpecifyingSeparateMicroGeometryForEachTooth"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def duplicate_specifying_separate_micro_geometry_for_each_tooth_for(
        self: "Self", gears: "List[_1122.CylindricalGearDesign]"
    ) -> "CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry

        Args:
            gears (List[mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign])
        """
        gears = conversion.mp_to_pn_objects_in_dotnet_list(gears)
        method_result = pythonnet_method_call(
            self.wrapped,
            "DuplicateSpecifyingSeparateMicroGeometryForEachToothFor",
            gears,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetMicroGeometry":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetMicroGeometry
        """
        return _Cast_CylindricalGearSetMicroGeometry(self)
