"""BevelDifferentialPlanetGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.gears import _2752

_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialPlanetGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2693, _2698
    from mastapy._private.system_model.part_model.gears import (
        _2750,
        _2756,
        _2760,
        _2767,
    )

    Self = TypeVar("Self", bound="BevelDifferentialPlanetGear")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialPlanetGear._Cast_BevelDifferentialPlanetGear",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialPlanetGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialPlanetGear:
    """Special nested class for casting BevelDifferentialPlanetGear to subclasses."""

    __parent__: "BevelDifferentialPlanetGear"

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2752.BevelDifferentialGear":
        return self.__parent__._cast(_2752.BevelDifferentialGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2756.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2756

        return self.__parent__._cast(_2756.BevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2750.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2750

        return self.__parent__._cast(_2750.AGMAGleasonConicalGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2760.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2760

        return self.__parent__._cast(_2760.ConicalGear)

    @property
    def gear(self: "CastSelf") -> "_2767.Gear":
        from mastapy._private.system_model.part_model.gears import _2767

        return self.__parent__._cast(_2767.Gear)

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
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "BevelDifferentialPlanetGear":
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
class BevelDifferentialPlanetGear(_2752.BevelDifferentialGear):
    """BevelDifferentialPlanetGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_PLANET_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_planets(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPlanets")

        if temp is None:
            return 0

        return temp

    @number_of_planets.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_planets(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfPlanets", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialPlanetGear":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialPlanetGear
        """
        return _Cast_BevelDifferentialPlanetGear(self)
