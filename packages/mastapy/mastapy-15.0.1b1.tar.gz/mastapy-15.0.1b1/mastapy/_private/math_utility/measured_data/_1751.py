"""OnedimensionalFunctionLookupTable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility.measured_data import _1750

_ONEDIMENSIONAL_FUNCTION_LOOKUP_TABLE = python_net_import(
    "SMT.MastaAPI.MathUtility.MeasuredData", "OnedimensionalFunctionLookupTable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1718
    from mastapy._private.utility import _1779

    Self = TypeVar("Self", bound="OnedimensionalFunctionLookupTable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="OnedimensionalFunctionLookupTable._Cast_OnedimensionalFunctionLookupTable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("OnedimensionalFunctionLookupTable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OnedimensionalFunctionLookupTable:
    """Special nested class for casting OnedimensionalFunctionLookupTable to subclasses."""

    __parent__: "OnedimensionalFunctionLookupTable"

    @property
    def lookup_table_base(self: "CastSelf") -> "_1750.LookupTableBase":
        pass

        return self.__parent__._cast(_1750.LookupTableBase)

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        from mastapy._private.utility import _1779

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def onedimensional_function_lookup_table(
        self: "CastSelf",
    ) -> "OnedimensionalFunctionLookupTable":
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
class OnedimensionalFunctionLookupTable(
    _1750.LookupTableBase["OnedimensionalFunctionLookupTable"]
):
    """OnedimensionalFunctionLookupTable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ONEDIMENSIONAL_FUNCTION_LOOKUP_TABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def lookup_table(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "LookupTable")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @lookup_table.setter
    @exception_bridge
    @enforce_parameter_types
    def lookup_table(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "LookupTable", value.wrapped)

    @property
    def cast_to(self: "Self") -> "_Cast_OnedimensionalFunctionLookupTable":
        """Cast to another type.

        Returns:
            _Cast_OnedimensionalFunctionLookupTable
        """
        return _Cast_OnedimensionalFunctionLookupTable(self)
