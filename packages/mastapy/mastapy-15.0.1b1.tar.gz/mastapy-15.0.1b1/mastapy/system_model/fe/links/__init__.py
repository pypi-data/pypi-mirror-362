"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.links._2643 import FELink
    from mastapy._private.system_model.fe.links._2644 import ElectricMachineStatorFELink
    from mastapy._private.system_model.fe.links._2645 import FELinkWithSelection
    from mastapy._private.system_model.fe.links._2646 import GearMeshFELink
    from mastapy._private.system_model.fe.links._2647 import (
        GearWithDuplicatedMeshesFELink,
    )
    from mastapy._private.system_model.fe.links._2648 import MultiAngleConnectionFELink
    from mastapy._private.system_model.fe.links._2649 import MultiNodeConnectorFELink
    from mastapy._private.system_model.fe.links._2650 import MultiNodeFELink
    from mastapy._private.system_model.fe.links._2651 import (
        PlanetaryConnectorMultiNodeFELink,
    )
    from mastapy._private.system_model.fe.links._2652 import PlanetBasedFELink
    from mastapy._private.system_model.fe.links._2653 import PlanetCarrierFELink
    from mastapy._private.system_model.fe.links._2654 import PointLoadFELink
    from mastapy._private.system_model.fe.links._2655 import RollingRingConnectionFELink
    from mastapy._private.system_model.fe.links._2656 import ShaftHubConnectionFELink
    from mastapy._private.system_model.fe.links._2657 import SingleNodeFELink
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.links._2643": ["FELink"],
        "_private.system_model.fe.links._2644": ["ElectricMachineStatorFELink"],
        "_private.system_model.fe.links._2645": ["FELinkWithSelection"],
        "_private.system_model.fe.links._2646": ["GearMeshFELink"],
        "_private.system_model.fe.links._2647": ["GearWithDuplicatedMeshesFELink"],
        "_private.system_model.fe.links._2648": ["MultiAngleConnectionFELink"],
        "_private.system_model.fe.links._2649": ["MultiNodeConnectorFELink"],
        "_private.system_model.fe.links._2650": ["MultiNodeFELink"],
        "_private.system_model.fe.links._2651": ["PlanetaryConnectorMultiNodeFELink"],
        "_private.system_model.fe.links._2652": ["PlanetBasedFELink"],
        "_private.system_model.fe.links._2653": ["PlanetCarrierFELink"],
        "_private.system_model.fe.links._2654": ["PointLoadFELink"],
        "_private.system_model.fe.links._2655": ["RollingRingConnectionFELink"],
        "_private.system_model.fe.links._2656": ["ShaftHubConnectionFELink"],
        "_private.system_model.fe.links._2657": ["SingleNodeFELink"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FELink",
    "ElectricMachineStatorFELink",
    "FELinkWithSelection",
    "GearMeshFELink",
    "GearWithDuplicatedMeshesFELink",
    "MultiAngleConnectionFELink",
    "MultiNodeConnectorFELink",
    "MultiNodeFELink",
    "PlanetaryConnectorMultiNodeFELink",
    "PlanetBasedFELink",
    "PlanetCarrierFELink",
    "PointLoadFELink",
    "RollingRingConnectionFELink",
    "ShaftHubConnectionFELink",
    "SingleNodeFELink",
)
