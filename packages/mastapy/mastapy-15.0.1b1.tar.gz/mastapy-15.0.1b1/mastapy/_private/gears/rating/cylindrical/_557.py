"""CylindricalMeshDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _456

_CYLINDRICAL_MESH_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalMeshDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.rating import _443
    from mastapy._private.gears.rating.cylindrical import _549

    Self = TypeVar("Self", bound="CylindricalMeshDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMeshDutyCycleRating._Cast_CylindricalMeshDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMeshDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMeshDutyCycleRating:
    """Special nested class for casting CylindricalMeshDutyCycleRating to subclasses."""

    __parent__: "CylindricalMeshDutyCycleRating"

    @property
    def mesh_duty_cycle_rating(self: "CastSelf") -> "_456.MeshDutyCycleRating":
        return self.__parent__._cast(_456.MeshDutyCycleRating)

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "_443.AbstractGearMeshRating":
        from mastapy._private.gears.rating import _443

        return self.__parent__._cast(_443.AbstractGearMeshRating)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def cylindrical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "CylindricalMeshDutyCycleRating":
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
class CylindricalMeshDutyCycleRating(_456.MeshDutyCycleRating):
    """CylindricalMeshDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MESH_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_nominal_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNominalAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_nominal_tangential_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNominalTangentialLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_radial_separating_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumRadialSeparatingLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def micropitting_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicropittingSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permanent_deformation_safety_factor_step_1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermanentDeformationSafetyFactorStep1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permanent_deformation_safety_factor_step_2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermanentDeformationSafetyFactorStep2"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_load_safety_factor_integral_temperature_method(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingLoadSafetyFactorIntegralTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_safety_factor_flash_temperature_method(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorFlashTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_safety_factor_integral_temperature_method(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorIntegralTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def highest_torque_load_case(self: "Self") -> "_549.CylindricalGearMeshRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HighestTorqueLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_mesh_ratings(
        self: "Self",
    ) -> "List[_549.CylindricalGearMeshRating]":
        """List[mastapy.gears.rating.cylindrical.CylindricalGearMeshRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def loaded_cylindrical_mesh_ratings(
        self: "Self",
    ) -> "List[_549.CylindricalGearMeshRating]":
        """List[mastapy.gears.rating.cylindrical.CylindricalGearMeshRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedCylindricalMeshRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalMeshDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMeshDutyCycleRating
        """
        return _Cast_CylindricalMeshDutyCycleRating(self)
