"""CutterSimulationCalc"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CUTTER_SIMULATION_CALC = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "CutterSimulationCalc",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
        _835,
        _840,
        _841,
        _843,
        _846,
        _848,
        _849,
        _850,
        _851,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _832

    Self = TypeVar("Self", bound="CutterSimulationCalc")
    CastSelf = TypeVar(
        "CastSelf", bound="CutterSimulationCalc._Cast_CutterSimulationCalc"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CutterSimulationCalc",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CutterSimulationCalc:
    """Special nested class for casting CutterSimulationCalc to subclasses."""

    __parent__: "CutterSimulationCalc"

    @property
    def form_wheel_grinding_simulation_calculator(
        self: "CastSelf",
    ) -> "_841.FormWheelGrindingSimulationCalculator":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _841,
        )

        return self.__parent__._cast(_841.FormWheelGrindingSimulationCalculator)

    @property
    def hob_simulation_calculator(self: "CastSelf") -> "_843.HobSimulationCalculator":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _843,
        )

        return self.__parent__._cast(_843.HobSimulationCalculator)

    @property
    def rack_simulation_calculator(self: "CastSelf") -> "_846.RackSimulationCalculator":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _846,
        )

        return self.__parent__._cast(_846.RackSimulationCalculator)

    @property
    def shaper_simulation_calculator(
        self: "CastSelf",
    ) -> "_848.ShaperSimulationCalculator":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _848,
        )

        return self.__parent__._cast(_848.ShaperSimulationCalculator)

    @property
    def shaving_simulation_calculator(
        self: "CastSelf",
    ) -> "_849.ShavingSimulationCalculator":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _849,
        )

        return self.__parent__._cast(_849.ShavingSimulationCalculator)

    @property
    def virtual_simulation_calculator(
        self: "CastSelf",
    ) -> "_850.VirtualSimulationCalculator":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _850,
        )

        return self.__parent__._cast(_850.VirtualSimulationCalculator)

    @property
    def worm_grinder_simulation_calculator(
        self: "CastSelf",
    ) -> "_851.WormGrinderSimulationCalculator":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _851,
        )

        return self.__parent__._cast(_851.WormGrinderSimulationCalculator)

    @property
    def cutter_simulation_calc(self: "CastSelf") -> "CutterSimulationCalc":
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
class CutterSimulationCalc(_0.APIBase):
    """CutterSimulationCalc

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUTTER_SIMULATION_CALC

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def base_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BaseDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def base_to_form_radius_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BaseToFormRadiusClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def chamfer_transverse_pressure_angle_at_tip_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ChamferTransversePressureAngleAtTipFormDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def critical_section_diameter(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CriticalSectionDiameter")

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def finish_cutter_tip_to_fillet_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishCutterTipToFilletClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def generating_circle_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeneratingCircleDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lowest_sap_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowestSAPDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_finish_stock_arc_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumFinishStockArcLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_finish_stock_arc_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumFinishStockArcLength")

        if temp is None:
            return 0.0

        return temp

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
    def normal_thickness_at_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalThicknessAtFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_thickness_at_tip_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalThicknessAtTipFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_tip_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalTipThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_tooth_thickness_on_the_reference_circle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalToothThicknessOnTheReferenceCircle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_tooth_thickness_on_the_v_circle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalToothThicknessOnTheVCircle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def notch_start_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NotchStartDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def profile_shift_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileShiftCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_chamfer_height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialChamferHeight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_clearance_between_rough_root_circle_and_theoretical_finish_root_circle(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "RadialClearanceBetweenRoughRootCircleAndTheoreticalFinishRootCircle",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reference_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def residual_fillet_undercut(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResidualFilletUndercut")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def residual_fillet_undercut_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResidualFilletUndercutDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rough_root_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughRootFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sap_to_form_radius_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SAPToFormRadiusClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def theoretical_finish_root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TheoreticalFinishRootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def theoretical_finish_root_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TheoreticalFinishRootFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_chamfer_angle_straight_line_approximation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseChamferAngleStraightLineApproximation"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_chamfer_angle_tangent_to_involute_at_tip_form_diameter(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseChamferAngleTangentToInvoluteAtTipFormDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_root_fillet_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseRootFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_tip_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseTipThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear(self: "Self") -> "_835.CylindricalCutterSimulatableGear":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.CylindricalCutterSimulatableGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stock_removed_at_designed_sap(self: "Self") -> "_840.FinishStockPoint":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.FinishStockPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StockRemovedAtDesignedSAP")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stock_removed_at_reference_diameter(self: "Self") -> "_840.FinishStockPoint":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.FinishStockPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StockRemovedAtReferenceDiameter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stock_removed_at_rough_tip_form(self: "Self") -> "_840.FinishStockPoint":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.FinishStockPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StockRemovedAtRoughTipForm")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def finish_stock_indexed_arcs(self: "Self") -> "List[_840.FinishStockPoint]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.FinishStockPoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishStockIndexedArcs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_fillet_points(self: "Self") -> "List[_832.NamedPoint]":
        """List[mastapy.gears.manufacturing.cylindrical.cutters.tangibles.NamedPoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearFilletPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def main_profile_finish_stock(self: "Self") -> "List[_840.FinishStockPoint]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.FinishStockPoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MainProfileFinishStock")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def cast_to(self: "Self") -> "_Cast_CutterSimulationCalc":
        """Cast to another type.

        Returns:
            _Cast_CutterSimulationCalc
        """
        return _Cast_CutterSimulationCalc(self)
