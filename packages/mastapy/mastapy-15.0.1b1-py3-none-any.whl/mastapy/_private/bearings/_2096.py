"""RollingBearingDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings import _2097
from mastapy._private.bearings.bearing_designs.rolling import _2375
from mastapy._private.utility.databases import _2031

_ROLLING_BEARING_TYPE = python_net_import("SMT.MastaAPI.Bearings", "RollingBearingType")
_BEARING_CATALOG = python_net_import("SMT.MastaAPI.Bearings", "BearingCatalog")
_HYBRID_STEEL_ALL = python_net_import("SMT.MastaAPI.Bearings", "HybridSteelAll")
_ROLLING_BEARING_DATABASE = python_net_import(
    "SMT.MastaAPI.Bearings", "RollingBearingDatabase"
)
_STRING = python_net_import("System", "String")
_INT_32 = python_net_import("System", "Int32")
_RANGE = python_net_import("SMT.MastaAPI.MathUtility", "Range")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar

    from mastapy._private.bearings import _2072, _2088, _2099
    from mastapy._private.utility.databases import _2023

    Self = TypeVar("Self", bound="RollingBearingDatabase")
    CastSelf = TypeVar(
        "CastSelf", bound="RollingBearingDatabase._Cast_RollingBearingDatabase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollingBearingDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingBearingDatabase:
    """Special nested class for casting RollingBearingDatabase to subclasses."""

    __parent__: "RollingBearingDatabase"

    @property
    def sql_database(self: "CastSelf") -> "_2031.SQLDatabase":
        return self.__parent__._cast(_2031.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_2023.Database":
        from mastapy._private.utility.databases import _2023

        return self.__parent__._cast(_2023.Database)

    @property
    def rolling_bearing_database(self: "CastSelf") -> "RollingBearingDatabase":
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
class RollingBearingDatabase(
    _2031.SQLDatabase[_2097.RollingBearingKey, _2375.RollingBearing]
):
    """RollingBearingDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_BEARING_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    @enforce_parameter_types
    def add_to_database(self: "Self", bearing: "_2375.RollingBearing") -> None:
        """Method does not return.

        Args:
            bearing (mastapy.bearings.bearing_designs.rolling.RollingBearing)
        """
        pythonnet_method_call(
            self.wrapped, "AddToDatabase", bearing.wrapped if bearing else None
        )

    @exception_bridge
    @enforce_parameter_types
    def create_bearing(
        self: "Self", type_: "_2099.RollingBearingType", designation: "str" = "None"
    ) -> "_2375.RollingBearing":
        """mastapy.bearings.bearing_designs.rolling.RollingBearing

        Args:
            type_ (mastapy.bearings.RollingBearingType)
            designation (str, optional)
        """
        type_ = conversion.mp_to_pn_enum(
            type_, "SMT.MastaAPI.Bearings.RollingBearingType"
        )
        designation = str(designation)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "CreateBearing",
            [_ROLLING_BEARING_TYPE, _STRING],
            type_,
            designation if designation else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def create_bearing_with_type_name(
        self: "Self", type_: "str", designation: "str" = "None"
    ) -> "_2375.RollingBearing":
        """mastapy.bearings.bearing_designs.rolling.RollingBearing

        Args:
            type_ (str)
            designation (str, optional)
        """
        type_ = str(type_)
        designation = str(designation)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "CreateBearing",
            [_STRING, _STRING],
            type_ if type_ else "",
            designation if designation else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def create_key(
        self: "Self", type_: "_2099.RollingBearingType", designation: "str" = "None"
    ) -> "_2097.RollingBearingKey":
        """mastapy.bearings.RollingBearingKey

        Args:
            type_ (mastapy.bearings.RollingBearingType)
            designation (str, optional)
        """
        type_ = conversion.mp_to_pn_enum(
            type_, "SMT.MastaAPI.Bearings.RollingBearingType"
        )
        designation = str(designation)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "CreateKey",
            [_ROLLING_BEARING_TYPE, _STRING],
            type_,
            designation if designation else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def create_key_with_type_name(
        self: "Self", type_: "str", designation: "str" = "None"
    ) -> "_2097.RollingBearingKey":
        """mastapy.bearings.RollingBearingKey

        Args:
            type_ (str)
            designation (str, optional)
        """
        type_ = str(type_)
        designation = str(designation)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "CreateKey",
            [_STRING, _STRING],
            type_ if type_ else "",
            designation if designation else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_from_database(self: "Self", bearing: "_2375.RollingBearing") -> None:
        """Method does not return.

        Args:
            bearing (mastapy.bearings.bearing_designs.rolling.RollingBearing)
        """
        pythonnet_method_call(
            self.wrapped, "RemoveFromDatabase", bearing.wrapped if bearing else None
        )

    @exception_bridge
    @enforce_parameter_types
    def search_for_rolling_bearing_with_catalog(
        self: "Self", catalog: "_2072.BearingCatalog"
    ) -> "List[_2375.RollingBearing]":
        """List[mastapy.bearings.bearing_designs.rolling.RollingBearing]

        Args:
            catalog (mastapy.bearings.BearingCatalog)
        """
        catalog = conversion.mp_to_pn_enum(
            catalog, "SMT.MastaAPI.Bearings.BearingCatalog"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_overload(
                self.wrapped, "SearchForRollingBearing", [_BEARING_CATALOG], catalog
            )
        )

    @exception_bridge
    @enforce_parameter_types
    def search_for_rolling_bearing_with_name_and_catalog(
        self: "Self", designation: "str", catalog: "_2072.BearingCatalog"
    ) -> "_2375.RollingBearing":
        """mastapy.bearings.bearing_designs.rolling.RollingBearing

        Args:
            designation (str)
            catalog (mastapy.bearings.BearingCatalog)
        """
        designation = str(designation)
        catalog = conversion.mp_to_pn_enum(
            catalog, "SMT.MastaAPI.Bearings.BearingCatalog"
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "SearchForRollingBearing",
            [_STRING, _BEARING_CATALOG],
            designation if designation else "",
            catalog,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def search_for_rolling_bearing_with_name_catalog_and_type(
        self: "Self",
        designation: "str",
        catalog: "_2072.BearingCatalog",
        type_: "_2099.RollingBearingType",
    ) -> "List[_2375.RollingBearing]":
        """List[mastapy.bearings.bearing_designs.rolling.RollingBearing]

        Args:
            designation (str)
            catalog (mastapy.bearings.BearingCatalog)
            type_ (mastapy.bearings.RollingBearingType)
        """
        designation = str(designation)
        catalog = conversion.mp_to_pn_enum(
            catalog, "SMT.MastaAPI.Bearings.BearingCatalog"
        )
        type_ = conversion.mp_to_pn_enum(
            type_, "SMT.MastaAPI.Bearings.RollingBearingType"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_overload(
                self.wrapped,
                "SearchForRollingBearing",
                [_STRING, _BEARING_CATALOG, _ROLLING_BEARING_TYPE],
                designation if designation else "",
                catalog,
                type_,
            )
        )

    @exception_bridge
    @enforce_parameter_types
    def search_for_rolling_bearing(
        self: "Self",
        designation: "str",
        catalog: "_2072.BearingCatalog",
        type_: "_2099.RollingBearingType",
        bore_range: "Tuple[float, float]",
        outer_diameter_range: "Tuple[float, float]",
        width_range: "Tuple[float, float]",
        dynamic_capacity_range: "Tuple[float, float]",
        number_of_rows: "int",
        material_type: "_2088.HybridSteelAll",
    ) -> "List[_2375.RollingBearing]":
        """List[mastapy.bearings.bearing_designs.rolling.RollingBearing]

        Args:
            designation (str)
            catalog (mastapy.bearings.BearingCatalog)
            type_ (mastapy.bearings.RollingBearingType)
            bore_range (Tuple[float, float])
            outer_diameter_range (Tuple[float, float])
            width_range (Tuple[float, float])
            dynamic_capacity_range (Tuple[float, float])
            number_of_rows (int)
            material_type (mastapy.bearings.HybridSteelAll)
        """
        designation = str(designation)
        catalog = conversion.mp_to_pn_enum(
            catalog, "SMT.MastaAPI.Bearings.BearingCatalog"
        )
        type_ = conversion.mp_to_pn_enum(
            type_, "SMT.MastaAPI.Bearings.RollingBearingType"
        )
        bore_range = conversion.mp_to_pn_range(bore_range)
        outer_diameter_range = conversion.mp_to_pn_range(outer_diameter_range)
        width_range = conversion.mp_to_pn_range(width_range)
        dynamic_capacity_range = conversion.mp_to_pn_range(dynamic_capacity_range)
        number_of_rows = int(number_of_rows)
        material_type = conversion.mp_to_pn_enum(
            material_type, "SMT.MastaAPI.Bearings.HybridSteelAll"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_overload(
                self.wrapped,
                "SearchForRollingBearing",
                [
                    _STRING,
                    _BEARING_CATALOG,
                    _ROLLING_BEARING_TYPE,
                    _RANGE,
                    _RANGE,
                    _RANGE,
                    _RANGE,
                    _INT_32,
                    _HYBRID_STEEL_ALL,
                ],
                designation if designation else "",
                catalog,
                type_,
                bore_range,
                outer_diameter_range,
                width_range,
                dynamic_capacity_range,
                number_of_rows if number_of_rows else 0,
                material_type,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RollingBearingDatabase":
        """Cast to another type.

        Returns:
            _Cast_RollingBearingDatabase
        """
        return _Cast_RollingBearingDatabase(self)
