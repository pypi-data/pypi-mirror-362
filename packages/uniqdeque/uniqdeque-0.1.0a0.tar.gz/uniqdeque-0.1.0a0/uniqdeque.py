from collections import OrderedDict
from typing import Collection, Reversible, TypeVar, Iterator

T = TypeVar('T')


class uniqdeque(Collection[T], Reversible[T]):
    """A hybrid deque-set that maintains uniqueness and insertion order."""
    __slots__ = ('ordered_dict',)

    def __init__(self, iterable=()):
        """Initialize, optionally with initial elements.

        Args:
            iterable: Initial elements (duplicates will be removed)
        """
        self.ordered_dict = OrderedDict()  # type: OrderedDict[T, None]
        for elem in iterable:
            self.ordered_dict[elem] = None

    def __repr__(self):
        # type: () -> str
        return '%s([%s])' % (
            type(self).__name__,
            ', '.join(repr(elem) for elem in self.ordered_dict),
        )

    def __eq__(self, other):
        # type: (object) -> bool
        if not isinstance(other, uniqdeque):
            return False
        else:
            return self.ordered_dict == other.ordered_dict

    def __len__(self):
        # type: () -> int
        return len(self.ordered_dict)

    def __contains__(self, item):
        # type: (object) -> bool
        return item in self.ordered_dict

    def __iter__(self):
        # type: () -> Iterator[T]
        return iter(self.ordered_dict)

    def __reversed__(self):
        # type: () -> Iterator[T]
        return reversed(self.ordered_dict)

    def push_front(self, elem):
        # type: (T) -> None
        """Add element to front if not already present."""
        if elem in self.ordered_dict:
            return
        self.ordered_dict[elem] = None
        self.ordered_dict.move_to_end(elem, False)

    def push_back(self, elem):
        # type: (T) -> None
        """Add element to back if not already present."""
        self.ordered_dict[elem] = None

    def pop_front(self):
        # type: () -> T
        """Remove and return front element.

        Raises:
            KeyError: If empty
        """
        elem, _ = self.ordered_dict.popitem(False)
        return elem

    def pop_back(self):
        # type: () -> T
        """Remove and return back element.

        Raises:
            KeyError: If empty
        """
        elem, _ = self.ordered_dict.popitem(True)
        return elem

    def discard(self, elem):
        # type: (T) -> None
        """Remove element if present."""
        self.ordered_dict.pop(elem, None)

    def clear(self):
        # type: () -> None
        """Remove all elements."""
        self.ordered_dict.clear()

    def copy(self):
        # type: () -> uniqdeque[T]
        """Return a shallow copy."""
        return uniqdeque(self.ordered_dict)
