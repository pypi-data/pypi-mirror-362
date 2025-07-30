"""CouplingHalf"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2693

_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2698
    from mastapy._private.system_model.part_model.couplings import (
        _2818,
        _2821,
        _2827,
        _2829,
        _2831,
        _2838,
        _2847,
        _2850,
        _2851,
        _2852,
        _2854,
        _2856,
    )

    Self = TypeVar("Self", bound="CouplingHalf")
    CastSelf = TypeVar("CastSelf", bound="CouplingHalf._Cast_CouplingHalf")


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalf",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalf:
    """Special nested class for casting CouplingHalf to subclasses."""

    __parent__: "CouplingHalf"

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
        return self.__parent__._cast(_2693.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        from mastapy._private.system_model.part_model import _2670

        return self.__parent__._cast(_2670.Component)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def clutch_half(self: "CastSelf") -> "_2818.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2818

        return self.__parent__._cast(_2818.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2821.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2821

        return self.__parent__._cast(_2821.ConceptCouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2827.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2827

        return self.__parent__._cast(_2827.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2829.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2829

        return self.__parent__._cast(_2829.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2831.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2831

        return self.__parent__._cast(_2831.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2838.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2838

        return self.__parent__._cast(_2838.RollingRing)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2847.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2847

        return self.__parent__._cast(_2847.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2850.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2850

        return self.__parent__._cast(_2850.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2851.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2851

        return self.__parent__._cast(_2851.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2852.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2852

        return self.__parent__._cast(_2852.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2854.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2854

        return self.__parent__._cast(_2854.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2856.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2856

        return self.__parent__._cast(_2856.TorqueConverterTurbine)

    @property
    def coupling_half(self: "CastSelf") -> "CouplingHalf":
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
class CouplingHalf(_2693.MountableComponent):
    """CouplingHalf

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bore(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bore.setter
    @exception_bridge
    @enforce_parameter_types
    def bore(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Bore", value)

    @property
    @exception_bridge
    def diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Diameter", value)

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalf":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalf
        """
        return _Cast_CouplingHalf(self)
