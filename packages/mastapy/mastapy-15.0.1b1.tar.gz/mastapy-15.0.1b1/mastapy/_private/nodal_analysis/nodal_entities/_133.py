"""BarBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
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
from mastapy._private.nodal_analysis.nodal_entities import _153

_BAR_BASE = python_net_import("SMT.MastaAPI.NodalAnalysis.NodalEntities", "BarBase")

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.nodal_analysis import _54
    from mastapy._private.nodal_analysis.nodal_entities import _132, _155
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3046,
    )

    Self = TypeVar("Self", bound="BarBase")
    CastSelf = TypeVar("CastSelf", bound="BarBase._Cast_BarBase")


__docformat__ = "restructuredtext en"
__all__ = ("BarBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BarBase:
    """Special nested class for casting BarBase to subclasses."""

    __parent__: "BarBase"

    @property
    def nodal_component(self: "CastSelf") -> "_153.NodalComponent":
        return self.__parent__._cast(_153.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def bar(self: "CastSelf") -> "_132.Bar":
        from mastapy._private.nodal_analysis.nodal_entities import _132

        return self.__parent__._cast(_132.Bar)

    @property
    def shaft_section_system_deflection(
        self: "CastSelf",
    ) -> "_3046.ShaftSectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3046,
        )

        return self.__parent__._cast(_3046.ShaftSectionSystemDeflection)

    @property
    def bar_base(self: "CastSelf") -> "BarBase":
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
class BarBase(_153.NodalComponent):
    """BarBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BAR_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def oil_dip_coefficient_inner_surface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilDipCoefficientInnerSurface")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def oil_dip_coefficient_outer_surface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilDipCoefficientOuterSurface")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torsional_compliance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorsionalCompliance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torsional_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TorsionalStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @torsional_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def torsional_stiffness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TorsionalStiffness", value)

    @property
    @exception_bridge
    def windage_loss_resistive_torque_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindageLossResistiveTorqueInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def windage_loss_resistive_torque_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindageLossResistiveTorqueOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def windage_power_loss_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindagePowerLossInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def windage_power_loss_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindagePowerLossOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bar_geometry(self: "Self") -> "_54.BarGeometry":
        """mastapy.nodal_analysis.BarGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BarGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BarBase":
        """Cast to another type.

        Returns:
            _Cast_BarBase
        """
        return _Cast_BarBase(self)
