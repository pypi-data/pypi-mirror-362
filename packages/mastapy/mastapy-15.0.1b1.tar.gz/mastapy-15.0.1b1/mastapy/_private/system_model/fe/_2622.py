"""LinkComponentAxialPositionErrorReporter"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D

_LINK_COMPONENT_AXIAL_POSITION_ERROR_REPORTER = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "LinkComponentAxialPositionErrorReporter"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LinkComponentAxialPositionErrorReporter")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LinkComponentAxialPositionErrorReporter._Cast_LinkComponentAxialPositionErrorReporter",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LinkComponentAxialPositionErrorReporter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LinkComponentAxialPositionErrorReporter:
    """Special nested class for casting LinkComponentAxialPositionErrorReporter to subclasses."""

    __parent__: "LinkComponentAxialPositionErrorReporter"

    @property
    def link_component_axial_position_error_reporter(
        self: "CastSelf",
    ) -> "LinkComponentAxialPositionErrorReporter":
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
class LinkComponentAxialPositionErrorReporter(_0.APIBase):
    """LinkComponentAxialPositionErrorReporter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LINK_COMPONENT_AXIAL_POSITION_ERROR_REPORTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def error_in_location_on_axis(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ErrorInLocationOnAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def expected_location_on_component_axis(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExpectedLocationOnComponentAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def location_on_component_axis_from_fe_nodes(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LocationOnComponentAxisFromFENodes"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_LinkComponentAxialPositionErrorReporter":
        """Cast to another type.

        Returns:
            _Cast_LinkComponentAxialPositionErrorReporter
        """
        return _Cast_LinkComponentAxialPositionErrorReporter(self)
