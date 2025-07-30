"""HarmonicLoadDataImportFromMotorPackages"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
)
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.harmonic_load_data import _1566
from mastapy._private.system_model.analyses_and_results.static_loads import _7770

_HARMONIC_LOAD_DATA_IMPORT_FROM_MOTOR_PACKAGES = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "HarmonicLoadDataImportFromMotorPackages",
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7749,
        _7767,
        _7769,
        _7772,
        _7773,
    )

    Self = TypeVar("Self", bound="HarmonicLoadDataImportFromMotorPackages")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicLoadDataImportFromMotorPackages._Cast_HarmonicLoadDataImportFromMotorPackages",
    )

T = TypeVar("T", bound="_7749.ElectricMachineHarmonicLoadImportOptionsBase")

__docformat__ = "restructuredtext en"
__all__ = ("HarmonicLoadDataImportFromMotorPackages",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicLoadDataImportFromMotorPackages:
    """Special nested class for casting HarmonicLoadDataImportFromMotorPackages to subclasses."""

    __parent__: "HarmonicLoadDataImportFromMotorPackages"

    @property
    def harmonic_load_data_import_base(
        self: "CastSelf",
    ) -> "_7770.HarmonicLoadDataImportBase":
        return self.__parent__._cast(_7770.HarmonicLoadDataImportBase)

    @property
    def harmonic_load_data_csv_import(
        self: "CastSelf",
    ) -> "_7767.HarmonicLoadDataCSVImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7767,
        )

        return self.__parent__._cast(_7767.HarmonicLoadDataCSVImport)

    @property
    def harmonic_load_data_flux_import(
        self: "CastSelf",
    ) -> "_7769.HarmonicLoadDataFluxImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7769,
        )

        return self.__parent__._cast(_7769.HarmonicLoadDataFluxImport)

    @property
    def harmonic_load_data_jmag_import(
        self: "CastSelf",
    ) -> "_7772.HarmonicLoadDataJMAGImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7772,
        )

        return self.__parent__._cast(_7772.HarmonicLoadDataJMAGImport)

    @property
    def harmonic_load_data_motor_cad_import(
        self: "CastSelf",
    ) -> "_7773.HarmonicLoadDataMotorCADImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7773,
        )

        return self.__parent__._cast(_7773.HarmonicLoadDataMotorCADImport)

    @property
    def harmonic_load_data_import_from_motor_packages(
        self: "CastSelf",
    ) -> "HarmonicLoadDataImportFromMotorPackages":
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
class HarmonicLoadDataImportFromMotorPackages(_7770.HarmonicLoadDataImportBase[T]):
    """HarmonicLoadDataImportFromMotorPackages

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _HARMONIC_LOAD_DATA_IMPORT_FROM_MOTOR_PACKAGES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_slice_number(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_int":
        """ListWithSelectedItem[int]"""
        temp = pythonnet_property_get(self.wrapped, "AxialSliceNumber")

        if temp is None:
            return 0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_int",
        )(temp)

    @axial_slice_number.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_slice_number(self: "Self", value: "int") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "AxialSliceNumber", value)

    @property
    @exception_bridge
    def data_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType":
        """EnumWithSelectedValue[mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType]"""
        temp = pythonnet_property_get(self.wrapped, "DataType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @data_type.setter
    @exception_bridge
    @enforce_parameter_types
    def data_type(self: "Self", value: "_1566.HarmonicLoadDataType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DataType", value)

    @property
    @exception_bridge
    def speed(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_float":
        """ListWithSelectedItem[float]"""
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_float",
        )(temp)

    @speed.setter
    @exception_bridge
    @enforce_parameter_types
    def speed(self: "Self", value: "float") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_float.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Speed", value)

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicLoadDataImportFromMotorPackages":
        """Cast to another type.

        Returns:
            _Cast_HarmonicLoadDataImportFromMotorPackages
        """
        return _Cast_HarmonicLoadDataImportFromMotorPackages(self)
