"""ConicalMeshLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.ltca import _944

_CONICAL_MESH_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Conical", "ConicalMeshLoadDistributionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1336, _1342, _1343
    from mastapy._private.gears.load_case.conical import _990
    from mastapy._private.gears.ltca.conical import _972
    from mastapy._private.gears.manufacturing.bevel import _887

    Self = TypeVar("Self", bound="ConicalMeshLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshLoadDistributionAnalysis._Cast_ConicalMeshLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshLoadDistributionAnalysis:
    """Special nested class for casting ConicalMeshLoadDistributionAnalysis to subclasses."""

    __parent__: "ConicalMeshLoadDistributionAnalysis"

    @property
    def gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_944.GearMeshLoadDistributionAnalysis":
        return self.__parent__._cast(_944.GearMeshLoadDistributionAnalysis)

    @property
    def gear_mesh_implementation_analysis(
        self: "CastSelf",
    ) -> "_1343.GearMeshImplementationAnalysis":
        from mastapy._private.gears.analysis import _1343

        return self.__parent__._cast(_1343.GearMeshImplementationAnalysis)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1342.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1342

        return self.__parent__._cast(_1342.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def conical_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "ConicalMeshLoadDistributionAnalysis":
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
class ConicalMeshLoadDistributionAnalysis(_944.GearMeshLoadDistributionAnalysis):
    """ConicalMeshLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_roll_angles(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfRollAngles")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def pinion_mean_te(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionMeanTE")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_peak_to_peak_te(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionPeakToPeakTE")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_peak_to_peak_te(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelPeakToPeakTE")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def conical_mesh_load_case(self: "Self") -> "_990.ConicalMeshLoadCase":
        """mastapy.gears.load_case.conical.ConicalMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def conical_mesh_manufacturing_analysis(
        self: "Self",
    ) -> "_887.ConicalMeshManufacturingAnalysis":
        """mastapy.gears.manufacturing.bevel.ConicalMeshManufacturingAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshManufacturingAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def meshed_gears(
        self: "Self",
    ) -> "List[_972.ConicalMeshedGearLoadDistributionAnalysis]":
        """List[mastapy.gears.ltca.conical.ConicalMeshedGearLoadDistributionAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ConicalMeshLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshLoadDistributionAnalysis
        """
        return _Cast_ConicalMeshLoadDistributionAnalysis(self)
