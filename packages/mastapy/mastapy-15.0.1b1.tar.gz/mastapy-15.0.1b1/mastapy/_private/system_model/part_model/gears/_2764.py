"""CylindricalPlanetGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2762

_CYLINDRICAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalPlanetGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2693, _2698
    from mastapy._private.system_model.part_model.gears import _2767

    Self = TypeVar("Self", bound="CylindricalPlanetGear")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalPlanetGear._Cast_CylindricalPlanetGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalPlanetGear:
    """Special nested class for casting CylindricalPlanetGear to subclasses."""

    __parent__: "CylindricalPlanetGear"

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2762.CylindricalGear":
        return self.__parent__._cast(_2762.CylindricalGear)

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
    def cylindrical_planet_gear(self: "CastSelf") -> "CylindricalPlanetGear":
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
class CylindricalPlanetGear(_2762.CylindricalGear):
    """CylindricalPlanetGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_PLANET_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalPlanetGear":
        """Cast to another type.

        Returns:
            _Cast_CylindricalPlanetGear
        """
        return _Cast_CylindricalPlanetGear(self)
