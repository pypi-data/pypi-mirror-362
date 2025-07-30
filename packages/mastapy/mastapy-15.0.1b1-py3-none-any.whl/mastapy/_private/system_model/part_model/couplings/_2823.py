"""Coupling"""

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

_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Coupling"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2659, _2698
    from mastapy._private.system_model.part_model.couplings import (
        _2817,
        _2820,
        _2824,
        _2828,
        _2846,
        _2853,
    )

    Self = TypeVar("Self", bound="Coupling")
    CastSelf = TypeVar("CastSelf", bound="Coupling._Cast_Coupling")


__docformat__ = "restructuredtext en"
__all__ = ("Coupling",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Coupling:
    """Special nested class for casting Coupling to subclasses."""

    __parent__: "Coupling"

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
    def clutch(self: "CastSelf") -> "_2817.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2817

        return self.__parent__._cast(_2817.Clutch)

    @property
    def concept_coupling(self: "CastSelf") -> "_2820.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2820

        return self.__parent__._cast(_2820.ConceptCoupling)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2828.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2828

        return self.__parent__._cast(_2828.PartToPartShearCoupling)

    @property
    def spring_damper(self: "CastSelf") -> "_2846.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2846

        return self.__parent__._cast(_2846.SpringDamper)

    @property
    def torque_converter(self: "CastSelf") -> "_2853.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2853

        return self.__parent__._cast(_2853.TorqueConverter)

    @property
    def coupling(self: "CastSelf") -> "Coupling":
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
class Coupling(_2708.SpecialisedAssembly):
    """Coupling

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialStiffness")

        if temp is None:
            return 0.0

        return temp

    @axial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AxialStiffness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def radial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialStiffness")

        if temp is None:
            return 0.0

        return temp

    @radial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialStiffness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tilt_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltStiffness")

        if temp is None:
            return 0.0

        return temp

    @tilt_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltStiffness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def torsional_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TorsionalStiffness")

        if temp is None:
            return 0.0

        return temp

    @torsional_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def torsional_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TorsionalStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def halves(self: "Self") -> "List[_2824.CouplingHalf]":
        """List[mastapy.system_model.part_model.couplings.CouplingHalf]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Halves")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def half_a(self: "Self") -> "_2824.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HalfA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def half_b(self: "Self") -> "_2824.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HalfB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_Coupling":
        """Cast to another type.

        Returns:
            _Cast_Coupling
        """
        return _Cast_Coupling(self)
