"""ActiveGearSetDesignSelectionGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs import _1054
from mastapy._private.system_model.part_model.configurations import _2864
from mastapy._private.system_model.part_model.gears import _2748, _2769

_ACTIVE_GEAR_SET_DESIGN_SELECTION_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ActiveGearSetDesignSelectionGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ActiveGearSetDesignSelectionGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ActiveGearSetDesignSelectionGroup._Cast_ActiveGearSetDesignSelectionGroup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ActiveGearSetDesignSelectionGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ActiveGearSetDesignSelectionGroup:
    """Special nested class for casting ActiveGearSetDesignSelectionGroup to subclasses."""

    __parent__: "ActiveGearSetDesignSelectionGroup"

    @property
    def part_detail_configuration(self: "CastSelf") -> "_2864.PartDetailConfiguration":
        return self.__parent__._cast(_2864.PartDetailConfiguration)

    @property
    def active_gear_set_design_selection_group(
        self: "CastSelf",
    ) -> "ActiveGearSetDesignSelectionGroup":
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
class ActiveGearSetDesignSelectionGroup(
    _2864.PartDetailConfiguration[
        _2748.ActiveGearSetDesignSelection, _2769.GearSet, _1054.GearSetDesign
    ]
):
    """ActiveGearSetDesignSelectionGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ACTIVE_GEAR_SET_DESIGN_SELECTION_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialContactRatioRatingForNVH")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_width_of_widest_cylindrical_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidthOfWidestCylindricalGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_cylindrical_axial_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumCylindricalAxialContactRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_cylindrical_transverse_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumCylindricalTransverseContactRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_tip_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumTipThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def simple_mass_of_cylindrical_gears(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SimpleMassOfCylindricalGears")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_face_width_of_cylindrical_gears(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalFaceWidthOfCylindricalGears")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseContactRatioRatingForNVH"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_and_axial_contact_ratio_rating_for_nvh(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseAndAxialContactRatioRatingForNVH"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ActiveGearSetDesignSelectionGroup":
        """Cast to another type.

        Returns:
            _Cast_ActiveGearSetDesignSelectionGroup
        """
        return _Cast_ActiveGearSetDesignSelectionGroup(self)
