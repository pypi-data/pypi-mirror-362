"""Module with simplified licence functionality."""

from __future__ import annotations

import contextlib
import functools
import urllib.error
import urllib.request
from contextlib import ContextDecorator
from dataclasses import dataclass
from types import TracebackType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable, Optional, Tuple, Type, TypeVar

    from mastapy.licensing import LicenceServerDetails

    Self = TypeVar("Self", bound="_MastaLicencesContextDecorator")
    T = TypeVar("T")
    DecoratorMethod = Callable[..., T]


__all__ = ("masta_licences", "LicenceRequestFailureException")


class LicenceRequestFailureException(Exception):
    """Exception raised when licences fail to be acquired."""


@dataclass(frozen=True)
class _MastaLicencesContextDecorator(ContextDecorator):
    modules: "Tuple[str, ...]"
    server_details: "Optional[LicenceServerDetails]" = None
    ip: str = ""
    port: int = 5053
    web_port: int = 5054
    licence_groups_ip: str = ""
    licence_groups_port: int = 5101

    @property
    @functools.lru_cache(maxsize=None)
    def _specified_ip(self: "Self") -> bool:
        return self.ip or self.licence_groups_ip

    def __call__(self: "Self", func: "DecoratorMethod") -> "DecoratorMethod":
        """Call override."""

        @functools.wraps(func)
        def wrapper_masta_licences(*args: Any, **kwargs: Any) -> T:
            with self._recreate_cm():
                return func(*args, **kwargs)

        return wrapper_masta_licences

    def __enter__(self: "Self") -> "Self":
        """Enter override."""
        from mastapy.licensing import LicenceServer, LicenceServerDetails

        if self.server_details is not None:
            LicenceServer.update_server_settings(self.server_details)
        elif self._specified_ip:
            new_server_details = LicenceServerDetails()
            new_server_details.ip = self.ip or self.licence_groups_ip
            new_server_details.port = self.port
            new_server_details.web_port = self.web_port
            new_server_details.licence_groups_ip = self.licence_groups_ip or self.ip
            new_server_details.licence_groups_port = self.licence_groups_port
            LicenceServer.update_server_settings(new_server_details)

        if not LicenceServer.request_modules(self.modules):
            server_details = LicenceServer.get_server_settings()

            if not server_details.has_ip:
                raise LicenceRequestFailureException(
                    "Attempted to request licences with an undefined server IP. Either "
                    'set the "ip" parameter or use '
                    "LicenceServer.update_server_settings(...)"
                ) from None

            server_address = server_details.ip

            if server_details.has_port:
                server_address += f":{server_details.port}"

            for server_url in (f"http://{server_address}", f"https://{server_address}"):
                with contextlib.suppress(urllib.error.URLError), urllib.request.urlopen(
                    server_url
                ):
                    break
            else:
                raise LicenceRequestFailureException(
                    f"Failed to get a response from licence server ({server_address}). "
                    "Check that your licence server settings are correct and that the "
                    "licence server is online."
                ) from None

            raise LicenceRequestFailureException(
                "Failed to acquire licences. There is either a problem with the "
                f"licence server ({server_address}) or the requested licences are not "
                "available."
            ) from None

        return self

    def __exit__(
        self: "Self",
        exc_type: "Optional[Type[BaseException]]",
        exc: "Optional[BaseException]",
        traceback: "Optional[TracebackType]",
    ) -> bool:
        """Exit override."""
        from mastapy.licensing import LicenceServer

        LicenceServer.remove_modules(self.modules)
        return False


def masta_licences(
    *modules: str,
    server_details: "Optional[LicenceServerDetails]" = None,
    ip: str = "",
    port: int = 5053,
    web_port: int = 5054,
    licence_groups_ip: str = "",
    licence_groups_port: int = 5101,
) -> _MastaLicencesContextDecorator:
    """Acquire and remove licences using a decorator or context manager.

    Note:
        This decorator/context manager acquires licences when entering scope
        *and* removes licences when exiting scope. If no keyword
        arguments are overridden then the server settings will not be
        updated. If server_details is specified all other keyword arguments
        will be ignored.

    Note:
        licence_groups_ip will copy the value of ip and vice-versa if either
        has not been set.

    Examples:
        This can be used as a decorator:

            >>> from mastapy import masta_licences
            >>> @masta_licences('MC101', server_details=my_server_details)
            >>> def my_method():
            >>>     ...

        It can also be used as a context manager:

            >>> from mastapy import masta_licences
            >>> def my_method():
            >>>     with masta_licences('MC101', ip='localhost'):
            >>>         ...

            Note that in the above example, all other keyword arguments besides
            "ip" will use the defaults.

    Args:
        *modules (str): Modules to acquire.
        server_details (LicenceServerDetails, optional): Server details for
            licences. If set, all optional keyword arguments will be ignored.
            Default is None.
        ip (str, optional): IP of the server. Default is an empty string.
        port (int, optional): Port of the server. Default is 5053.
        web_port (int, optional): Web Port of the server. Default is 5054.
        licence_groups_ip (str, optional): Licence Groups IP of the server.
            Default is an empty string.
        licence_groups_port (int, optional): Licence Groups Port of the server.
            Default is 5101.

    Returns:
        _MastaLicencesContextDecorator
    """
    return _MastaLicencesContextDecorator(
        modules=modules,
        server_details=server_details,
        ip=ip,
        port=port,
        web_port=web_port,
        licence_groups_ip=licence_groups_ip,
        licence_groups_port=licence_groups_port,
    )
