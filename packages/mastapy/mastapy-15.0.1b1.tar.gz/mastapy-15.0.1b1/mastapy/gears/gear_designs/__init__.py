"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs._1044 import (
        BevelHypoidGearDesignSettingsDatabase,
    )
    from mastapy._private.gears.gear_designs._1045 import (
        BevelHypoidGearDesignSettingsItem,
    )
    from mastapy._private.gears.gear_designs._1046 import (
        BevelHypoidGearRatingSettingsDatabase,
    )
    from mastapy._private.gears.gear_designs._1047 import (
        BevelHypoidGearRatingSettingsItem,
    )
    from mastapy._private.gears.gear_designs._1048 import DesignConstraint
    from mastapy._private.gears.gear_designs._1049 import (
        DesignConstraintCollectionDatabase,
    )
    from mastapy._private.gears.gear_designs._1050 import DesignConstraintsCollection
    from mastapy._private.gears.gear_designs._1051 import GearDesign
    from mastapy._private.gears.gear_designs._1052 import GearDesignComponent
    from mastapy._private.gears.gear_designs._1053 import GearMeshDesign
    from mastapy._private.gears.gear_designs._1054 import GearSetDesign
    from mastapy._private.gears.gear_designs._1055 import (
        SelectedDesignConstraintsCollection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs._1044": ["BevelHypoidGearDesignSettingsDatabase"],
        "_private.gears.gear_designs._1045": ["BevelHypoidGearDesignSettingsItem"],
        "_private.gears.gear_designs._1046": ["BevelHypoidGearRatingSettingsDatabase"],
        "_private.gears.gear_designs._1047": ["BevelHypoidGearRatingSettingsItem"],
        "_private.gears.gear_designs._1048": ["DesignConstraint"],
        "_private.gears.gear_designs._1049": ["DesignConstraintCollectionDatabase"],
        "_private.gears.gear_designs._1050": ["DesignConstraintsCollection"],
        "_private.gears.gear_designs._1051": ["GearDesign"],
        "_private.gears.gear_designs._1052": ["GearDesignComponent"],
        "_private.gears.gear_designs._1053": ["GearMeshDesign"],
        "_private.gears.gear_designs._1054": ["GearSetDesign"],
        "_private.gears.gear_designs._1055": ["SelectedDesignConstraintsCollection"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BevelHypoidGearDesignSettingsDatabase",
    "BevelHypoidGearDesignSettingsItem",
    "BevelHypoidGearRatingSettingsDatabase",
    "BevelHypoidGearRatingSettingsItem",
    "DesignConstraint",
    "DesignConstraintCollectionDatabase",
    "DesignConstraintsCollection",
    "GearDesign",
    "GearDesignComponent",
    "GearMeshDesign",
    "GearSetDesign",
    "SelectedDesignConstraintsCollection",
)
