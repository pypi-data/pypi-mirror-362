"""ConceptCoupling"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.couplings import _2823

_CONCEPT_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCoupling"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1718
    from mastapy._private.nodal_analysis import _57, _85
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2659, _2698, _2708
    from mastapy._private.system_model.part_model.couplings import _2822

    Self = TypeVar("Self", bound="ConceptCoupling")
    CastSelf = TypeVar("CastSelf", bound="ConceptCoupling._Cast_ConceptCoupling")


__docformat__ = "restructuredtext en"
__all__ = ("ConceptCoupling",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptCoupling:
    """Special nested class for casting ConceptCoupling to subclasses."""

    __parent__: "ConceptCoupling"

    @property
    def coupling(self: "CastSelf") -> "_2823.Coupling":
        return self.__parent__._cast(_2823.Coupling)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2708.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2708

        return self.__parent__._cast(_2708.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2659

        return self.__parent__._cast(_2659.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def concept_coupling(self: "CastSelf") -> "ConceptCoupling":
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
class ConceptCoupling(_2823.Coupling):
    """ConceptCoupling

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_COUPLING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def coupling_type(self: "Self") -> "_57.CouplingType":
        """mastapy.nodal_analysis.CouplingType"""
        temp = pythonnet_property_get(self.wrapped, "CouplingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.CouplingType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._57", "CouplingType"
        )(value)

    @coupling_type.setter
    @exception_bridge
    @enforce_parameter_types
    def coupling_type(self: "Self", value: "_57.CouplingType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.CouplingType"
        )
        pythonnet_property_set(self.wrapped, "CouplingType", value)

    @property
    @exception_bridge
    def default_efficiency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DefaultEfficiency")

        if temp is None:
            return 0.0

        return temp

    @default_efficiency.setter
    @exception_bridge
    @enforce_parameter_types
    def default_efficiency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DefaultEfficiency",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def default_speed_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DefaultSpeedRatio")

        if temp is None:
            return 0.0

        return temp

    @default_speed_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def default_speed_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DefaultSpeedRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def display_tilt_in_2d_drawing(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DisplayTiltIn2DDrawing")

        if temp is None:
            return False

        return temp

    @display_tilt_in_2d_drawing.setter
    @exception_bridge
    @enforce_parameter_types
    def display_tilt_in_2d_drawing(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DisplayTiltIn2DDrawing",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def efficiency_vs_speed_ratio(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "EfficiencyVsSpeedRatio")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @efficiency_vs_speed_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def efficiency_vs_speed_ratio(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "EfficiencyVsSpeedRatio", value.wrapped)

    @property
    @exception_bridge
    def half_positioning(self: "Self") -> "_2822.ConceptCouplingHalfPositioning":
        """mastapy.system_model.part_model.couplings.ConceptCouplingHalfPositioning"""
        temp = pythonnet_property_get(self.wrapped, "HalfPositioning")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.PartModel.Couplings.ConceptCouplingHalfPositioning",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model.couplings._2822",
            "ConceptCouplingHalfPositioning",
        )(value)

    @half_positioning.setter
    @exception_bridge
    @enforce_parameter_types
    def half_positioning(
        self: "Self", value: "_2822.ConceptCouplingHalfPositioning"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.PartModel.Couplings.ConceptCouplingHalfPositioning",
        )
        pythonnet_property_set(self.wrapped, "HalfPositioning", value)

    @property
    @exception_bridge
    def halves_are_coincident(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HalvesAreCoincident")

        if temp is None:
            return False

        return temp

    @halves_are_coincident.setter
    @exception_bridge
    @enforce_parameter_types
    def halves_are_coincident(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HalvesAreCoincident",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def specify_efficiency_vs_speed_ratio(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyEfficiencyVsSpeedRatio")

        if temp is None:
            return False

        return temp

    @specify_efficiency_vs_speed_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_efficiency_vs_speed_ratio(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyEfficiencyVsSpeedRatio",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def specify_stiffness_matrix(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyStiffnessMatrix")

        if temp is None:
            return False

        return temp

    @specify_stiffness_matrix.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_stiffness_matrix(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyStiffnessMatrix",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def tilt_about_x(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltAboutX")

        if temp is None:
            return 0.0

        return temp

    @tilt_about_x.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_about_x(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltAboutX", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tilt_about_y(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltAboutY")

        if temp is None:
            return 0.0

        return temp

    @tilt_about_y.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_about_y(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltAboutY", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def torsional_damping(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TorsionalDamping")

        if temp is None:
            return 0.0

        return temp

    @torsional_damping.setter
    @exception_bridge
    @enforce_parameter_types
    def torsional_damping(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TorsionalDamping", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def translational_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TranslationalStiffness")

        if temp is None:
            return 0.0

        return temp

    @translational_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def translational_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TranslationalStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def stiffness(
        self: "Self",
    ) -> "_85.NodalMatrixEditorWrapperConceptCouplingStiffness":
        """mastapy.nodal_analysis.NodalMatrixEditorWrapperConceptCouplingStiffness

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Stiffness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptCoupling":
        """Cast to another type.

        Returns:
            _Cast_ConceptCoupling
        """
        return _Cast_ConceptCoupling(self)
