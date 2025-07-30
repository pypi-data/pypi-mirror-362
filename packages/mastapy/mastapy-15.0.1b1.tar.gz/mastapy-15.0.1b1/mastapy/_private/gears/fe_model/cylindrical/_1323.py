"""CylindricalGearSetFEModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.fe_model import _1320

_CYLINDRICAL_GEAR_SET_FE_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.FEModel.Cylindrical", "CylindricalGearSetFEModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1337, _1346, _1351
    from mastapy._private.gears.gear_designs.cylindrical import _1141

    Self = TypeVar("Self", bound="CylindricalGearSetFEModel")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearSetFEModel._Cast_CylindricalGearSetFEModel"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetFEModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetFEModel:
    """Special nested class for casting CylindricalGearSetFEModel to subclasses."""

    __parent__: "CylindricalGearSetFEModel"

    @property
    def gear_set_fe_model(self: "CastSelf") -> "_1320.GearSetFEModel":
        return self.__parent__._cast(_1320.GearSetFEModel)

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1351.GearSetImplementationDetail":
        from mastapy._private.gears.analysis import _1351

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
    def cylindrical_gear_set_fe_model(self: "CastSelf") -> "CylindricalGearSetFEModel":
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
class CylindricalGearSetFEModel(_1320.GearSetFEModel):
    """CylindricalGearSetFEModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_FE_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_coupled_teeth_either_side(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCoupledTeethEitherSide")

        if temp is None:
            return 0

        return temp

    @number_of_coupled_teeth_either_side.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_coupled_teeth_either_side(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfCoupledTeethEitherSide",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def remove_local_compressive_stress_due_to_applied_point_load_from_root_stress(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "RemoveLocalCompressiveStressDueToAppliedPointLoadFromRootStress",
        )

        if temp is None:
            return False

        return temp

    @remove_local_compressive_stress_due_to_applied_point_load_from_root_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def remove_local_compressive_stress_due_to_applied_point_load_from_root_stress(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RemoveLocalCompressiveStressDueToAppliedPointLoadFromRootStress",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_manufactured_profile_shape(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseManufacturedProfileShape")

        if temp is None:
            return False

        return temp

    @use_manufactured_profile_shape.setter
    @exception_bridge
    @enforce_parameter_types
    def use_manufactured_profile_shape(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseManufacturedProfileShape",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def manufacturing_configuration_selection(
        self: "Self",
    ) -> "_1141.CylindricalGearSetManufacturingConfigurationSelection":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetManufacturingConfigurationSelection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ManufacturingConfigurationSelection"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetFEModel":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetFEModel
        """
        return _Cast_CylindricalGearSetFEModel(self)
