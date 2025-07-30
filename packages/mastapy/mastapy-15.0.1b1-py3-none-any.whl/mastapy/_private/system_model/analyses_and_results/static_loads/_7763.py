"""GearSetHarmonicLoadData"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.harmonic_load_data import _1564

_GEAR_SET_HARMONIC_LOAD_DATA = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearSetHarmonicLoadData"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1697
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7716,
        _7733,
        _7762,
    )

    Self = TypeVar("Self", bound="GearSetHarmonicLoadData")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetHarmonicLoadData._Cast_GearSetHarmonicLoadData"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetHarmonicLoadData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetHarmonicLoadData:
    """Special nested class for casting GearSetHarmonicLoadData to subclasses."""

    __parent__: "GearSetHarmonicLoadData"

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "_1564.HarmonicLoadDataBase":
        return self.__parent__._cast(_1564.HarmonicLoadDataBase)

    @property
    def conical_gear_set_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7716.ConicalGearSetHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7716,
        )

        return self.__parent__._cast(_7716.ConicalGearSetHarmonicLoadData)

    @property
    def cylindrical_gear_set_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7733.CylindricalGearSetHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7733,
        )

        return self.__parent__._cast(_7733.CylindricalGearSetHarmonicLoadData)

    @property
    def gear_set_harmonic_load_data(self: "CastSelf") -> "GearSetHarmonicLoadData":
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
class GearSetHarmonicLoadData(_1564.HarmonicLoadDataBase):
    """GearSetHarmonicLoadData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_HARMONIC_LOAD_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def excitation_order_as_rotational_order_of_shaft(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ExcitationOrderAsRotationalOrderOfShaft"
        )

        if temp is None:
            return 0.0

        return temp

    @excitation_order_as_rotational_order_of_shaft.setter
    @exception_bridge
    @enforce_parameter_types
    def excitation_order_as_rotational_order_of_shaft(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExcitationOrderAsRotationalOrderOfShaft",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def gear_mesh_te_order_type(self: "Self") -> "_7762.GearMeshTEOrderType":
        """mastapy.system_model.analyses_and_results.static_loads.GearMeshTEOrderType"""
        temp = pythonnet_property_get(self.wrapped, "GearMeshTEOrderType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.GearMeshTEOrderType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.static_loads._7762",
            "GearMeshTEOrderType",
        )(value)

    @gear_mesh_te_order_type.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_mesh_te_order_type(
        self: "Self", value: "_7762.GearMeshTEOrderType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.GearMeshTEOrderType",
        )
        pythonnet_property_set(self.wrapped, "GearMeshTEOrderType", value)

    @property
    @exception_bridge
    def reference_shaft(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceShaft")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @reference_shaft.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_shaft(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ReferenceShaft", value)

    @property
    @exception_bridge
    def excitations(self: "Self") -> "List[_1697.FourierSeries]":
        """List[mastapy.math_utility.FourierSeries]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Excitations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def copy_data_to_duplicate_planetary_meshes(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CopyDataToDuplicatePlanetaryMeshes")

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetHarmonicLoadData":
        """Cast to another type.

        Returns:
            _Cast_GearSetHarmonicLoadData
        """
        return _Cast_GearSetHarmonicLoadData(self)
