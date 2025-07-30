"""tuple_with_name."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Optional, Sequence


class TupleWithName(tuple):
    """Create a TupleWithName with any number of arguments and a name.

    Args:
        *args (Sequence[Any]): arguments for the tuple
        name (str, optional): An optional name for the tuple

    Note:
        The API's NamedTuple object is a tuple with a single name, which is
        different to Python's namedtuple. Therefore, this implementation
        has been named TupleWithName to make that more clear.
    """

    def __new__(cls, *args: "Sequence[Any]", name: "Optional[str]" = None):
        """Override for the new magic method."""
        return super(TupleWithName, cls).__new__(TupleWithName, args)

    def __init__(self, *args: "Sequence[Any]", name: "Optional[str]" = None):
        self._name = name

    @property
    def name(self) -> str:
        """The name of the tuple.

        Returns:
            str: the name
        """
        return self._name

    def __str__(self):
        """Override for the string magic method."""
        values = ", ".join(str(x) for x in self)
        return (
            "({}; {})".format(self.name, values) if self.name else "({})".format(values)
        )

    def __repr__(self):
        """Override for the repr magic method."""
        return "{}({}, name='{}')".format(
            self.__class__.__qualname__, ", ".join(str(x) for x in self), self.name
        )
