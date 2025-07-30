from collections.abc import Iterable, Iterator
from itertools import combinations


def generate_subsets(it: Iterable, *, min_size: int = None, max_size: int = None) -> Iterator[Iterable]:
    """
    Generate all subsets of the given iterable with sizes between min_size and max_size.

    Parameters
    ----------
    it : Iterable
        The input iterable of elements to generate subsets from.
    min_size : int, optional
        Minimum size of subsets to generate. Defaults to 0.
    max_size : int, optional
        Maximum size of subsets to generate. Defaults to the size of the iterable.

    Yields
    ------
    Iterable
        Subsequences (tuples) of the input iterable representing subsets.
    """
    elements = tuple(it)
    if min_size is None:
        min_size = 0
    if max_size is None:
        max_size = len(elements)
    for r in range(min_size, max_size + 1):
        for c in combinations(elements, r):
            yield c


def generate_two_list_partitions(iterable: Iterable, first_list_max_size=None) -> Iterator[tuple[list, list]]:
    """
    Generate all two-list partitions of subsets of the input iterable.

    For every subset of the input iterable, generate all partitions of that subset into two lists.
    Optionally limit the size of the first list.

    Parameters
    ----------
    iterable : Iterable
        The input iterable to partition.
    first_list_max_size : int, optional
        Maximum allowed size for the first list in the partition. If None, no limit is applied.

    Yields
    ------
    tuple of (list, list)
        A tuple containing two lists representing a partition of a subset of the input iterable.
    """
    elements = list(iterable)
    n = len(elements)

    for subset_size in range(n + 1):
        for subset in combinations(elements, subset_size):
            max_part1_size = subset_size if first_list_max_size is None else min(first_list_max_size, subset_size)
            for part1_size in range(max_part1_size + 1):
                for part1 in combinations(subset, part1_size):
                    part1_set = set(part1)
                    part2 = [e for e in subset if e not in part1_set]
                    yield list(part1), part2
