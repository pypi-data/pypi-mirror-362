"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets.cycloidal._2554 import (
        CycloidalDiscAxialLeftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal._2555 import (
        CycloidalDiscAxialRightSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal._2556 import (
        CycloidalDiscCentralBearingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal._2557 import (
        CycloidalDiscInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal._2558 import (
        CycloidalDiscOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal._2559 import (
        CycloidalDiscPlanetaryBearingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal._2560 import (
        CycloidalDiscPlanetaryBearingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal._2561 import (
        RingPinsSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal._2562 import (
        RingPinsToDiscConnection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets.cycloidal._2554": [
            "CycloidalDiscAxialLeftSocket"
        ],
        "_private.system_model.connections_and_sockets.cycloidal._2555": [
            "CycloidalDiscAxialRightSocket"
        ],
        "_private.system_model.connections_and_sockets.cycloidal._2556": [
            "CycloidalDiscCentralBearingConnection"
        ],
        "_private.system_model.connections_and_sockets.cycloidal._2557": [
            "CycloidalDiscInnerSocket"
        ],
        "_private.system_model.connections_and_sockets.cycloidal._2558": [
            "CycloidalDiscOuterSocket"
        ],
        "_private.system_model.connections_and_sockets.cycloidal._2559": [
            "CycloidalDiscPlanetaryBearingConnection"
        ],
        "_private.system_model.connections_and_sockets.cycloidal._2560": [
            "CycloidalDiscPlanetaryBearingSocket"
        ],
        "_private.system_model.connections_and_sockets.cycloidal._2561": [
            "RingPinsSocket"
        ],
        "_private.system_model.connections_and_sockets.cycloidal._2562": [
            "RingPinsToDiscConnection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CycloidalDiscAxialLeftSocket",
    "CycloidalDiscAxialRightSocket",
    "CycloidalDiscCentralBearingConnection",
    "CycloidalDiscInnerSocket",
    "CycloidalDiscOuterSocket",
    "CycloidalDiscPlanetaryBearingConnection",
    "CycloidalDiscPlanetaryBearingSocket",
    "RingPinsSocket",
    "RingPinsToDiscConnection",
)
