"""RelativeComponentAlignment"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_RELATIVE_COMPONENT_ALIGNMENT = python_net_import(
    "SMT.MastaAPI.SystemModel", "RelativeComponentAlignment"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.math_utility import _1675
    from mastapy._private.system_model import _2432
    from mastapy._private.system_model.part_model import _2670

    Self = TypeVar("Self", bound="RelativeComponentAlignment")
    CastSelf = TypeVar(
        "CastSelf", bound="RelativeComponentAlignment._Cast_RelativeComponentAlignment"
    )

T = TypeVar("T", bound="_2670.Component")

__docformat__ = "restructuredtext en"
__all__ = ("RelativeComponentAlignment",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RelativeComponentAlignment:
    """Special nested class for casting RelativeComponentAlignment to subclasses."""

    __parent__: "RelativeComponentAlignment"

    @property
    def relative_component_alignment(self: "CastSelf") -> "RelativeComponentAlignment":
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
class RelativeComponentAlignment(_0.APIBase, Generic[T]):
    """RelativeComponentAlignment

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _RELATIVE_COMPONENT_ALIGNMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def alignment_axis(self: "Self") -> "_1675.AlignmentAxis":
        """mastapy.math_utility.AlignmentAxis"""
        temp = pythonnet_property_get(self.wrapped, "AlignmentAxis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.MathUtility.AlignmentAxis")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1675", "AlignmentAxis"
        )(value)

    @alignment_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def alignment_axis(self: "Self", value: "_1675.AlignmentAxis") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.AlignmentAxis"
        )
        pythonnet_property_set(self.wrapped, "AlignmentAxis", value)

    @property
    @exception_bridge
    def axial_offset(self: "Self") -> "_2432.RelativeOffsetOption":
        """mastapy.system_model.RelativeOffsetOption"""
        temp = pythonnet_property_get(self.wrapped, "AxialOffset")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.RelativeOffsetOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model._2432", "RelativeOffsetOption"
        )(value)

    @axial_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_offset(self: "Self", value: "_2432.RelativeOffsetOption") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.RelativeOffsetOption"
        )
        pythonnet_property_set(self.wrapped, "AxialOffset", value)

    @property
    @exception_bridge
    def rotation_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAngle")

        if temp is None:
            return 0.0

        return temp

    @rotation_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def rotation_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RotationAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def specified_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedOffset")

        if temp is None:
            return 0.0

        return temp

    @specified_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SpecifiedOffset", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RelativeComponentAlignment":
        """Cast to another type.

        Returns:
            _Cast_RelativeComponentAlignment
        """
        return _Cast_RelativeComponentAlignment(self)
