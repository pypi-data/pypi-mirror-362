"""GleasonHypoidMeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.conical import _637

_GLEASON_HYPOID_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Hypoid.Standards", "GleasonHypoidMeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _457

    Self = TypeVar("Self", bound="GleasonHypoidMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GleasonHypoidMeshSingleFlankRating._Cast_GleasonHypoidMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GleasonHypoidMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GleasonHypoidMeshSingleFlankRating:
    """Special nested class for casting GleasonHypoidMeshSingleFlankRating to subclasses."""

    __parent__: "GleasonHypoidMeshSingleFlankRating"

    @property
    def conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_637.ConicalMeshSingleFlankRating":
        return self.__parent__._cast(_637.ConicalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_457.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _457

        return self.__parent__._cast(_457.MeshSingleFlankRating)

    @property
    def gleason_hypoid_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "GleasonHypoidMeshSingleFlankRating":
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
class GleasonHypoidMeshSingleFlankRating(_637.ConicalMeshSingleFlankRating):
    """GleasonHypoidMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GLEASON_HYPOID_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def calculated_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def dynamic_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def elastic_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def geometry_factor_i(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorI")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_distribution_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_distribution_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def overload_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverloadFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def overload_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverloadFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def rating_standard_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingStandardName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def size_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def size_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def surface_condition_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceConditionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def temperature_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TemperatureFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def temperature_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TemperatureFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def transmitted_tangential_load_at_large_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransmittedTangentialLoadAtLargeEnd"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GleasonHypoidMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_GleasonHypoidMeshSingleFlankRating
        """
        return _Cast_GleasonHypoidMeshSingleFlankRating(self)
