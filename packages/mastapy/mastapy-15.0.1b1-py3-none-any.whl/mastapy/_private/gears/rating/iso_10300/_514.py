"""ISO10300MeshSingleFlankRatingBevelMethodB2"""

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
from mastapy._private.gears.rating.iso_10300 import _517

_ISO10300_MESH_SINGLE_FLANK_RATING_BEVEL_METHOD_B2 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300MeshSingleFlankRatingBevelMethodB2"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _457
    from mastapy._private.gears.rating.conical import _637
    from mastapy._private.gears.rating.iso_10300 import _513

    Self = TypeVar("Self", bound="ISO10300MeshSingleFlankRatingBevelMethodB2")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO10300MeshSingleFlankRatingBevelMethodB2._Cast_ISO10300MeshSingleFlankRatingBevelMethodB2",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO10300MeshSingleFlankRatingBevelMethodB2",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO10300MeshSingleFlankRatingBevelMethodB2:
    """Special nested class for casting ISO10300MeshSingleFlankRatingBevelMethodB2 to subclasses."""

    __parent__: "ISO10300MeshSingleFlankRatingBevelMethodB2"

    @property
    def iso10300_mesh_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "_517.ISO10300MeshSingleFlankRatingMethodB2":
        return self.__parent__._cast(_517.ISO10300MeshSingleFlankRatingMethodB2)

    @property
    def iso10300_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_513.ISO10300MeshSingleFlankRating":
        pass

        from mastapy._private.gears.rating.iso_10300 import _513

        return self.__parent__._cast(_513.ISO10300MeshSingleFlankRating)

    @property
    def conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_637.ConicalMeshSingleFlankRating":
        from mastapy._private.gears.rating.conical import _637

        return self.__parent__._cast(_637.ConicalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_457.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _457

        return self.__parent__._cast(_457.MeshSingleFlankRating)

    @property
    def iso10300_mesh_single_flank_rating_bevel_method_b2(
        self: "CastSelf",
    ) -> "ISO10300MeshSingleFlankRatingBevelMethodB2":
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
class ISO10300MeshSingleFlankRatingBevelMethodB2(
    _517.ISO10300MeshSingleFlankRatingMethodB2
):
    """ISO10300MeshSingleFlankRatingBevelMethodB2

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO10300_MESH_SINGLE_FLANK_RATING_BEVEL_METHOD_B2

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def load_sharing_ratio_for_bending_method_b2_for_none_statically_loaded_bevel_gear(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LoadSharingRatioForBendingMethodB2ForNoneStaticallyLoadedBevelGear",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_sharing_ratio_for_bending_method_b2_statically_loaded_straight_and_zerol_bevel_gears(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LoadSharingRatioForBendingMethodB2StaticallyLoadedStraightAndZerolBevelGears",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def location_of_point_of_load_application_for_maximum_bending_stress_on_path_of_action(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LocationOfPointOfLoadApplicationForMaximumBendingStressOnPathOfAction",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def location_of_point_of_load_application_for_maximum_bending_stress_on_path_of_action_for_non_statically_loaded_with_modified_contact_ratio_larger_than_2(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LocationOfPointOfLoadApplicationForMaximumBendingStressOnPathOfActionForNonStaticallyLoadedWithModifiedContactRatioLargerThan2",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def location_of_point_of_load_application_for_maximum_bending_stress_on_path_of_action_for_non_statically_loaded_with_modified_contact_ratio_less_or_equal_than_2(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LocationOfPointOfLoadApplicationForMaximumBendingStressOnPathOfActionForNonStaticallyLoadedWithModifiedContactRatioLessOrEqualThan2",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def location_of_point_of_load_application_for_maximum_bending_stress_on_path_of_action_for_statically_loaded_straight_bevel_and_zerol_bevel_gear(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LocationOfPointOfLoadApplicationForMaximumBendingStressOnPathOfActionForStaticallyLoadedStraightBevelAndZerolBevelGear",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_length_of_action_to_point_of_load_application_method_b2(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeLengthOfActionToPointOfLoadApplicationMethodB2"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gj(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GJ")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO10300MeshSingleFlankRatingBevelMethodB2":
        """Cast to another type.

        Returns:
            _Cast_ISO10300MeshSingleFlankRatingBevelMethodB2
        """
        return _Cast_ISO10300MeshSingleFlankRatingBevelMethodB2(self)
