"""FESubstructureWithBatchOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_FE_SUBSTRUCTURE_WITH_BATCH_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FESubstructureWithBatchOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe import _2605

    Self = TypeVar("Self", bound="FESubstructureWithBatchOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FESubstructureWithBatchOptions._Cast_FESubstructureWithBatchOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructureWithBatchOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructureWithBatchOptions:
    """Special nested class for casting FESubstructureWithBatchOptions to subclasses."""

    __parent__: "FESubstructureWithBatchOptions"

    @property
    def fe_substructure_with_batch_options(
        self: "CastSelf",
    ) -> "FESubstructureWithBatchOptions":
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
class FESubstructureWithBatchOptions(_0.APIBase):
    """FESubstructureWithBatchOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE_WITH_BATCH_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fe_substructure(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FESubstructure")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def load_mesh_and_vectors(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LoadMeshAndVectors")

        if temp is None:
            return False

        return temp

    @load_mesh_and_vectors.setter
    @exception_bridge
    @enforce_parameter_types
    def load_mesh_and_vectors(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LoadMeshAndVectors",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def load_mesh(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LoadMesh")

        if temp is None:
            return False

        return temp

    @load_mesh.setter
    @exception_bridge
    @enforce_parameter_types
    def load_mesh(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "LoadMesh", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def load_vectors(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LoadVectors")

        if temp is None:
            return False

        return temp

    @load_vectors.setter
    @exception_bridge
    @enforce_parameter_types
    def load_vectors(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "LoadVectors", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def run_condensation(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RunCondensation")

        if temp is None:
            return False

        return temp

    @run_condensation.setter
    @exception_bridge
    @enforce_parameter_types
    def run_condensation(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "RunCondensation", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def unload_mesh(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UnloadMesh")

        if temp is None:
            return False

        return temp

    @unload_mesh.setter
    @exception_bridge
    @enforce_parameter_types
    def unload_mesh(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UnloadMesh", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def unload_vectors(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UnloadVectors")

        if temp is None:
            return False

        return temp

    @unload_vectors.setter
    @exception_bridge
    @enforce_parameter_types
    def unload_vectors(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UnloadVectors", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def fe(self: "Self") -> "_2605.FESubstructure":
        """mastapy.system_model.fe.FESubstructure

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FE")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FESubstructureWithBatchOptions":
        """Cast to another type.

        Returns:
            _Cast_FESubstructureWithBatchOptions
        """
        return _Cast_FESubstructureWithBatchOptions(self)
