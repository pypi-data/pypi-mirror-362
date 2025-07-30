"""
Defines specialized argument classes for building complex pipeline queries.

This module provides the `NestedArg` class, which allows for the construction
of arguments for deeply nested searches in a fluent and expressive way. It
also defines the `SpecalArg` enum used to control the behavior of nested
argument resolution.
"""

from typing import Any, Generic, TypeVar, overload, Literal, Sequence
from enum import Enum


class SpecalArg(Enum):
    """
    Defines special behaviors for resolving `NestedArg` values.

    When a nested search has multiple levels, the arguments for each level
    (like 'name' or 'recursive') may not all be specified to the same depth.
    This enum controls how the shorter argument lists are padded to match the
    deepest list.
    """
    EXPANDLAST = "EXPANDLAST"
    """Repeats the last provided value for any remaining levels."""
    FILLDEFAULT = "FILLDEFAULT"
    """Fills any remaining levels with `DEFAULT, like lambda _: True`."""
    FILLNONE = "FILLNONE"
    """Fills any remaining levels with `None`."""
    FILLFALSE = "FILLFALSE"
    """Fills any remaining levels with `False`."""
    FILLTRUE = "FILLTRUE"
    """Fills any remaining levels with `True`."""

class Default: ...
DEFAULT = Default()

V = TypeVar("V")
class NestedArgBase(Generic[V]):
    """
    Base class for a nested argument container.

    This class holds a list of values and a special resolution strategy
    that are used to construct arguments for each step in a nested pipeline search.
    """
    def __init__(self) -> None: 
        """Initializes the NestedArgBase."""
        self.values: list[V] = []
        self.specal: SpecalArg = SpecalArg.FILLDEFAULT
    def copy(self) -> "NestedArgBase[V]":
        result = NestedArgBase()
        result.values = self.values.copy()
        result.specal = self.specal
        return result
    def __repr__(self) -> str:
        """Provides a developer-friendly string representation."""
        s = ' > '.join(map(str, self.values))
        if self.specal is not None:
            s += ' > ' + str(self.specal)
        return f"{self.__class__.__name__}({s})" 
    def __len__(self) -> int:
        """Returns the number of values currently in the argument list."""
        return self.values.__len__()
def resolve_value(values: Sequence[V | Default], 
                  specal: SpecalArg, 
                  max_n: int = -1, 
                  default: V | None = None) -> Sequence[V] | Sequence[V | None] | Sequence[V | bool] | Sequence[V | None | bool]:
    """
    Resolves a list of values to a specific length based on a special behavior.

    This function is used internally by the pipeline to ensure all argument lists
    for a nested search have the same length.

    Args:
        values: The list of values to resolve.
        specal: The special resolution strategy to apply if padding is needed.
        max_n: The target length for the list. If negative, the original list
               is returned.

    Returns:
        The resolved list of values, padded or truncated to `max_n`.

    Raises:
        ValueError: If `specal` is `EXPANDLAST` and `values` is empty.
    """
    resolved_values: list[V | None] = [default if isinstance(value, Default) else value for value in values]
    if max_n < 0: return resolved_values
    if len(resolved_values) == max_n: return resolved_values
    if len(resolved_values) > max_n: return resolved_values[:max_n]
    left: int = max_n - len(resolved_values)
    if specal == SpecalArg.EXPANDLAST:
        if len(resolved_values) == 0: 
            raise ValueError(f"{specal} can't use at first place")
        last = resolved_values[-1]
        return resolved_values + [last]*left
    if specal == SpecalArg.FILLDEFAULT:
        return resolved_values + [default]*left
    if specal == SpecalArg.FILLTRUE:
        return resolved_values + [True]*left
    if specal == SpecalArg.FILLFALSE:
        return resolved_values + [False]*left
    return resolved_values + [None]*left
class NestedArg(NestedArgBase[V]):
    """
    A fluent builder for creating a sequence of arguments for nested searches.

    This class allows users to chain values together using the `add()` or `then()` method
    or the `>>` operator to define a different argument for each level of a
    `find_nested_tag` operation.

    Example:
        # To specify names for a 3-level search:
        NestedArg().add('div').add('p').add('a')
        # Or using the operator:
        NestedArg() >> 'div' >> 'p' >> 'a'
    """
    def copy(self) -> "NestedArg[V]":
        result = NestedArg()
        result.values = self.values.copy()
        result.specal = self.specal
        return result
    @overload
    def add(self, value: SpecalArg) -> NestedArgBase[V]: ...
    @overload
    def add(self, value: V) -> "NestedArg[V]": ...
    def add(self, value: V | SpecalArg) -> "NestedArg[V] | NestedArgBase[V]":
        """
        Adds a value or a special resolution strategy to the argument list.

        Args:
            value: The argument value for the next level of the search, or
                   a `SpecalArg` to define the padding behavior.

        Returns:
            The `NestedArg` instance for further chaining, or the base class `NestedArgBase`
            if a `SpecalArg` was added.
        """
        result = self.copy()
        if isinstance(value, SpecalArg):
            result.specal = value
            return result
        result.values.append(value)
        return result
    @overload
    def then(self, value: SpecalArg) -> NestedArgBase[V]: ...
    @overload
    def then(self, value: V) -> "NestedArg[V]": ...
    def then(self, value: V | SpecalArg) -> "NestedArg[V] | NestedArgBase[V]":
        """An alias for the `add` method for a more fluent interface."""
        return self.add(value)
    @overload
    def __rshift__(self, value: SpecalArg) -> NestedArgBase[V]: ...
    @overload
    def __rshift__(self, value: V) -> "NestedArg[V]": ...
    def __rshift__(self, value: V | SpecalArg) -> "NestedArg[V] | NestedArgBase[V]": 
        """
        An alias for the `add` method using the `>>` operator for chaining.

        Args:
            value: The argument value or `SpecalArg` to add.

        Returns:
            The `NestedArg` instance for further chaining, or the base class `NestedArgBase`
            if a `SpecalArg` was added.
        """
        return self.add(value)