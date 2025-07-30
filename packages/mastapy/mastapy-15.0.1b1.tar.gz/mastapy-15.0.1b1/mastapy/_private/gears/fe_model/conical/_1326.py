"""ConicalSetFEModel"""

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
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.fe_model import _1320
from mastapy._private.gears.manufacturing.bevel import _894

_CONICAL_SET_FE_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.FEModel.Conical", "ConicalSetFEModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1337, _1346, _1351
    from mastapy._private.gears.fe_model.conical import _1327
    from mastapy._private.nodal_analysis import _61

    Self = TypeVar("Self", bound="ConicalSetFEModel")
    CastSelf = TypeVar("CastSelf", bound="ConicalSetFEModel._Cast_ConicalSetFEModel")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalSetFEModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalSetFEModel:
    """Special nested class for casting ConicalSetFEModel to subclasses."""

    __parent__: "ConicalSetFEModel"

    @property
    def gear_set_fe_model(self: "CastSelf") -> "_1320.GearSetFEModel":
        return self.__parent__._cast(_1320.GearSetFEModel)

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1351.GearSetImplementationDetail":
        from mastapy._private.gears.analysis import _1351

        return self.__parent__._cast(_1351.GearSetImplementationDetail)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1346.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1346

        return self.__parent__._cast(_1346.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

    @property
    def conical_set_fe_model(self: "CastSelf") -> "ConicalSetFEModel":
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
class ConicalSetFEModel(_1320.GearSetFEModel):
    """ConicalSetFEModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_SET_FE_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def element_order(self: "Self") -> "_61.ElementOrder":
        """mastapy.nodal_analysis.ElementOrder"""
        temp = pythonnet_property_get(self.wrapped, "ElementOrder")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.ElementOrder"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._61", "ElementOrder"
        )(value)

    @element_order.setter
    @exception_bridge
    @enforce_parameter_types
    def element_order(self: "Self", value: "_61.ElementOrder") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.ElementOrder"
        )
        pythonnet_property_set(self.wrapped, "ElementOrder", value)

    @property
    @exception_bridge
    def flank_data_source(self: "Self") -> "_1327.FlankDataSource":
        """mastapy.gears.fe_model.conical.FlankDataSource"""
        temp = pythonnet_property_get(self.wrapped, "FlankDataSource")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.FEModel.Conical.FlankDataSource"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.fe_model.conical._1327", "FlankDataSource"
        )(value)

    @flank_data_source.setter
    @exception_bridge
    @enforce_parameter_types
    def flank_data_source(self: "Self", value: "_1327.FlankDataSource") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.FEModel.Conical.FlankDataSource"
        )
        pythonnet_property_set(self.wrapped, "FlankDataSource", value)

    @property
    @exception_bridge
    def selected_design(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig":
        """ListWithSelectedItem[mastapy.gears.manufacturing.bevel.ConicalSetManufacturingConfig]"""
        temp = pythonnet_property_get(self.wrapped, "SelectedDesign")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_ConicalSetManufacturingConfig",
        )(temp)

    @selected_design.setter
    @exception_bridge
    @enforce_parameter_types
    def selected_design(
        self: "Self", value: "_894.ConicalSetManufacturingConfig"
    ) -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "SelectedDesign", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalSetFEModel":
        """Cast to another type.

        Returns:
            _Cast_ConicalSetFEModel
        """
        return _Cast_ConicalSetFEModel(self)
