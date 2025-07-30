"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.databases._2022 import ConnectionState
    from mastapy._private.utility.databases._2023 import Database
    from mastapy._private.utility.databases._2024 import DatabaseConnectionSettings
    from mastapy._private.utility.databases._2025 import DatabaseKey
    from mastapy._private.utility.databases._2026 import DatabaseSettings
    from mastapy._private.utility.databases._2027 import NamedDatabase
    from mastapy._private.utility.databases._2028 import NamedDatabaseItem
    from mastapy._private.utility.databases._2029 import NamedKey
    from mastapy._private.utility.databases._2030 import (
        NetworkDatabaseConnectionSettingsItem,
    )
    from mastapy._private.utility.databases._2031 import SQLDatabase
    from mastapy._private.utility.databases._2032 import VersionUpdater
    from mastapy._private.utility.databases._2033 import VersionUpdaterSelectableItem
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.databases._2022": ["ConnectionState"],
        "_private.utility.databases._2023": ["Database"],
        "_private.utility.databases._2024": ["DatabaseConnectionSettings"],
        "_private.utility.databases._2025": ["DatabaseKey"],
        "_private.utility.databases._2026": ["DatabaseSettings"],
        "_private.utility.databases._2027": ["NamedDatabase"],
        "_private.utility.databases._2028": ["NamedDatabaseItem"],
        "_private.utility.databases._2029": ["NamedKey"],
        "_private.utility.databases._2030": ["NetworkDatabaseConnectionSettingsItem"],
        "_private.utility.databases._2031": ["SQLDatabase"],
        "_private.utility.databases._2032": ["VersionUpdater"],
        "_private.utility.databases._2033": ["VersionUpdaterSelectableItem"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConnectionState",
    "Database",
    "DatabaseConnectionSettings",
    "DatabaseKey",
    "DatabaseSettings",
    "NamedDatabase",
    "NamedDatabaseItem",
    "NamedKey",
    "NetworkDatabaseConnectionSettingsItem",
    "SQLDatabase",
    "VersionUpdater",
    "VersionUpdaterSelectableItem",
)
