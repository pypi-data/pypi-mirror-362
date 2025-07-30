"""Root of the mastapy package."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private._0 import APIBase
    from mastapy._private._1 import Initialiser
    from mastapy._private._2 import LegacyV2RuntimeActivationPolicyAttributeSetter
    from mastapy._private._3 import PythonUtility
    from mastapy._private._4 import UtilityMethods
    from mastapy._private._5 import Versioning
    from mastapy._private._7894 import ConsoleProgress
    from mastapy._private._7895 import MarshalByRefObjectPermanent
    from mastapy._private._7896 import MarshalByRefObjects
    from mastapy._private._7897 import EnvironmentVariableUtility
    from mastapy._private._7898 import Remoting
    from mastapy._private._7899 import ScriptedPropertyNameAttribute
    from mastapy._private._7900 import SimpleTaskProgress
    from mastapy._private._7901 import TaskProgress
    from mastapy._private._7902 import TaskProgressWithErrorHandling
    from mastapy._private._internal import (
        Examples,
        ListWithSelectedItem,
        MeasurementType,
        TupleWithName,
        __api_version__,
        __version__,
        init,
        masta_after,
        masta_before,
        masta_licences,
        masta_property,
        overridable,
    )
    from mastapy._private._math import (
        Color,
        Long,
        Matrix2x2,
        Matrix3x3,
        Matrix4x4,
        Vector2D,
        Vector3D,
        Vector4D,
        approximately_equal,
        clamp,
        fract,
        sign,
        smoothstep,
        step,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private._internal": [
            "masta_property",
            "masta_before",
            "masta_after",
            "init",
            "__version__",
            "__api_version__",
            "TupleWithName",
            "overridable",
            "MeasurementType",
            "masta_licences",
            "Examples",
            "ListWithSelectedItem",
        ],
        "_private._math": [
            "clamp",
            "sign",
            "fract",
            "step",
            "smoothstep",
            "approximately_equal",
            "Long",
            "Vector2D",
            "Vector3D",
            "Vector4D",
            "Color",
            "Matrix2x2",
            "Matrix3x3",
            "Matrix4x4",
        ],
        "_private._0": ["APIBase"],
        "_private._1": ["Initialiser"],
        "_private._2": ["LegacyV2RuntimeActivationPolicyAttributeSetter"],
        "_private._3": ["PythonUtility"],
        "_private._4": ["UtilityMethods"],
        "_private._5": ["Versioning"],
        "_private._7894": ["ConsoleProgress"],
        "_private._7895": ["MarshalByRefObjectPermanent"],
        "_private._7896": ["MarshalByRefObjects"],
        "_private._7897": ["EnvironmentVariableUtility"],
        "_private._7898": ["Remoting"],
        "_private._7899": ["ScriptedPropertyNameAttribute"],
        "_private._7900": ["SimpleTaskProgress"],
        "_private._7901": ["TaskProgress"],
        "_private._7902": ["TaskProgressWithErrorHandling"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

    from mastapy._private._internal import mastafile_hook as __mh

    __mh()


__all__ = (
    "masta_property",
    "masta_before",
    "masta_after",
    "init",
    "__version__",
    "__api_version__",
    "TupleWithName",
    "overridable",
    "MeasurementType",
    "masta_licences",
    "Examples",
    "ListWithSelectedItem",
    "clamp",
    "sign",
    "fract",
    "step",
    "smoothstep",
    "approximately_equal",
    "Long",
    "Vector2D",
    "Vector3D",
    "Vector4D",
    "Color",
    "Matrix2x2",
    "Matrix3x3",
    "Matrix4x4",
    "APIBase",
    "Initialiser",
    "LegacyV2RuntimeActivationPolicyAttributeSetter",
    "PythonUtility",
    "UtilityMethods",
    "Versioning",
    "ConsoleProgress",
    "MarshalByRefObjectPermanent",
    "MarshalByRefObjects",
    "EnvironmentVariableUtility",
    "Remoting",
    "ScriptedPropertyNameAttribute",
    "SimpleTaskProgress",
    "TaskProgress",
    "TaskProgressWithErrorHandling",
)
