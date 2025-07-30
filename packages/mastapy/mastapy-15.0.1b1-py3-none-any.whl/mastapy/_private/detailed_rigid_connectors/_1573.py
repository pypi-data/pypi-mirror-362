"""DetailedRigidConnectorHalfDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DETAILED_RIGID_CONNECTOR_HALF_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors", "DetailedRigidConnectorHalfDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.detailed_rigid_connectors.interference_fits import _1631
    from mastapy._private.detailed_rigid_connectors.keyed_joints import _1624
    from mastapy._private.detailed_rigid_connectors.splines import (
        _1574,
        _1577,
        _1581,
        _1584,
        _1592,
        _1599,
        _1604,
    )

    Self = TypeVar("Self", bound="DetailedRigidConnectorHalfDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DetailedRigidConnectorHalfDesign._Cast_DetailedRigidConnectorHalfDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DetailedRigidConnectorHalfDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DetailedRigidConnectorHalfDesign:
    """Special nested class for casting DetailedRigidConnectorHalfDesign to subclasses."""

    __parent__: "DetailedRigidConnectorHalfDesign"

    @property
    def custom_spline_half_design(self: "CastSelf") -> "_1574.CustomSplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1574

        return self.__parent__._cast(_1574.CustomSplineHalfDesign)

    @property
    def din5480_spline_half_design(self: "CastSelf") -> "_1577.DIN5480SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1577

        return self.__parent__._cast(_1577.DIN5480SplineHalfDesign)

    @property
    def gbt3478_spline_half_design(self: "CastSelf") -> "_1581.GBT3478SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1581

        return self.__parent__._cast(_1581.GBT3478SplineHalfDesign)

    @property
    def iso4156_spline_half_design(self: "CastSelf") -> "_1584.ISO4156SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1584

        return self.__parent__._cast(_1584.ISO4156SplineHalfDesign)

    @property
    def sae_spline_half_design(self: "CastSelf") -> "_1592.SAESplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1592

        return self.__parent__._cast(_1592.SAESplineHalfDesign)

    @property
    def spline_half_design(self: "CastSelf") -> "_1599.SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1599

        return self.__parent__._cast(_1599.SplineHalfDesign)

    @property
    def standard_spline_half_design(
        self: "CastSelf",
    ) -> "_1604.StandardSplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1604

        return self.__parent__._cast(_1604.StandardSplineHalfDesign)

    @property
    def keyway_joint_half_design(self: "CastSelf") -> "_1624.KeywayJointHalfDesign":
        from mastapy._private.detailed_rigid_connectors.keyed_joints import _1624

        return self.__parent__._cast(_1624.KeywayJointHalfDesign)

    @property
    def interference_fit_half_design(
        self: "CastSelf",
    ) -> "_1631.InterferenceFitHalfDesign":
        from mastapy._private.detailed_rigid_connectors.interference_fits import _1631

        return self.__parent__._cast(_1631.InterferenceFitHalfDesign)

    @property
    def detailed_rigid_connector_half_design(
        self: "CastSelf",
    ) -> "DetailedRigidConnectorHalfDesign":
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
class DetailedRigidConnectorHalfDesign(_0.APIBase):
    """DetailedRigidConnectorHalfDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DETAILED_RIGID_CONNECTOR_HALF_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def tensile_yield_strength(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TensileYieldStrength")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tensile_yield_strength.setter
    @exception_bridge
    @enforce_parameter_types
    def tensile_yield_strength(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TensileYieldStrength", value)

    @property
    @exception_bridge
    def ultimate_tensile_strength(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "UltimateTensileStrength")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @ultimate_tensile_strength.setter
    @exception_bridge
    @enforce_parameter_types
    def ultimate_tensile_strength(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UltimateTensileStrength", value)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DetailedRigidConnectorHalfDesign":
        """Cast to another type.

        Returns:
            _Cast_DetailedRigidConnectorHalfDesign
        """
        return _Cast_DetailedRigidConnectorHalfDesign(self)
