"""FEStiffness"""

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
from mastapy._private._math.vector_3d import Vector3D

_FE_STIFFNESS = python_net_import("SMT.MastaAPI.NodalAnalysis", "FEStiffness")

if TYPE_CHECKING:
    from typing import Any, List, Optional, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.ltca import _936, _938, _950
    from mastapy._private.gears.ltca.conical import _966, _968
    from mastapy._private.gears.ltca.cylindrical import _954, _956
    from mastapy._private.nodal_analysis import _82
    from mastapy._private.system_model.fe import _2605

    Self = TypeVar("Self", bound="FEStiffness")
    CastSelf = TypeVar("CastSelf", bound="FEStiffness._Cast_FEStiffness")


__docformat__ = "restructuredtext en"
__all__ = ("FEStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEStiffness:
    """Special nested class for casting FEStiffness to subclasses."""

    __parent__: "FEStiffness"

    @property
    def gear_bending_stiffness(self: "CastSelf") -> "_936.GearBendingStiffness":
        from mastapy._private.gears.ltca import _936

        return self.__parent__._cast(_936.GearBendingStiffness)

    @property
    def gear_contact_stiffness(self: "CastSelf") -> "_938.GearContactStiffness":
        from mastapy._private.gears.ltca import _938

        return self.__parent__._cast(_938.GearContactStiffness)

    @property
    def gear_stiffness(self: "CastSelf") -> "_950.GearStiffness":
        from mastapy._private.gears.ltca import _950

        return self.__parent__._cast(_950.GearStiffness)

    @property
    def cylindrical_gear_bending_stiffness(
        self: "CastSelf",
    ) -> "_954.CylindricalGearBendingStiffness":
        from mastapy._private.gears.ltca.cylindrical import _954

        return self.__parent__._cast(_954.CylindricalGearBendingStiffness)

    @property
    def cylindrical_gear_contact_stiffness(
        self: "CastSelf",
    ) -> "_956.CylindricalGearContactStiffness":
        from mastapy._private.gears.ltca.cylindrical import _956

        return self.__parent__._cast(_956.CylindricalGearContactStiffness)

    @property
    def conical_gear_bending_stiffness(
        self: "CastSelf",
    ) -> "_966.ConicalGearBendingStiffness":
        from mastapy._private.gears.ltca.conical import _966

        return self.__parent__._cast(_966.ConicalGearBendingStiffness)

    @property
    def conical_gear_contact_stiffness(
        self: "CastSelf",
    ) -> "_968.ConicalGearContactStiffness":
        from mastapy._private.gears.ltca.conical import _968

        return self.__parent__._cast(_968.ConicalGearContactStiffness)

    @property
    def fe_substructure(self: "CastSelf") -> "_2605.FESubstructure":
        from mastapy._private.system_model.fe import _2605

        return self.__parent__._cast(_2605.FESubstructure)

    @property
    def fe_stiffness(self: "CastSelf") -> "FEStiffness":
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
class FEStiffness(_0.APIBase):
    """FEStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_alignment_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialAlignmentTolerance")

        if temp is None:
            return 0.0

        return temp

    @axial_alignment_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_alignment_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AxialAlignmentTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def calculate_acceleration_force_from_mass_matrix(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CalculateAccelerationForceFromMassMatrix"
        )

        if temp is None:
            return False

        return temp

    @calculate_acceleration_force_from_mass_matrix.setter
    @exception_bridge
    @enforce_parameter_types
    def calculate_acceleration_force_from_mass_matrix(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CalculateAccelerationForceFromMassMatrix",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def frequency_of_highest_mode(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOfHighestMode")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gyroscopic_matrix_is_known(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GyroscopicMatrixIsKnown")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_grounded(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsGrounded")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_using_full_fe_model(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsUsingFullFEModel")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mass_matrix_is_known(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassMatrixIsKnown")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def number_of_internal_modes(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfInternalModes")

        if temp is None:
            return 0

        return temp

    @number_of_internal_modes.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_internal_modes(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfInternalModes",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_physical_nodes(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPhysicalNodes")

        if temp is None:
            return 0

        return temp

    @number_of_physical_nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_physical_nodes(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPhysicalNodes",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def radial_alignment_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialAlignmentTolerance")

        if temp is None:
            return 0.0

        return temp

    @radial_alignment_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_alignment_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialAlignmentTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def reason_scalar_mass_not_known(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReasonScalarMassNotKnown")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def tolerance_for_zero_frequencies(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceForZeroFrequencies")

        if temp is None:
            return 0.0

        return temp

    @tolerance_for_zero_frequencies.setter
    @exception_bridge
    @enforce_parameter_types
    def tolerance_for_zero_frequencies(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceForZeroFrequencies",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def centre_of_mass_in_local_coordinate_system(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CentreOfMassInLocalCoordinateSystem"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def mass_matrix_mn_rad_s_kg(self: "Self") -> "_82.NodalMatrix":
        """mastapy.nodal_analysis.NodalMatrix

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassMatrixMNRadSKg")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stiffness_in_fe_coordinate_system_mn_rad(self: "Self") -> "_82.NodalMatrix":
        """mastapy.nodal_analysis.NodalMatrix

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StiffnessInFECoordinateSystemMNRad"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stiffness_matrix(self: "Self") -> "_82.NodalMatrix":
        """mastapy.nodal_analysis.NodalMatrix

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessMatrix")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def set_stiffness_and_mass(
        self: "Self",
        stiffness: "_82.NodalMatrix",
        mass: Optional["_82.NodalMatrix"] = None,
    ) -> None:
        """Method does not return.

        Args:
            stiffness (mastapy.nodal_analysis.NodalMatrix)
            mass (mastapy.nodal_analysis.NodalMatrix, optional)
        """
        pythonnet_method_call(
            self.wrapped,
            "SetStiffnessAndMass",
            stiffness.wrapped if stiffness else None,
            mass.wrapped if mass else None,
        )

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
    def cast_to(self: "Self") -> "_Cast_FEStiffness":
        """Cast to another type.

        Returns:
            _Cast_FEStiffness
        """
        return _Cast_FEStiffness(self)
