"""CylindricalGearFromCAD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item, overridable
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.gears import _2762, _2763
from mastapy._private.system_model.part_model.import_from_cad import _2740

_CYLINDRICAL_GEAR_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "CylindricalGearFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.geometry.two_d import _401
    from mastapy._private.system_model.part_model.import_from_cad import (
        _2730,
        _2731,
        _2735,
        _2736,
        _2737,
        _2738,
    )

    Self = TypeVar("Self", bound="CylindricalGearFromCAD")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearFromCAD._Cast_CylindricalGearFromCAD"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFromCAD:
    """Special nested class for casting CylindricalGearFromCAD to subclasses."""

    __parent__: "CylindricalGearFromCAD"

    @property
    def mountable_component_from_cad(
        self: "CastSelf",
    ) -> "_2740.MountableComponentFromCAD":
        return self.__parent__._cast(_2740.MountableComponentFromCAD)

    @property
    def component_from_cad(self: "CastSelf") -> "_2730.ComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2730

        return self.__parent__._cast(_2730.ComponentFromCAD)

    @property
    def component_from_cad_base(self: "CastSelf") -> "_2731.ComponentFromCADBase":
        from mastapy._private.system_model.part_model.import_from_cad import _2731

        return self.__parent__._cast(_2731.ComponentFromCADBase)

    @property
    def cylindrical_gear_in_planetary_set_from_cad(
        self: "CastSelf",
    ) -> "_2735.CylindricalGearInPlanetarySetFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2735

        return self.__parent__._cast(_2735.CylindricalGearInPlanetarySetFromCAD)

    @property
    def cylindrical_planet_gear_from_cad(
        self: "CastSelf",
    ) -> "_2736.CylindricalPlanetGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2736

        return self.__parent__._cast(_2736.CylindricalPlanetGearFromCAD)

    @property
    def cylindrical_ring_gear_from_cad(
        self: "CastSelf",
    ) -> "_2737.CylindricalRingGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2737

        return self.__parent__._cast(_2737.CylindricalRingGearFromCAD)

    @property
    def cylindrical_sun_gear_from_cad(
        self: "CastSelf",
    ) -> "_2738.CylindricalSunGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2738

        return self.__parent__._cast(_2738.CylindricalSunGearFromCAD)

    @property
    def cylindrical_gear_from_cad(self: "CastSelf") -> "CylindricalGearFromCAD":
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
class CylindricalGearFromCAD(_2740.MountableComponentFromCAD):
    """CylindricalGearFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cad_drawing_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CADDrawingDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def centre_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CentreDistance")

        if temp is None:
            return 0.0

        return temp

    @centre_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def centre_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CentreDistance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def existing_gear_set(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_CylindricalGearSet":
        """ListWithSelectedItem[mastapy.system_model.part_model.gears.CylindricalGearSet]"""
        temp = pythonnet_property_get(self.wrapped, "ExistingGearSet")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_CylindricalGearSet",
        )(temp)

    @existing_gear_set.setter
    @exception_bridge
    @enforce_parameter_types
    def existing_gear_set(self: "Self", value: "_2763.CylindricalGearSet") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_CylindricalGearSet.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ExistingGearSet", value)

    @property
    @exception_bridge
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def gear_set_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "GearSetName")

        if temp is None:
            return ""

        return temp

    @gear_set_name.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_set_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "GearSetName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def helix_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HelixAngle")

        if temp is None:
            return 0.0

        return temp

    @helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HelixAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def internal_external(self: "Self") -> "_401.InternalExternalType":
        """mastapy.geometry.two_d.InternalExternalType"""
        temp = pythonnet_property_get(self.wrapped, "InternalExternal")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Geometry.TwoD.InternalExternalType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.geometry.two_d._401", "InternalExternalType"
        )(value)

    @internal_external.setter
    @exception_bridge
    @enforce_parameter_types
    def internal_external(self: "Self", value: "_401.InternalExternalType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Geometry.TwoD.InternalExternalType"
        )
        pythonnet_property_set(self.wrapped, "InternalExternal", value)

    @property
    @exception_bridge
    def meshing_gear(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_CylindricalGear":
        """ListWithSelectedItem[mastapy.system_model.part_model.gears.CylindricalGear]"""
        temp = pythonnet_property_get(self.wrapped, "MeshingGear")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_CylindricalGear",
        )(temp)

    @meshing_gear.setter
    @exception_bridge
    @enforce_parameter_types
    def meshing_gear(self: "Self", value: "_2762.CylindricalGear") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_CylindricalGear.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "MeshingGear", value)

    @property
    @exception_bridge
    def normal_module(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NormalModule")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @normal_module.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_module(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NormalModule", value)

    @property
    @exception_bridge
    def normal_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_teeth(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_teeth(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfTeeth", value)

    @property
    @exception_bridge
    def root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFromCAD":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFromCAD
        """
        return _Cast_CylindricalGearFromCAD(self)
