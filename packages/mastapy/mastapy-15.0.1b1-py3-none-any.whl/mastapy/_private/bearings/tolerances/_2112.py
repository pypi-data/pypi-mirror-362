"""InterferenceTolerance"""

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
from mastapy._private.bearings.tolerances import _2104

_INTERFERENCE_TOLERANCE = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "InterferenceTolerance"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _2091
    from mastapy._private.bearings.tolerances import (
        _2107,
        _2109,
        _2110,
        _2115,
        _2116,
        _2120,
        _2125,
    )

    Self = TypeVar("Self", bound="InterferenceTolerance")
    CastSelf = TypeVar(
        "CastSelf", bound="InterferenceTolerance._Cast_InterferenceTolerance"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterferenceTolerance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterferenceTolerance:
    """Special nested class for casting InterferenceTolerance to subclasses."""

    __parent__: "InterferenceTolerance"

    @property
    def bearing_connection_component(
        self: "CastSelf",
    ) -> "_2104.BearingConnectionComponent":
        return self.__parent__._cast(_2104.BearingConnectionComponent)

    @property
    def inner_ring_tolerance(self: "CastSelf") -> "_2109.InnerRingTolerance":
        from mastapy._private.bearings.tolerances import _2109

        return self.__parent__._cast(_2109.InnerRingTolerance)

    @property
    def inner_support_tolerance(self: "CastSelf") -> "_2110.InnerSupportTolerance":
        from mastapy._private.bearings.tolerances import _2110

        return self.__parent__._cast(_2110.InnerSupportTolerance)

    @property
    def outer_ring_tolerance(self: "CastSelf") -> "_2115.OuterRingTolerance":
        from mastapy._private.bearings.tolerances import _2115

        return self.__parent__._cast(_2115.OuterRingTolerance)

    @property
    def outer_support_tolerance(self: "CastSelf") -> "_2116.OuterSupportTolerance":
        from mastapy._private.bearings.tolerances import _2116

        return self.__parent__._cast(_2116.OuterSupportTolerance)

    @property
    def ring_tolerance(self: "CastSelf") -> "_2120.RingTolerance":
        from mastapy._private.bearings.tolerances import _2120

        return self.__parent__._cast(_2120.RingTolerance)

    @property
    def support_tolerance(self: "CastSelf") -> "_2125.SupportTolerance":
        from mastapy._private.bearings.tolerances import _2125

        return self.__parent__._cast(_2125.SupportTolerance)

    @property
    def interference_tolerance(self: "CastSelf") -> "InterferenceTolerance":
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
class InterferenceTolerance(_2104.BearingConnectionComponent):
    """InterferenceTolerance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTERFERENCE_TOLERANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def definition_option(self: "Self") -> "_2107.BearingToleranceDefinitionOptions":
        """mastapy.bearings.tolerances.BearingToleranceDefinitionOptions"""
        temp = pythonnet_property_get(self.wrapped, "DefinitionOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.Tolerances.BearingToleranceDefinitionOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.tolerances._2107",
            "BearingToleranceDefinitionOptions",
        )(value)

    @definition_option.setter
    @exception_bridge
    @enforce_parameter_types
    def definition_option(
        self: "Self", value: "_2107.BearingToleranceDefinitionOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.Tolerances.BearingToleranceDefinitionOptions"
        )
        pythonnet_property_set(self.wrapped, "DefinitionOption", value)

    @property
    @exception_bridge
    def mounting_point_surface_finish(
        self: "Self",
    ) -> "_2091.MountingPointSurfaceFinishes":
        """mastapy.bearings.MountingPointSurfaceFinishes"""
        temp = pythonnet_property_get(self.wrapped, "MountingPointSurfaceFinish")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.MountingPointSurfaceFinishes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2091", "MountingPointSurfaceFinishes"
        )(value)

    @mounting_point_surface_finish.setter
    @exception_bridge
    @enforce_parameter_types
    def mounting_point_surface_finish(
        self: "Self", value: "_2091.MountingPointSurfaceFinishes"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.MountingPointSurfaceFinishes"
        )
        pythonnet_property_set(self.wrapped, "MountingPointSurfaceFinish", value)

    @property
    @exception_bridge
    def non_contacting_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NonContactingDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @non_contacting_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def non_contacting_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NonContactingDiameter", value)

    @property
    @exception_bridge
    def surface_fitting_reduction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SurfaceFittingReduction")

        if temp is None:
            return 0.0

        return temp

    @surface_fitting_reduction.setter
    @exception_bridge
    @enforce_parameter_types
    def surface_fitting_reduction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SurfaceFittingReduction",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tolerance_lower_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceLowerLimit")

        if temp is None:
            return 0.0

        return temp

    @tolerance_lower_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def tolerance_lower_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceLowerLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tolerance_upper_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceUpperLimit")

        if temp is None:
            return 0.0

        return temp

    @tolerance_upper_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def tolerance_upper_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceUpperLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_InterferenceTolerance":
        """Cast to another type.

        Returns:
            _Cast_InterferenceTolerance
        """
        return _Cast_InterferenceTolerance(self)
