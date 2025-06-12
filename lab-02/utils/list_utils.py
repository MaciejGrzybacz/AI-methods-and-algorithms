from typing import TypeVar, Callable, Iterator, Iterable, Sequence

T = TypeVar('T')


def split(collection: list[T], test: Callable[[T], bool]) -> tuple[list[T], list[T]]:
    """Splits list into two parts based on a test function.

    :param collection: list to split.
    :param test: function used to test the collection elements
    :return: a tuple, where the first element is a list of elements satisfying the test,
             and the second is a list containing the elements failing the tests.
    """
    passed: list[T] = list()
    failed: list[T] = list()
    for element in collection:
        if test(element):
            passed.append(element)
        else:
            failed.append(element)
    return passed, failed


def pairs(collection: Sequence[T]) -> Iterator[tuple[T, T]]:
    """
    Yields all possible pairs of elements of a sequence.
    """
    for i, e1 in enumerate(collection):
        for e2 in collection[i + 1:]:
            yield e1, e2


