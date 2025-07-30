"""CylindricalGearGrindingWorm"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.cutters import _815

_CYLINDRICAL_GEAR_GRINDING_WORM = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters",
    "CylindricalGearGrindingWorm",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _809, _816
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
        _831,
        _833,
    )
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="CylindricalGearGrindingWorm")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearGrindingWorm._Cast_CylindricalGearGrindingWorm",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearGrindingWorm",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearGrindingWorm:
    """Special nested class for casting CylindricalGearGrindingWorm to subclasses."""

    __parent__: "CylindricalGearGrindingWorm"

    @property
    def cylindrical_gear_rack_design(
        self: "CastSelf",
    ) -> "_815.CylindricalGearRackDesign":
        return self.__parent__._cast(_815.CylindricalGearRackDesign)

    @property
    def cylindrical_gear_real_cutter_design(
        self: "CastSelf",
    ) -> "_816.CylindricalGearRealCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _816

        return self.__parent__._cast(_816.CylindricalGearRealCutterDesign)

    @property
    def cylindrical_gear_abstract_cutter_design(
        self: "CastSelf",
    ) -> "_809.CylindricalGearAbstractCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _809

        return self.__parent__._cast(_809.CylindricalGearAbstractCutterDesign)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def cylindrical_gear_grinding_worm(
        self: "CastSelf",
    ) -> "CylindricalGearGrindingWorm":
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
class CylindricalGearGrindingWorm(_815.CylindricalGearRackDesign):
    """CylindricalGearGrindingWorm

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_GRINDING_WORM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def edge_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EdgeHeight")

        if temp is None:
            return 0.0

        return temp

    @edge_height.setter
    @exception_bridge
    @enforce_parameter_types
    def edge_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EdgeHeight", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def flat_tip_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FlatTipWidth")

        if temp is None:
            return 0.0

        return temp

    @flat_tip_width.setter
    @exception_bridge
    @enforce_parameter_types
    def flat_tip_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FlatTipWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def has_tolerances(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasTolerances")

        if temp is None:
            return False

        return temp

    @has_tolerances.setter
    @exception_bridge
    @enforce_parameter_types
    def has_tolerances(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasTolerances", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def nominal_rack_shape(self: "Self") -> "_833.RackShape":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.RackShape

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalRackShape")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def nominal_worm_grinder_shape(
        self: "Self",
    ) -> "_831.CylindricalGearWormGrinderShape":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.CylindricalGearWormGrinderShape

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalWormGrinderShape")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearGrindingWorm":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearGrindingWorm
        """
        return _Cast_CylindricalGearGrindingWorm(self)
