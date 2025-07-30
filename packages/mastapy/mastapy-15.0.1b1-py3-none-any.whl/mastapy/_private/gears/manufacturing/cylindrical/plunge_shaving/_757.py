"""RealPlungeShaverOutputs"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _754

_REAL_PLUNGE_SHAVER_OUTPUTS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving",
    "RealPlungeShaverOutputs",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical import _716
    from mastapy._private.gears.manufacturing.cylindrical.cutters import _813
    from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _748

    Self = TypeVar("Self", bound="RealPlungeShaverOutputs")
    CastSelf = TypeVar(
        "CastSelf", bound="RealPlungeShaverOutputs._Cast_RealPlungeShaverOutputs"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RealPlungeShaverOutputs",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RealPlungeShaverOutputs:
    """Special nested class for casting RealPlungeShaverOutputs to subclasses."""

    __parent__: "RealPlungeShaverOutputs"

    @property
    def plunge_shaver_outputs(self: "CastSelf") -> "_754.PlungeShaverOutputs":
        return self.__parent__._cast(_754.PlungeShaverOutputs)

    @property
    def real_plunge_shaver_outputs(self: "CastSelf") -> "RealPlungeShaverOutputs":
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
class RealPlungeShaverOutputs(_754.PlungeShaverOutputs):
    """RealPlungeShaverOutputs

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REAL_PLUNGE_SHAVER_OUTPUTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def highest_shaver_tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HighestShaverTipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lead_measurement_method(self: "Self") -> "_748.MicroGeometryDefinitionMethod":
        """mastapy.gears.manufacturing.cylindrical.plunge_shaving.MicroGeometryDefinitionMethod"""
        temp = pythonnet_property_get(self.wrapped, "LeadMeasurementMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving.MicroGeometryDefinitionMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._748",
            "MicroGeometryDefinitionMethod",
        )(value)

    @lead_measurement_method.setter
    @exception_bridge
    @enforce_parameter_types
    def lead_measurement_method(
        self: "Self", value: "_748.MicroGeometryDefinitionMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving.MicroGeometryDefinitionMethod",
        )
        pythonnet_property_set(self.wrapped, "LeadMeasurementMethod", value)

    @property
    @exception_bridge
    def lowest_shaver_tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowestShaverTipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def profile_measurement_method(
        self: "Self",
    ) -> "_748.MicroGeometryDefinitionMethod":
        """mastapy.gears.manufacturing.cylindrical.plunge_shaving.MicroGeometryDefinitionMethod"""
        temp = pythonnet_property_get(self.wrapped, "ProfileMeasurementMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving.MicroGeometryDefinitionMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.manufacturing.cylindrical.plunge_shaving._748",
            "MicroGeometryDefinitionMethod",
        )(value)

    @profile_measurement_method.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_measurement_method(
        self: "Self", value: "_748.MicroGeometryDefinitionMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving.MicroGeometryDefinitionMethod",
        )
        pythonnet_property_set(self.wrapped, "ProfileMeasurementMethod", value)

    @property
    @exception_bridge
    def specify_face_width(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyFaceWidth")

        if temp is None:
            return False

        return temp

    @specify_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_face_width(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyFaceWidth",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def left_flank_micro_geometry(
        self: "Self",
    ) -> "_716.CylindricalGearSpecifiedMicroGeometry":
        """mastapy.gears.manufacturing.cylindrical.CylindricalGearSpecifiedMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank_micro_geometry(
        self: "Self",
    ) -> "_716.CylindricalGearSpecifiedMicroGeometry":
        """mastapy.gears.manufacturing.cylindrical.CylindricalGearSpecifiedMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaver(self: "Self") -> "_813.CylindricalGearPlungeShaver":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearPlungeShaver

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shaver")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micro_geometry(
        self: "Self",
    ) -> "List[_716.CylindricalGearSpecifiedMicroGeometry]":
        """List[mastapy.gears.manufacturing.cylindrical.CylindricalGearSpecifiedMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroGeometry")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def calculate_micro_geometry(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateMicroGeometry")

    @exception_bridge
    def face_width_requires_calculation(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "FaceWidthRequiresCalculation")

    @property
    def cast_to(self: "Self") -> "_Cast_RealPlungeShaverOutputs":
        """Cast to another type.

        Returns:
            _Cast_RealPlungeShaverOutputs
        """
        return _Cast_RealPlungeShaverOutputs(self)
