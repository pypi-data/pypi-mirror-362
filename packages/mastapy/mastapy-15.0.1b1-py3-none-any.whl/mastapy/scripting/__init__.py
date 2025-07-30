"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.scripting._7905 import ApiEnumForAttribute
    from mastapy._private.scripting._7906 import ApiVersion
    from mastapy._private.scripting._7907 import SMTBitmap
    from mastapy._private.scripting._7909 import MastaPropertyAttribute
    from mastapy._private.scripting._7910 import PythonCommand
    from mastapy._private.scripting._7911 import ScriptingCommand
    from mastapy._private.scripting._7912 import ScriptingExecutionCommand
    from mastapy._private.scripting._7913 import ScriptingObjectCommand
    from mastapy._private.scripting._7914 import ApiVersioning
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.scripting._7905": ["ApiEnumForAttribute"],
        "_private.scripting._7906": ["ApiVersion"],
        "_private.scripting._7907": ["SMTBitmap"],
        "_private.scripting._7909": ["MastaPropertyAttribute"],
        "_private.scripting._7910": ["PythonCommand"],
        "_private.scripting._7911": ["ScriptingCommand"],
        "_private.scripting._7912": ["ScriptingExecutionCommand"],
        "_private.scripting._7913": ["ScriptingObjectCommand"],
        "_private.scripting._7914": ["ApiVersioning"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ApiEnumForAttribute",
    "ApiVersion",
    "SMTBitmap",
    "MastaPropertyAttribute",
    "PythonCommand",
    "ScriptingCommand",
    "ScriptingExecutionCommand",
    "ScriptingObjectCommand",
    "ApiVersioning",
)
