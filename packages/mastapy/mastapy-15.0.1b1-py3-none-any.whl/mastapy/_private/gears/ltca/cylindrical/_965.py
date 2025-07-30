"""FaceGearSetLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.ltca.cylindrical import _963

_FACE_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Cylindrical", "FaceGearSetLoadDistributionAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1337, _1346, _1348, _1349
    from mastapy._private.gears.ltca import _949

    Self = TypeVar("Self", bound="FaceGearSetLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FaceGearSetLoadDistributionAnalysis._Cast_FaceGearSetLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearSetLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearSetLoadDistributionAnalysis:
    """Special nested class for casting FaceGearSetLoadDistributionAnalysis to subclasses."""

    __parent__: "FaceGearSetLoadDistributionAnalysis"

    @property
    def cylindrical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_963.CylindricalGearSetLoadDistributionAnalysis":
        return self.__parent__._cast(_963.CylindricalGearSetLoadDistributionAnalysis)

    @property
    def gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_949.GearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _949

        return self.__parent__._cast(_949.GearSetLoadDistributionAnalysis)

    @property
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "_1348.GearSetImplementationAnalysis":
        from mastapy._private.gears.analysis import _1348

        return self.__parent__._cast(_1348.GearSetImplementationAnalysis)

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "_1349.GearSetImplementationAnalysisAbstract":
        from mastapy._private.gears.analysis import _1349

        return self.__parent__._cast(_1349.GearSetImplementationAnalysisAbstract)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1346.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1346

        return self.__parent__._cast(_1346.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

    @property
    def face_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "FaceGearSetLoadDistributionAnalysis":
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
class FaceGearSetLoadDistributionAnalysis(
    _963.CylindricalGearSetLoadDistributionAnalysis
):
    """FaceGearSetLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearSetLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_FaceGearSetLoadDistributionAnalysis
        """
        return _Cast_FaceGearSetLoadDistributionAnalysis(self)
