"""StraightBevelDiffGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.bevel import _1302

_STRAIGHT_BEVEL_DIFF_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.StraightBevelDiff", "StraightBevelDiffGearSetDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1052, _1054
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1315
    from mastapy._private.gears.gear_designs.conical import _1276
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _1069, _1070

    Self = TypeVar("Self", bound="StraightBevelDiffGearSetDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearSetDesign._Cast_StraightBevelDiffGearSetDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearSetDesign:
    """Special nested class for casting StraightBevelDiffGearSetDesign to subclasses."""

    __parent__: "StraightBevelDiffGearSetDesign"

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "_1302.BevelGearSetDesign":
        return self.__parent__._cast(_1302.BevelGearSetDesign)

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1315.AGMAGleasonConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1315

        return self.__parent__._cast(_1315.AGMAGleasonConicalGearSetDesign)

    @property
    def conical_gear_set_design(self: "CastSelf") -> "_1276.ConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.conical import _1276

        return self.__parent__._cast(_1276.ConicalGearSetDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "_1054.GearSetDesign":
        from mastapy._private.gears.gear_designs import _1054

        return self.__parent__._cast(_1054.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def straight_bevel_diff_gear_set_design(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearSetDesign":
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
class StraightBevelDiffGearSetDesign(_1302.BevelGearSetDesign):
    """StraightBevelDiffGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def derating_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeratingFactor")

        if temp is None:
            return 0.0

        return temp

    @derating_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def derating_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeratingFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def gears(self: "Self") -> "List[_1069.StraightBevelDiffGearDesign]":
        """List[mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def straight_bevel_diff_gears(
        self: "Self",
    ) -> "List[_1069.StraightBevelDiffGearDesign]":
        """List[mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def straight_bevel_diff_meshes(
        self: "Self",
    ) -> "List[_1070.StraightBevelDiffGearMeshDesign]":
        """List[mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearSetDesign
        """
        return _Cast_StraightBevelDiffGearSetDesign(self)
