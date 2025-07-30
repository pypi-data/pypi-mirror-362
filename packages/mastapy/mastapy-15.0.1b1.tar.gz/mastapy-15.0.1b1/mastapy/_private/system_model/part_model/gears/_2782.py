"""SpiralBevelGearSet"""

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
from mastapy._private.system_model.part_model.gears import _2757

_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.spiral_bevel import _1075
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets.gears import _2544
    from mastapy._private.system_model.part_model import _2659, _2698, _2708
    from mastapy._private.system_model.part_model.gears import (
        _2751,
        _2761,
        _2769,
        _2781,
    )

    Self = TypeVar("Self", bound="SpiralBevelGearSet")
    CastSelf = TypeVar("CastSelf", bound="SpiralBevelGearSet._Cast_SpiralBevelGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearSet:
    """Special nested class for casting SpiralBevelGearSet to subclasses."""

    __parent__: "SpiralBevelGearSet"

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2757.BevelGearSet":
        return self.__parent__._cast(_2757.BevelGearSet)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2751.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2751

        return self.__parent__._cast(_2751.AGMAGleasonConicalGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2761.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2761

        return self.__parent__._cast(_2761.ConicalGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2769.GearSet":
        from mastapy._private.system_model.part_model.gears import _2769

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
    def spiral_bevel_gear_set(self: "CastSelf") -> "SpiralBevelGearSet":
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
class SpiralBevelGearSet(_2757.BevelGearSet):
    """SpiralBevelGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def conical_gear_set_design(self: "Self") -> "_1075.SpiralBevelGearSetDesign":
        """mastapy.gears.gear_designs.spiral_bevel.SpiralBevelGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def spiral_bevel_gear_set_design(self: "Self") -> "_1075.SpiralBevelGearSetDesign":
        """mastapy.gears.gear_designs.spiral_bevel.SpiralBevelGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def spiral_bevel_gears(self: "Self") -> "List[_2781.SpiralBevelGear]":
        """List[mastapy.system_model.part_model.gears.SpiralBevelGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def spiral_bevel_meshes(self: "Self") -> "List[_2544.SpiralBevelGearMesh]":
        """List[mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelGearSet":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearSet
        """
        return _Cast_SpiralBevelGearSet(self)
