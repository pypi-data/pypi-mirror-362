"""WormGearSet"""

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
from mastapy._private.system_model.part_model.gears import _2769

_WORM_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.worm import _1063
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets.gears import _2550
    from mastapy._private.system_model.part_model import _2659, _2698, _2708
    from mastapy._private.system_model.part_model.gears import _2789

    Self = TypeVar("Self", bound="WormGearSet")
    CastSelf = TypeVar("CastSelf", bound="WormGearSet._Cast_WormGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("WormGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearSet:
    """Special nested class for casting WormGearSet to subclasses."""

    __parent__: "WormGearSet"

    @property
    def gear_set(self: "CastSelf") -> "_2769.GearSet":
        return self.__parent__._cast(_2769.GearSet)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2708.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2708

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
    def worm_gear_set(self: "CastSelf") -> "WormGearSet":
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
class WormGearSet(_2769.GearSet):
    """WormGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_gear_set_design(self: "Self") -> "_1063.WormGearSetDesign":
        """mastapy.gears.gear_designs.worm.WormGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def worm_gear_set_design(self: "Self") -> "_1063.WormGearSetDesign":
        """mastapy.gears.gear_designs.worm.WormGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def worm_gears(self: "Self") -> "List[_2789.WormGear]":
        """List[mastapy.system_model.part_model.gears.WormGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def worm_meshes(self: "Self") -> "List[_2550.WormGearMesh]":
        """List[mastapy.system_model.connections_and_sockets.gears.WormGearMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearSet":
        """Cast to another type.

        Returns:
            _Cast_WormGearSet
        """
        return _Cast_WormGearSet(self)
