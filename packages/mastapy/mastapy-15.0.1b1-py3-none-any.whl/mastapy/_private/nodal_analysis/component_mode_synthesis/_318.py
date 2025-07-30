"""ModalCMSResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
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
from mastapy._private.nodal_analysis.component_mode_synthesis import _319

_MODAL_CMS_RESULTS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis", "ModalCMSResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis.component_mode_synthesis import _315, _316

    Self = TypeVar("Self", bound="ModalCMSResults")
    CastSelf = TypeVar("CastSelf", bound="ModalCMSResults._Cast_ModalCMSResults")


__docformat__ = "restructuredtext en"
__all__ = ("ModalCMSResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModalCMSResults:
    """Special nested class for casting ModalCMSResults to subclasses."""

    __parent__: "ModalCMSResults"

    @property
    def real_cms_results(self: "CastSelf") -> "_319.RealCMSResults":
        return self.__parent__._cast(_319.RealCMSResults)

    @property
    def cms_results(self: "CastSelf") -> "_315.CMSResults":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _315

        return self.__parent__._cast(_315.CMSResults)

    @property
    def modal_cms_results(self: "CastSelf") -> "ModalCMSResults":
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
class ModalCMSResults(_319.RealCMSResults):
    """ModalCMSResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODAL_CMS_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def calculate_results(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CalculateResults")

        if temp is None:
            return False

        return temp

    @calculate_results.setter
    @exception_bridge
    @enforce_parameter_types
    def calculate_results(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CalculateResults",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def frequency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Frequency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mode_id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModeID")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def fe_results_per_section(self: "Self") -> "List[_316.FESectionResults]":
        """List[mastapy.nodal_analysis.component_mode_synthesis.FESectionResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEResultsPerSection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def calculate_strain_and_kinetic_energy(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateStrainAndKineticEnergy")

    @property
    def cast_to(self: "Self") -> "_Cast_ModalCMSResults":
        """Cast to another type.

        Returns:
            _Cast_ModalCMSResults
        """
        return _Cast_ModalCMSResults(self)
