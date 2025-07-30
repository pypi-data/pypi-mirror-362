"""ConceptClearanceBearing"""

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
from mastapy._private.bearings.bearing_designs import _2344

_CONCEPT_CLEARANCE_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Concept", "ConceptClearanceBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2340
    from mastapy._private.bearings.bearing_designs.concept import _2408, _2410

    Self = TypeVar("Self", bound="ConceptClearanceBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="ConceptClearanceBearing._Cast_ConceptClearanceBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptClearanceBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptClearanceBearing:
    """Special nested class for casting ConceptClearanceBearing to subclasses."""

    __parent__: "ConceptClearanceBearing"

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2344.NonLinearBearing":
        return self.__parent__._cast(_2344.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2340.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2340

        return self.__parent__._cast(_2340.BearingDesign)

    @property
    def concept_axial_clearance_bearing(
        self: "CastSelf",
    ) -> "_2408.ConceptAxialClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2408

        return self.__parent__._cast(_2408.ConceptAxialClearanceBearing)

    @property
    def concept_radial_clearance_bearing(
        self: "CastSelf",
    ) -> "_2410.ConceptRadialClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2410

        return self.__parent__._cast(_2410.ConceptRadialClearanceBearing)

    @property
    def concept_clearance_bearing(self: "CastSelf") -> "ConceptClearanceBearing":
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
class ConceptClearanceBearing(_2344.NonLinearBearing):
    """ConceptClearanceBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_CLEARANCE_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactDiameter")

        if temp is None:
            return 0.0

        return temp

    @contact_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ContactDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def contact_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactStiffness")

        if temp is None:
            return 0.0

        return temp

    @contact_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ContactStiffness", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptClearanceBearing":
        """Cast to another type.

        Returns:
            _Cast_ConceptClearanceBearing
        """
        return _Cast_ConceptClearanceBearing(self)
