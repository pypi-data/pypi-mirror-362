"""ShaftFEMeshingOptions"""

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
from mastapy._private.nodal_analysis import _64

_SHAFT_FE_MESHING_OPTIONS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "ShaftFEMeshingOptions"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.nodal_analysis import _79

    Self = TypeVar("Self", bound="ShaftFEMeshingOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftFEMeshingOptions._Cast_ShaftFEMeshingOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftFEMeshingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftFEMeshingOptions:
    """Special nested class for casting ShaftFEMeshingOptions to subclasses."""

    __parent__: "ShaftFEMeshingOptions"

    @property
    def fe_meshing_options(self: "CastSelf") -> "_64.FEMeshingOptions":
        return self.__parent__._cast(_64.FEMeshingOptions)

    @property
    def shaft_fe_meshing_options(self: "CastSelf") -> "ShaftFEMeshingOptions":
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
class ShaftFEMeshingOptions(_64.FEMeshingOptions):
    """ShaftFEMeshingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_FE_MESHING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def corner_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CornerTolerance")

        if temp is None:
            return 0.0

        return temp

    @corner_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def corner_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CornerTolerance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def element_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_size.setter
    @exception_bridge
    @enforce_parameter_types
    def element_size(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementSize", value)

    @property
    @exception_bridge
    def meshing_diameter_for_gear(self: "Self") -> "_79.MeshingDiameterForGear":
        """mastapy.nodal_analysis.MeshingDiameterForGear"""
        temp = pythonnet_property_get(self.wrapped, "MeshingDiameterForGear")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.MeshingDiameterForGear"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._79", "MeshingDiameterForGear"
        )(value)

    @meshing_diameter_for_gear.setter
    @exception_bridge
    @enforce_parameter_types
    def meshing_diameter_for_gear(
        self: "Self", value: "_79.MeshingDiameterForGear"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.MeshingDiameterForGear"
        )
        pythonnet_property_set(self.wrapped, "MeshingDiameterForGear", value)

    @property
    @exception_bridge
    def minimum_fillet_radius_to_include(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumFilletRadiusToInclude")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_fillet_radius_to_include.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_fillet_radius_to_include(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumFilletRadiusToInclude", value)

    @property
    @exception_bridge
    def smooth_corners(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SmoothCorners")

        if temp is None:
            return False

        return temp

    @smooth_corners.setter
    @exception_bridge
    @enforce_parameter_types
    def smooth_corners(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SmoothCorners", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftFEMeshingOptions":
        """Cast to another type.

        Returns:
            _Cast_ShaftFEMeshingOptions
        """
        return _Cast_ShaftFEMeshingOptions(self)
