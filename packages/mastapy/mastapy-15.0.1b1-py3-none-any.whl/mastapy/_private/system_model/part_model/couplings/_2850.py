"""SynchroniserHalf"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
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
from mastapy._private.system_model.part_model.couplings import _2851

_SYNCHRONISER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserHalf"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2693, _2698
    from mastapy._private.system_model.part_model.couplings import _2824, _2849

    Self = TypeVar("Self", bound="SynchroniserHalf")
    CastSelf = TypeVar("CastSelf", bound="SynchroniserHalf._Cast_SynchroniserHalf")


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserHalf",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserHalf:
    """Special nested class for casting SynchroniserHalf to subclasses."""

    __parent__: "SynchroniserHalf"

    @property
    def synchroniser_part(self: "CastSelf") -> "_2851.SynchroniserPart":
        return self.__parent__._cast(_2851.SynchroniserPart)

    @property
    def coupling_half(self: "CastSelf") -> "_2824.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2824

        return self.__parent__._cast(_2824.CouplingHalf)

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
        from mastapy._private.system_model.part_model import _2693

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
    def synchroniser_half(self: "CastSelf") -> "SynchroniserHalf":
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
class SynchroniserHalf(_2851.SynchroniserPart):
    """SynchroniserHalf

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER_HALF

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def area_of_cone_with_minimum_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AreaOfConeWithMinimumArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def blocker_chamfer_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BlockerChamferAngle")

        if temp is None:
            return 0.0

        return temp

    @blocker_chamfer_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def blocker_chamfer_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BlockerChamferAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def blocker_chamfer_coefficient_of_friction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "BlockerChamferCoefficientOfFriction"
        )

        if temp is None:
            return 0.0

        return temp

    @blocker_chamfer_coefficient_of_friction.setter
    @exception_bridge
    @enforce_parameter_types
    def blocker_chamfer_coefficient_of_friction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BlockerChamferCoefficientOfFriction",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def blocker_chamfer_pcd(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BlockerChamferPCD")

        if temp is None:
            return 0.0

        return temp

    @blocker_chamfer_pcd.setter
    @exception_bridge
    @enforce_parameter_types
    def blocker_chamfer_pcd(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BlockerChamferPCD",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def cone_side(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConeSide")

        if temp is None:
            return ""

        return temp

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
    def number_of_surfaces(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSurfaces")

        if temp is None:
            return 0

        return temp

    @number_of_surfaces.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_surfaces(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfSurfaces", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def total_area_of_cones(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalAreaOfCones")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cones(self: "Self") -> "List[_2849.SynchroniserCone]":
        """List[mastapy.system_model.part_model.couplings.SynchroniserCone]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cones")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SynchroniserHalf":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserHalf
        """
        return _Cast_SynchroniserHalf(self)
