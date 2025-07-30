"""Rotor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1384

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_ROTOR = python_net_import("SMT.MastaAPI.ElectricMachines", "Rotor")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import (
        _1372,
        _1375,
        _1399,
        _1409,
        _1425,
        _1431,
        _1440,
        _1459,
    )

    Self = TypeVar("Self", bound="Rotor")
    CastSelf = TypeVar("CastSelf", bound="Rotor._Cast_Rotor")


__docformat__ = "restructuredtext en"
__all__ = ("Rotor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Rotor:
    """Special nested class for casting Rotor to subclasses."""

    __parent__: "Rotor"

    @property
    def cad_rotor(self: "CastSelf") -> "_1372.CADRotor":
        from mastapy._private.electric_machines import _1372

        return self.__parent__._cast(_1372.CADRotor)

    @property
    def cad_wound_field_synchronous_rotor(
        self: "CastSelf",
    ) -> "_1375.CADWoundFieldSynchronousRotor":
        from mastapy._private.electric_machines import _1375

        return self.__parent__._cast(_1375.CADWoundFieldSynchronousRotor)

    @property
    def interior_permanent_magnet_and_synchronous_reluctance_rotor(
        self: "CastSelf",
    ) -> "_1409.InteriorPermanentMagnetAndSynchronousReluctanceRotor":
        from mastapy._private.electric_machines import _1409

        return self.__parent__._cast(
            _1409.InteriorPermanentMagnetAndSynchronousReluctanceRotor
        )

    @property
    def permanent_magnet_rotor(self: "CastSelf") -> "_1425.PermanentMagnetRotor":
        from mastapy._private.electric_machines import _1425

        return self.__parent__._cast(_1425.PermanentMagnetRotor)

    @property
    def surface_permanent_magnet_rotor(
        self: "CastSelf",
    ) -> "_1440.SurfacePermanentMagnetRotor":
        from mastapy._private.electric_machines import _1440

        return self.__parent__._cast(_1440.SurfacePermanentMagnetRotor)

    @property
    def wound_field_synchronous_rotor(
        self: "CastSelf",
    ) -> "_1459.WoundFieldSynchronousRotor":
        from mastapy._private.electric_machines import _1459

        return self.__parent__._cast(_1459.WoundFieldSynchronousRotor)

    @property
    def rotor(self: "CastSelf") -> "Rotor":
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
class Rotor(_0.APIBase):
    """Rotor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bore(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return temp

    @bore.setter
    @exception_bridge
    @enforce_parameter_types
    def bore(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Bore", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def d_axis_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DAxisAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def d_axis_and_q_axis_convention(
        self: "Self",
    ) -> "overridable.Overridable_DQAxisConvention":
        """Overridable[mastapy.electric_machines.DQAxisConvention]"""
        temp = pythonnet_property_get(self.wrapped, "DAxisAndQAxisConvention")

        if temp is None:
            return None

        value = overridable.Overridable_DQAxisConvention.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @d_axis_and_q_axis_convention.setter
    @exception_bridge
    @enforce_parameter_types
    def d_axis_and_q_axis_convention(
        self: "Self",
        value: "Union[_1384.DQAxisConvention, Tuple[_1384.DQAxisConvention, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_DQAxisConvention.wrapper_type()
        enclosed_type = overridable.Overridable_DQAxisConvention.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DAxisAndQAxisConvention", value)

    @property
    @exception_bridge
    def initial_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InitialAngle")

        if temp is None:
            return 0.0

        return temp

    @initial_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def initial_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "InitialAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def is_skewed(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsSkewed")

        if temp is None:
            return False

        return temp

    @is_skewed.setter
    @exception_bridge
    @enforce_parameter_types
    def is_skewed(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsSkewed", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def kair(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Kair")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def magnet_flux_barrier_length(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MagnetFluxBarrierLength")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @magnet_flux_barrier_length.setter
    @exception_bridge
    @enforce_parameter_types
    def magnet_flux_barrier_length(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MagnetFluxBarrierLength", value)

    @property
    @exception_bridge
    def number_of_magnet_segments_in_axial_direction(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfMagnetSegmentsInAxialDirection"
        )

        if temp is None:
            return 0

        return temp

    @number_of_magnet_segments_in_axial_direction.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_magnet_segments_in_axial_direction(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfMagnetSegmentsInAxialDirection",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_poles(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPoles")

        if temp is None:
            return 0

        return temp

    @number_of_poles.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_poles(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfPoles", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_slices(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSlices")

        if temp is None:
            return 0

        return temp

    @number_of_slices.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_slices(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfSlices", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def polar_inertia(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PolarInertia")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rotor_length(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RotorLength")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rotor_length.setter
    @exception_bridge
    @enforce_parameter_types
    def rotor_length(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RotorLength", value)

    @property
    @exception_bridge
    def rotor_material_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "RotorMaterialDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @rotor_material_database.setter
    @exception_bridge
    @enforce_parameter_types
    def rotor_material_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "RotorMaterialDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def use_same_material_as_stator(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSameMaterialAsStator")

        if temp is None:
            return False

        return temp

    @use_same_material_as_stator.setter
    @exception_bridge
    @enforce_parameter_types
    def use_same_material_as_stator(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSameMaterialAsStator",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def field_winding_specification(
        self: "Self",
    ) -> "_1399.FieldWindingSpecificationBase":
        """mastapy.electric_machines.FieldWindingSpecificationBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FieldWindingSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def skew_slices(self: "Self") -> "List[_1431.RotorSkewSlice]":
        """List[mastapy.electric_machines.RotorSkewSlice]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SkewSlices")

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
    def cast_to(self: "Self") -> "_Cast_Rotor":
        """Cast to another type.

        Returns:
            _Cast_Rotor
        """
        return _Cast_Rotor(self)
