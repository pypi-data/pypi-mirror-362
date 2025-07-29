from typing import Iterable, Iterator, List, Optional, TypeVar, Generic, Callable
from functools import reduce
from itertools import chain

T = TypeVar("T")

class Fiterator(Generic[T], Iterator[T]):
    """A Fiterator is a simple wrapper around an iterator that lets you easily chain function calls."""

    def __init__(self, iterable: Iterable[T]) -> None:
        """Take some iterable and initialize a Fiterator."""
        self.i = iterable.__iter__()

    def filter(self, func: Callable[[T], bool]):
        """Return a new fiterator filtered with the function `func`."""
        return Fiterator(filter(func, self.i))

    S = TypeVar("S")

    def map(self, func: Callable[[T], S]):
        """Return a new fiterator mapped with the function `func`."""
        return Fiterator(map(func, self.i))

    def enumerate(self):
        """Return a new fiterator of tuple pairs consisting of the original values and their index in the iterator."""
        return Fiterator(enumerate(self.i))

    def chain(self, *iterators: Iterator):
        """Return a new fiterator that chains together two or more iterators."""
        return Fiterator(chain(self.i, *iterators))

    def collect(self) -> List[T]:
        """Collect the contents of a fiterator into a list."""
        return list(self.i)

    S = TypeVar("S")

    def reduce(self, func: Callable[[S, T], S], initial: S):
        """Reduce the values of a fiterator into one value by repeatedly calling a reducing `func`."""
        return reduce(func, self.i, initial)

    def any(self) -> bool:
        """Return True if any of the values in the iterator are truthy."""
        return any(self.i)

    def all(self) -> bool:
        """Return True if all of the values in the iterator are truthy."""
        return all(self.i)

    def find(self, needle: Callable[[T], bool]) -> Optional[T]:
        """Return the first value in the iterator for which the needle is true, otherwise return None."""
        for x in self.collect():
            if needle(x):
                return x
        return None

    def for_each(self, func: Callable[[T], None]):
        """Call the passed function `func` for each item in the iterator."""
        for x in self.i:
            func(x)

    def __next__(self):
        return self.i.__next__()


def into_iter(iterable: Iterable[T]) -> Fiterator[T]:
    """Initialize a Fiterator from an iterable."""
    return Fiterator(iterable)
