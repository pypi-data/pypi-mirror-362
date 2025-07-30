"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.import_from_cad._2728 import (
        AbstractShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2729 import (
        ClutchFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2730 import (
        ComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2731 import (
        ComponentFromCADBase,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2732 import (
        ConceptBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2733 import (
        ConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2734 import (
        CylindricalGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2735 import (
        CylindricalGearInPlanetarySetFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2736 import (
        CylindricalPlanetGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2737 import (
        CylindricalRingGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2738 import (
        CylindricalSunGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2739 import (
        HousedOrMounted,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2740 import (
        MountableComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2741 import (
        PlanetShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2742 import (
        PulleyFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2743 import (
        RigidConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2744 import (
        RollingBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2745 import (
        ShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2746 import (
        ShaftFromCADAuto,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.import_from_cad._2728": [
            "AbstractShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2729": ["ClutchFromCAD"],
        "_private.system_model.part_model.import_from_cad._2730": ["ComponentFromCAD"],
        "_private.system_model.part_model.import_from_cad._2731": [
            "ComponentFromCADBase"
        ],
        "_private.system_model.part_model.import_from_cad._2732": [
            "ConceptBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2733": ["ConnectorFromCAD"],
        "_private.system_model.part_model.import_from_cad._2734": [
            "CylindricalGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2735": [
            "CylindricalGearInPlanetarySetFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2736": [
            "CylindricalPlanetGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2737": [
            "CylindricalRingGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2738": [
            "CylindricalSunGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2739": ["HousedOrMounted"],
        "_private.system_model.part_model.import_from_cad._2740": [
            "MountableComponentFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2741": [
            "PlanetShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2742": ["PulleyFromCAD"],
        "_private.system_model.part_model.import_from_cad._2743": [
            "RigidConnectorFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2744": [
            "RollingBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2745": ["ShaftFromCAD"],
        "_private.system_model.part_model.import_from_cad._2746": ["ShaftFromCADAuto"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftFromCAD",
    "ClutchFromCAD",
    "ComponentFromCAD",
    "ComponentFromCADBase",
    "ConceptBearingFromCAD",
    "ConnectorFromCAD",
    "CylindricalGearFromCAD",
    "CylindricalGearInPlanetarySetFromCAD",
    "CylindricalPlanetGearFromCAD",
    "CylindricalRingGearFromCAD",
    "CylindricalSunGearFromCAD",
    "HousedOrMounted",
    "MountableComponentFromCAD",
    "PlanetShaftFromCAD",
    "PulleyFromCAD",
    "RigidConnectorFromCAD",
    "RollingBearingFromCAD",
    "ShaftFromCAD",
    "ShaftFromCADAuto",
)
