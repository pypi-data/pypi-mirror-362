"""AbstractForceAndDisplacementResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D

_ABSTRACT_FORCE_AND_DISPLACEMENT_RESULTS = python_net_import(
    "SMT.MastaAPI.MathUtility.MeasuredVectors", "AbstractForceAndDisplacementResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1744, _1745, _1748

    Self = TypeVar("Self", bound="AbstractForceAndDisplacementResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractForceAndDisplacementResults._Cast_AbstractForceAndDisplacementResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractForceAndDisplacementResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractForceAndDisplacementResults:
    """Special nested class for casting AbstractForceAndDisplacementResults to subclasses."""

    __parent__: "AbstractForceAndDisplacementResults"

    @property
    def force_and_displacement_results(
        self: "CastSelf",
    ) -> "_1744.ForceAndDisplacementResults":
        from mastapy._private.math_utility.measured_vectors import _1744

        return self.__parent__._cast(_1744.ForceAndDisplacementResults)

    @property
    def force_results(self: "CastSelf") -> "_1745.ForceResults":
        from mastapy._private.math_utility.measured_vectors import _1745

        return self.__parent__._cast(_1745.ForceResults)

    @property
    def abstract_force_and_displacement_results(
        self: "CastSelf",
    ) -> "AbstractForceAndDisplacementResults":
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
class AbstractForceAndDisplacementResults(_0.APIBase):
    """AbstractForceAndDisplacementResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_FORCE_AND_DISPLACEMENT_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def node(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Node")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def force(self: "Self") -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Force")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def location(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Location")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractForceAndDisplacementResults":
        """Cast to another type.

        Returns:
            _Cast_AbstractForceAndDisplacementResults
        """
        return _Cast_AbstractForceAndDisplacementResults(self)
