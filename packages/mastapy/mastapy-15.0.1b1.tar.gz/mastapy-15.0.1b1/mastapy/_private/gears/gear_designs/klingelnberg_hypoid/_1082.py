"""KlingelnbergCycloPalloidHypoidGearMeshDesign"""

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
from mastapy._private.gears.gear_designs.klingelnberg_conical import _1086

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.KlingelnbergHypoid",
    "KlingelnbergCycloPalloidHypoidGearMeshDesign",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1052, _1053
    from mastapy._private.gears.gear_designs.conical import _1275
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import (
        _1081,
        _1083,
        _1084,
    )

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidHypoidGearMeshDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearMeshDesign._Cast_KlingelnbergCycloPalloidHypoidGearMeshDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearMeshDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearMeshDesign:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearMeshDesign to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearMeshDesign"

    @property
    def klingelnberg_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1086.KlingelnbergConicalGearMeshDesign":
        return self.__parent__._cast(_1086.KlingelnbergConicalGearMeshDesign)

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "_1275.ConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.conical import _1275

        return self.__parent__._cast(_1275.ConicalGearMeshDesign)

    @property
    def gear_mesh_design(self: "CastSelf") -> "_1053.GearMeshDesign":
        from mastapy._private.gears.gear_designs import _1053

        return self.__parent__._cast(_1053.GearMeshDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearMeshDesign":
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
class KlingelnbergCycloPalloidHypoidGearMeshDesign(
    _1086.KlingelnbergConicalGearMeshDesign
):
    """KlingelnbergCycloPalloidHypoidGearMeshDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self",
    ) -> "_1083.KlingelnbergCycloPalloidHypoidGearSetDesign":
        """mastapy.gears.gear_designs.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearSet"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_hypoid_gears(
        self: "Self",
    ) -> "List[_1081.KlingelnbergCycloPalloidHypoidGearDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGears"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_hypoid_meshed_gears(
        self: "Self",
    ) -> "List[_1084.KlingelnbergCycloPalloidHypoidMeshedGearDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidMeshedGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidMeshedGears"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidHypoidGearMeshDesign":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearMeshDesign
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearMeshDesign(self)
