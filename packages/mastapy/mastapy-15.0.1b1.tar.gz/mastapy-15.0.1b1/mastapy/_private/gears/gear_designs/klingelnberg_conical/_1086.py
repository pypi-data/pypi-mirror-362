"""KlingelnbergConicalGearMeshDesign"""

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
from mastapy._private.gears.gear_designs.conical import _1275

_KLINGELNBERG_CONICAL_GEAR_MESH_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.KlingelnbergConical",
    "KlingelnbergConicalGearMeshDesign",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs import _1052, _1053
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1082
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1078

    Self = TypeVar("Self", bound="KlingelnbergConicalGearMeshDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergConicalGearMeshDesign._Cast_KlingelnbergConicalGearMeshDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergConicalGearMeshDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergConicalGearMeshDesign:
    """Special nested class for casting KlingelnbergConicalGearMeshDesign to subclasses."""

    __parent__: "KlingelnbergConicalGearMeshDesign"

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "_1275.ConicalGearMeshDesign":
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
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1078.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1078

        return self.__parent__._cast(
            _1078.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1082.KlingelnbergCycloPalloidHypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1082

        return self.__parent__._cast(_1082.KlingelnbergCycloPalloidHypoidGearMeshDesign)

    @property
    def klingelnberg_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "KlingelnbergConicalGearMeshDesign":
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
class KlingelnbergConicalGearMeshDesign(_1275.ConicalGearMeshDesign):
    """KlingelnbergConicalGearMeshDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CONICAL_GEAR_MESH_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def application_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ApplicationFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @application_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def application_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ApplicationFactor", value)

    @property
    @exception_bridge
    def effective_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_distribution_factor_longitudinal(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "LoadDistributionFactorLongitudinal"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @load_distribution_factor_longitudinal.setter
    @exception_bridge
    @enforce_parameter_types
    def load_distribution_factor_longitudinal(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "LoadDistributionFactorLongitudinal", value
        )

    @property
    @exception_bridge
    def net_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NetFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergConicalGearMeshDesign":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergConicalGearMeshDesign
        """
        return _Cast_KlingelnbergConicalGearMeshDesign(self)
