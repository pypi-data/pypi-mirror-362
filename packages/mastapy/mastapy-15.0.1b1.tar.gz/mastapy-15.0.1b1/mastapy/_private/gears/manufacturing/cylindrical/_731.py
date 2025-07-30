"""GearManufacturingConfigurationViewModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEAR_MANUFACTURING_CONFIGURATION_VIEW_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical",
    "GearManufacturingConfigurationViewModel",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.manufacturing.cylindrical import _732
    from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
        _857,
        _863,
        _873,
        _874,
    )
    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _777,
        _790,
        _804,
    )

    Self = TypeVar("Self", bound="GearManufacturingConfigurationViewModel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearManufacturingConfigurationViewModel._Cast_GearManufacturingConfigurationViewModel",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearManufacturingConfigurationViewModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearManufacturingConfigurationViewModel:
    """Special nested class for casting GearManufacturingConfigurationViewModel to subclasses."""

    __parent__: "GearManufacturingConfigurationViewModel"

    @property
    def gear_manufacturing_configuration_view_model_placeholder(
        self: "CastSelf",
    ) -> "_732.GearManufacturingConfigurationViewModelPlaceholder":
        from mastapy._private.gears.manufacturing.cylindrical import _732

        return self.__parent__._cast(
            _732.GearManufacturingConfigurationViewModelPlaceholder
        )

    @property
    def hobbing_process_simulation_view_model(
        self: "CastSelf",
    ) -> "_777.HobbingProcessSimulationViewModel":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _777,
        )

        return self.__parent__._cast(_777.HobbingProcessSimulationViewModel)

    @property
    def process_simulation_view_model(
        self: "CastSelf",
    ) -> "_790.ProcessSimulationViewModel":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _790,
        )

        return self.__parent__._cast(_790.ProcessSimulationViewModel)

    @property
    def worm_grinding_process_simulation_view_model(
        self: "CastSelf",
    ) -> "_804.WormGrindingProcessSimulationViewModel":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _804,
        )

        return self.__parent__._cast(_804.WormGrindingProcessSimulationViewModel)

    @property
    def conventional_shaving_dynamics_view_model(
        self: "CastSelf",
    ) -> "_857.ConventionalShavingDynamicsViewModel":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _857,
        )

        return self.__parent__._cast(_857.ConventionalShavingDynamicsViewModel)

    @property
    def plunge_shaving_dynamics_view_model(
        self: "CastSelf",
    ) -> "_863.PlungeShavingDynamicsViewModel":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _863,
        )

        return self.__parent__._cast(_863.PlungeShavingDynamicsViewModel)

    @property
    def shaving_dynamics_view_model(
        self: "CastSelf",
    ) -> "_873.ShavingDynamicsViewModel":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _873,
        )

        return self.__parent__._cast(_873.ShavingDynamicsViewModel)

    @property
    def shaving_dynamics_view_model_base(
        self: "CastSelf",
    ) -> "_874.ShavingDynamicsViewModelBase":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _874,
        )

        return self.__parent__._cast(_874.ShavingDynamicsViewModelBase)

    @property
    def gear_manufacturing_configuration_view_model(
        self: "CastSelf",
    ) -> "GearManufacturingConfigurationViewModel":
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
class GearManufacturingConfigurationViewModel(_0.APIBase):
    """GearManufacturingConfigurationViewModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MANUFACTURING_CONFIGURATION_VIEW_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_GearManufacturingConfigurationViewModel":
        """Cast to another type.

        Returns:
            _Cast_GearManufacturingConfigurationViewModel
        """
        return _Cast_GearManufacturingConfigurationViewModel(self)
