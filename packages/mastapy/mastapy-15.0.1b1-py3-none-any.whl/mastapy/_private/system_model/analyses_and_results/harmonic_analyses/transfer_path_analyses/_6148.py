"""TransferPathAnalysisSetupOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7878
from mastapy._private.system_model.analyses_and_results.static_loads import _7674

_TRANSFER_PATH_ANALYSIS_SETUP_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.TransferPathAnalyses",
    "TransferPathAnalysisSetupOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
        _6145,
    )

    Self = TypeVar("Self", bound="TransferPathAnalysisSetupOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TransferPathAnalysisSetupOptions._Cast_TransferPathAnalysisSetupOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TransferPathAnalysisSetupOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TransferPathAnalysisSetupOptions:
    """Special nested class for casting TransferPathAnalysisSetupOptions to subclasses."""

    __parent__: "TransferPathAnalysisSetupOptions"

    @property
    def abstract_analysis_options(self: "CastSelf") -> "_7878.AbstractAnalysisOptions":
        return self.__parent__._cast(_7878.AbstractAnalysisOptions)

    @property
    def transfer_path_analysis_setup_options(
        self: "CastSelf",
    ) -> "TransferPathAnalysisSetupOptions":
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
class TransferPathAnalysisSetupOptions(
    _7878.AbstractAnalysisOptions[_7674.StaticLoadCase]
):
    """TransferPathAnalysisSetupOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRANSFER_PATH_ANALYSIS_SETUP_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def tolerance_for_rigid_body_modes(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceForRigidBodyModes")

        if temp is None:
            return 0.0

        return temp

    @tolerance_for_rigid_body_modes.setter
    @exception_bridge
    @enforce_parameter_types
    def tolerance_for_rigid_body_modes(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceForRigidBodyModes",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shafts_and_fe_parts_to_include(
        self: "Self",
    ) -> "List[_6145.ShaftOrHousingSelection]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses.ShaftOrHousingSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftsAndFEPartsToInclude")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_TransferPathAnalysisSetupOptions":
        """Cast to another type.

        Returns:
            _Cast_TransferPathAnalysisSetupOptions
        """
        return _Cast_TransferPathAnalysisSetupOptions(self)
