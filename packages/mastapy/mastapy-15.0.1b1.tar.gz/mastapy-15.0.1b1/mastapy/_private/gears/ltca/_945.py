"""GearMeshLoadDistributionAtRotation"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEAR_MESH_LOAD_DISTRIBUTION_AT_ROTATION = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearMeshLoadDistributionAtRotation"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.ltca import _946, _952
    from mastapy._private.gears.ltca.conical import _974
    from mastapy._private.gears.ltca.cylindrical import _964

    Self = TypeVar("Self", bound="GearMeshLoadDistributionAtRotation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshLoadDistributionAtRotation._Cast_GearMeshLoadDistributionAtRotation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshLoadDistributionAtRotation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshLoadDistributionAtRotation:
    """Special nested class for casting GearMeshLoadDistributionAtRotation to subclasses."""

    __parent__: "GearMeshLoadDistributionAtRotation"

    @property
    def cylindrical_mesh_load_distribution_at_rotation(
        self: "CastSelf",
    ) -> "_964.CylindricalMeshLoadDistributionAtRotation":
        from mastapy._private.gears.ltca.cylindrical import _964

        return self.__parent__._cast(_964.CylindricalMeshLoadDistributionAtRotation)

    @property
    def conical_mesh_load_distribution_at_rotation(
        self: "CastSelf",
    ) -> "_974.ConicalMeshLoadDistributionAtRotation":
        from mastapy._private.gears.ltca.conical import _974

        return self.__parent__._cast(_974.ConicalMeshLoadDistributionAtRotation)

    @property
    def gear_mesh_load_distribution_at_rotation(
        self: "CastSelf",
    ) -> "GearMeshLoadDistributionAtRotation":
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
class GearMeshLoadDistributionAtRotation(_0.APIBase):
    """GearMeshLoadDistributionAtRotation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_LOAD_DISTRIBUTION_AT_ROTATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Index")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def mesh_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_loaded_teeth(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfLoadedTeeth")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_potentially_loaded_teeth(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfPotentiallyLoadedTeeth")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def transmission_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TransmissionError")

        if temp is None:
            return 0.0

        return temp

    @transmission_error.setter
    @exception_bridge
    @enforce_parameter_types
    def transmission_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TransmissionError",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def gear_a_in_mesh(
        self: "Self",
    ) -> "_952.MeshedGearLoadDistributionAnalysisAtRotation":
        """mastapy.gears.ltca.MeshedGearLoadDistributionAnalysisAtRotation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearAInMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_b_in_mesh(
        self: "Self",
    ) -> "_952.MeshedGearLoadDistributionAnalysisAtRotation":
        """mastapy.gears.ltca.MeshedGearLoadDistributionAnalysisAtRotation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBInMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def loaded_contact_lines(self: "Self") -> "List[_946.GearMeshLoadedContactLine]":
        """List[mastapy.gears.ltca.GearMeshLoadedContactLine]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedContactLines")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshed_gears(
        self: "Self",
    ) -> "List[_952.MeshedGearLoadDistributionAnalysisAtRotation]":
        """List[mastapy.gears.ltca.MeshedGearLoadDistributionAnalysisAtRotation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGears")

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
    def cast_to(self: "Self") -> "_Cast_GearMeshLoadDistributionAtRotation":
        """Cast to another type.

        Returns:
            _Cast_GearMeshLoadDistributionAtRotation
        """
        return _Cast_GearMeshLoadDistributionAtRotation(self)
