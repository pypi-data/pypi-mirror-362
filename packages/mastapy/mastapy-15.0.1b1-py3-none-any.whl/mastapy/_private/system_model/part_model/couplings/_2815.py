"""BeltDrive"""

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
from mastapy._private.system_model.part_model import _2708

_BELT_DRIVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDrive"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import _2489
    from mastapy._private.system_model.part_model import _2659, _2698
    from mastapy._private.system_model.part_model.couplings import _2816, _2826, _2831

    Self = TypeVar("Self", bound="BeltDrive")
    CastSelf = TypeVar("CastSelf", bound="BeltDrive._Cast_BeltDrive")


__docformat__ = "restructuredtext en"
__all__ = ("BeltDrive",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BeltDrive:
    """Special nested class for casting BeltDrive to subclasses."""

    __parent__: "BeltDrive"

    @property
    def specialised_assembly(self: "CastSelf") -> "_2708.SpecialisedAssembly":
        return self.__parent__._cast(_2708.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2659

        return self.__parent__._cast(_2659.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def cvt(self: "CastSelf") -> "_2826.CVT":
        from mastapy._private.system_model.part_model.couplings import _2826

        return self.__parent__._cast(_2826.CVT)

    @property
    def belt_drive(self: "CastSelf") -> "BeltDrive":
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
class BeltDrive(_2708.SpecialisedAssembly):
    """BeltDrive

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BELT_DRIVE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def belt_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeltLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def belt_mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeltMass")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def belt_mass_per_unit_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BeltMassPerUnitLength")

        if temp is None:
            return 0.0

        return temp

    @belt_mass_per_unit_length.setter
    @exception_bridge
    @enforce_parameter_types
    def belt_mass_per_unit_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BeltMassPerUnitLength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pre_tension(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PreTension")

        if temp is None:
            return 0.0

        return temp

    @pre_tension.setter
    @exception_bridge
    @enforce_parameter_types
    def pre_tension(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PreTension", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def specify_stiffness_for_unit_length(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyStiffnessForUnitLength")

        if temp is None:
            return False

        return temp

    @specify_stiffness_for_unit_length.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_stiffness_for_unit_length(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyStiffnessForUnitLength",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Stiffness")

        if temp is None:
            return 0.0

        return temp

    @stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Stiffness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def stiffness_for_unit_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StiffnessForUnitLength")

        if temp is None:
            return 0.0

        return temp

    @stiffness_for_unit_length.setter
    @exception_bridge
    @enforce_parameter_types
    def stiffness_for_unit_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StiffnessForUnitLength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def type_of_belt(self: "Self") -> "_2816.BeltDriveType":
        """mastapy.system_model.part_model.couplings.BeltDriveType"""
        temp = pythonnet_property_get(self.wrapped, "TypeOfBelt")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PartModel.Couplings.BeltDriveType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model.couplings._2816", "BeltDriveType"
        )(value)

    @type_of_belt.setter
    @exception_bridge
    @enforce_parameter_types
    def type_of_belt(self: "Self", value: "_2816.BeltDriveType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PartModel.Couplings.BeltDriveType"
        )
        pythonnet_property_set(self.wrapped, "TypeOfBelt", value)

    @property
    @exception_bridge
    def belt_connections(self: "Self") -> "List[_2489.BeltConnection]":
        """List[mastapy.system_model.connections_and_sockets.BeltConnection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeltConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def pulleys(self: "Self") -> "List[_2831.Pulley]":
        """List[mastapy.system_model.part_model.couplings.Pulley]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Pulleys")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BeltDrive":
        """Cast to another type.

        Returns:
            _Cast_BeltDrive
        """
        return _Cast_BeltDrive(self)
