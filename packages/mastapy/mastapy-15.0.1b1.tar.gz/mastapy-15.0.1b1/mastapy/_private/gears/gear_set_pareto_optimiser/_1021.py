"""MicroGeometryDesignSpaceSearchChartInformation"""

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
from mastapy._private.gears.gear_set_pareto_optimiser import _1007, _1020
from mastapy._private.gears.ltca.cylindrical import _963

_MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_CHART_INFORMATION = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser",
    "MicroGeometryDesignSpaceSearchChartInformation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_set_pareto_optimiser import _1019

    Self = TypeVar("Self", bound="MicroGeometryDesignSpaceSearchChartInformation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicroGeometryDesignSpaceSearchChartInformation._Cast_MicroGeometryDesignSpaceSearchChartInformation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryDesignSpaceSearchChartInformation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicroGeometryDesignSpaceSearchChartInformation:
    """Special nested class for casting MicroGeometryDesignSpaceSearchChartInformation to subclasses."""

    __parent__: "MicroGeometryDesignSpaceSearchChartInformation"

    @property
    def chart_info_base(self: "CastSelf") -> "_1007.ChartInfoBase":
        return self.__parent__._cast(_1007.ChartInfoBase)

    @property
    def micro_geometry_design_space_search_chart_information(
        self: "CastSelf",
    ) -> "MicroGeometryDesignSpaceSearchChartInformation":
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
class MicroGeometryDesignSpaceSearchChartInformation(
    _1007.ChartInfoBase[
        _963.CylindricalGearSetLoadDistributionAnalysis,
        _1020.MicroGeometryDesignSpaceSearchCandidate,
    ]
):
    """MicroGeometryDesignSpaceSearchChartInformation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_CHART_INFORMATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def optimiser(self: "Self") -> "_1019.MicroGeometryDesignSpaceSearch":
        """mastapy.gears.gear_set_pareto_optimiser.MicroGeometryDesignSpaceSearch

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Optimiser")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MicroGeometryDesignSpaceSearchChartInformation":
        """Cast to another type.

        Returns:
            _Cast_MicroGeometryDesignSpaceSearchChartInformation
        """
        return _Cast_MicroGeometryDesignSpaceSearchChartInformation(self)
