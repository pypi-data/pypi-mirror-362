"""CylindricalGearSetHarmonicLoadData"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.static_loads import _7763

_CYLINDRICAL_GEAR_SET_HARMONIC_LOAD_DATA = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalGearSetHarmonicLoadData",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import _1564

    Self = TypeVar("Self", bound="CylindricalGearSetHarmonicLoadData")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetHarmonicLoadData._Cast_CylindricalGearSetHarmonicLoadData",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetHarmonicLoadData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetHarmonicLoadData:
    """Special nested class for casting CylindricalGearSetHarmonicLoadData to subclasses."""

    __parent__: "CylindricalGearSetHarmonicLoadData"

    @property
    def gear_set_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7763.GearSetHarmonicLoadData":
        return self.__parent__._cast(_7763.GearSetHarmonicLoadData)

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "_1564.HarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1564

        return self.__parent__._cast(_1564.HarmonicLoadDataBase)

    @property
    def cylindrical_gear_set_harmonic_load_data(
        self: "CastSelf",
    ) -> "CylindricalGearSetHarmonicLoadData":
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
class CylindricalGearSetHarmonicLoadData(_7763.GearSetHarmonicLoadData):
    """CylindricalGearSetHarmonicLoadData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_HARMONIC_LOAD_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetHarmonicLoadData":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetHarmonicLoadData
        """
        return _Cast_CylindricalGearSetHarmonicLoadData(self)
