"""KeywayJointHalfDesign"""

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
from mastapy._private.detailed_rigid_connectors.interference_fits import _1631

_KEYWAY_JOINT_HALF_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints", "KeywayJointHalfDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors import _1573

    Self = TypeVar("Self", bound="KeywayJointHalfDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="KeywayJointHalfDesign._Cast_KeywayJointHalfDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("KeywayJointHalfDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KeywayJointHalfDesign:
    """Special nested class for casting KeywayJointHalfDesign to subclasses."""

    __parent__: "KeywayJointHalfDesign"

    @property
    def interference_fit_half_design(
        self: "CastSelf",
    ) -> "_1631.InterferenceFitHalfDesign":
        return self.__parent__._cast(_1631.InterferenceFitHalfDesign)

    @property
    def detailed_rigid_connector_half_design(
        self: "CastSelf",
    ) -> "_1573.DetailedRigidConnectorHalfDesign":
        from mastapy._private.detailed_rigid_connectors import _1573

        return self.__parent__._cast(_1573.DetailedRigidConnectorHalfDesign)

    @property
    def keyway_joint_half_design(self: "CastSelf") -> "KeywayJointHalfDesign":
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
class KeywayJointHalfDesign(_1631.InterferenceFitHalfDesign):
    """KeywayJointHalfDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KEYWAY_JOINT_HALF_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def effective_keyway_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveKeywayDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hardness_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HardnessFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def is_case_hardened(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsCaseHardened")

        if temp is None:
            return False

        return temp

    @is_case_hardened.setter
    @exception_bridge
    @enforce_parameter_types
    def is_case_hardened(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsCaseHardened", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def keyway_chamfer_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "KeywayChamferDepth")

        if temp is None:
            return 0.0

        return temp

    @keyway_chamfer_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def keyway_chamfer_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "KeywayChamferDepth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def support_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SupportFactor")

        if temp is None:
            return 0.0

        return temp

    @support_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def support_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SupportFactor", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_KeywayJointHalfDesign":
        """Cast to another type.

        Returns:
            _Cast_KeywayJointHalfDesign
        """
        return _Cast_KeywayJointHalfDesign(self)
