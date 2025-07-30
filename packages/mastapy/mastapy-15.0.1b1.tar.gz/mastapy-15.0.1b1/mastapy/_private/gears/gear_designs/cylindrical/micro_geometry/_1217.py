"""CylindricalGearMicroGeometryPerTooth"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1214

_CYLINDRICAL_GEAR_MICRO_GEOMETRY_PER_TOOTH = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearMicroGeometryPerTooth",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335, _1338, _1341

    Self = TypeVar("Self", bound="CylindricalGearMicroGeometryPerTooth")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMicroGeometryPerTooth._Cast_CylindricalGearMicroGeometryPerTooth",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMicroGeometryPerTooth",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMicroGeometryPerTooth:
    """Special nested class for casting CylindricalGearMicroGeometryPerTooth to subclasses."""

    __parent__: "CylindricalGearMicroGeometryPerTooth"

    @property
    def cylindrical_gear_micro_geometry_base(
        self: "CastSelf",
    ) -> "_1214.CylindricalGearMicroGeometryBase":
        return self.__parent__._cast(_1214.CylindricalGearMicroGeometryBase)

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1341.GearImplementationDetail":
        from mastapy._private.gears.analysis import _1341

        return self.__parent__._cast(_1341.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1338

        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def cylindrical_gear_micro_geometry_per_tooth(
        self: "CastSelf",
    ) -> "CylindricalGearMicroGeometryPerTooth":
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
class CylindricalGearMicroGeometryPerTooth(_1214.CylindricalGearMicroGeometryBase):
    """CylindricalGearMicroGeometryPerTooth

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MICRO_GEOMETRY_PER_TOOTH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMicroGeometryPerTooth":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMicroGeometryPerTooth
        """
        return _Cast_CylindricalGearMicroGeometryPerTooth(self)
