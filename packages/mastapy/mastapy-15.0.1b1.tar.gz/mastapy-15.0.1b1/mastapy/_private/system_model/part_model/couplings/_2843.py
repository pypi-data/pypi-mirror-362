"""SplineLeadRelief"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.couplings import _2832

_SPLINE_LEAD_RELIEF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SplineLeadRelief"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility.stiffness_calculators import _1720
    from mastapy._private.system_model.part_model.couplings import _2825
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="SplineLeadRelief")
    CastSelf = TypeVar("CastSelf", bound="SplineLeadRelief._Cast_SplineLeadRelief")


__docformat__ = "restructuredtext en"
__all__ = ("SplineLeadRelief",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SplineLeadRelief:
    """Special nested class for casting SplineLeadRelief to subclasses."""

    __parent__: "SplineLeadRelief"

    @property
    def rigid_connector_settings(self: "CastSelf") -> "_2832.RigidConnectorSettings":
        return self.__parent__._cast(_2832.RigidConnectorSettings)

    @property
    def spline_lead_relief(self: "CastSelf") -> "SplineLeadRelief":
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
class SplineLeadRelief(_2832.RigidConnectorSettings):
    """SplineLeadRelief

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPLINE_LEAD_RELIEF

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_position(self: "Self") -> "_1720.IndividualContactPosition":
        """mastapy.math_utility.stiffness_calculators.IndividualContactPosition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPosition")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.MathUtility.StiffnessCalculators.IndividualContactPosition",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility.stiffness_calculators._1720",
            "IndividualContactPosition",
        )(value)

    @property
    @exception_bridge
    def linear_relief(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LinearRelief")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @linear_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_relief(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LinearRelief", value)

    @property
    @exception_bridge
    def microgeometry_clearance_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicrogeometryClearanceChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def crowning(self: "Self") -> "_2825.CrowningSpecification":
        """mastapy.system_model.part_model.couplings.CrowningSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Crowning")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SplineLeadRelief":
        """Cast to another type.

        Returns:
            _Cast_SplineLeadRelief
        """
        return _Cast_SplineLeadRelief(self)
