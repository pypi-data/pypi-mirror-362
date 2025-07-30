"""JISB1603SplineJointDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.detailed_rigid_connectors.splines import _1585

_JISB1603_SPLINE_JOINT_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "JISB1603SplineJointDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors import _1572
    from mastapy._private.detailed_rigid_connectors.splines import _1600, _1605

    Self = TypeVar("Self", bound="JISB1603SplineJointDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="JISB1603SplineJointDesign._Cast_JISB1603SplineJointDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("JISB1603SplineJointDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_JISB1603SplineJointDesign:
    """Special nested class for casting JISB1603SplineJointDesign to subclasses."""

    __parent__: "JISB1603SplineJointDesign"

    @property
    def iso4156_spline_joint_design(
        self: "CastSelf",
    ) -> "_1585.ISO4156SplineJointDesign":
        return self.__parent__._cast(_1585.ISO4156SplineJointDesign)

    @property
    def standard_spline_joint_design(
        self: "CastSelf",
    ) -> "_1605.StandardSplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1605

        return self.__parent__._cast(_1605.StandardSplineJointDesign)

    @property
    def spline_joint_design(self: "CastSelf") -> "_1600.SplineJointDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1600

        return self.__parent__._cast(_1600.SplineJointDesign)

    @property
    def detailed_rigid_connector_design(
        self: "CastSelf",
    ) -> "_1572.DetailedRigidConnectorDesign":
        from mastapy._private.detailed_rigid_connectors import _1572

        return self.__parent__._cast(_1572.DetailedRigidConnectorDesign)

    @property
    def jisb1603_spline_joint_design(self: "CastSelf") -> "JISB1603SplineJointDesign":
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
class JISB1603SplineJointDesign(_1585.ISO4156SplineJointDesign):
    """JISB1603SplineJointDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _JISB1603_SPLINE_JOINT_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_JISB1603SplineJointDesign":
        """Cast to another type.

        Returns:
            _Cast_JISB1603SplineJointDesign
        """
        return _Cast_JISB1603SplineJointDesign(self)
