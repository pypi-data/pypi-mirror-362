"""CouplingConnectionLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7780

_COUPLING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CouplingConnectionLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7701,
        _7707,
        _7718,
        _7800,
        _7827,
        _7844,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2567

    Self = TypeVar("Self", bound="CouplingConnectionLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CouplingConnectionLoadCase._Cast_CouplingConnectionLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionLoadCase:
    """Special nested class for casting CouplingConnectionLoadCase to subclasses."""

    __parent__: "CouplingConnectionLoadCase"

    @property
    def inter_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7780.InterMountableComponentConnectionLoadCase":
        return self.__parent__._cast(_7780.InterMountableComponentConnectionLoadCase)

    @property
    def connection_load_case(self: "CastSelf") -> "_7718.ConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7718,
        )

        return self.__parent__._cast(_7718.ConnectionLoadCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2890.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.ConnectionAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def clutch_connection_load_case(
        self: "CastSelf",
    ) -> "_7701.ClutchConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7701,
        )

        return self.__parent__._cast(_7701.ClutchConnectionLoadCase)

    @property
    def concept_coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_7707.ConceptCouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7707,
        )

        return self.__parent__._cast(_7707.ConceptCouplingConnectionLoadCase)

    @property
    def part_to_part_shear_coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_7800.PartToPartShearCouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7800,
        )

        return self.__parent__._cast(_7800.PartToPartShearCouplingConnectionLoadCase)

    @property
    def spring_damper_connection_load_case(
        self: "CastSelf",
    ) -> "_7827.SpringDamperConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7827,
        )

        return self.__parent__._cast(_7827.SpringDamperConnectionLoadCase)

    @property
    def torque_converter_connection_load_case(
        self: "CastSelf",
    ) -> "_7844.TorqueConverterConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7844,
        )

        return self.__parent__._cast(_7844.TorqueConverterConnectionLoadCase)

    @property
    def coupling_connection_load_case(self: "CastSelf") -> "CouplingConnectionLoadCase":
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
class CouplingConnectionLoadCase(_7780.InterMountableComponentConnectionLoadCase):
    """CouplingConnectionLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2567.CouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.CouplingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionLoadCase
        """
        return _Cast_CouplingConnectionLoadCase(self)
