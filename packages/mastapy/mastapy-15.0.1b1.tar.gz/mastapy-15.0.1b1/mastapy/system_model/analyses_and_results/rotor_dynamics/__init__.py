"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4287 import (
        RotorDynamicsDrawStyle,
    )
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4288 import (
        ShaftComplexShape,
    )
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4289 import (
        ShaftForcedComplexShape,
    )
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4290 import (
        ShaftModalComplexShape,
    )
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4291 import (
        ShaftModalComplexShapeAtSpeeds,
    )
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4292 import (
        ShaftModalComplexShapeAtStiffness,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.rotor_dynamics._4287": [
            "RotorDynamicsDrawStyle"
        ],
        "_private.system_model.analyses_and_results.rotor_dynamics._4288": [
            "ShaftComplexShape"
        ],
        "_private.system_model.analyses_and_results.rotor_dynamics._4289": [
            "ShaftForcedComplexShape"
        ],
        "_private.system_model.analyses_and_results.rotor_dynamics._4290": [
            "ShaftModalComplexShape"
        ],
        "_private.system_model.analyses_and_results.rotor_dynamics._4291": [
            "ShaftModalComplexShapeAtSpeeds"
        ],
        "_private.system_model.analyses_and_results.rotor_dynamics._4292": [
            "ShaftModalComplexShapeAtStiffness"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "RotorDynamicsDrawStyle",
    "ShaftComplexShape",
    "ShaftForcedComplexShape",
    "ShaftModalComplexShape",
    "ShaftModalComplexShapeAtSpeeds",
    "ShaftModalComplexShapeAtStiffness",
)
