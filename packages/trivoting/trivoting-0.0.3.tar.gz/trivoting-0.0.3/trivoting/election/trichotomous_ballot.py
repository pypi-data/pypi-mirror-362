from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Collection

from trivoting.election.alternative import Alternative

class AbstractTrichotomousBallot(ABC):
    """
    Abstract base class for a trichotomous ballot.

    A trichotomous ballot partitions alternatives into approved and disapproved sets,
    with the implicit third category being neutral or unknown.

    Subclasses must implement the `approved` and `disapproved` properties.
    """

    @property
    @abstractmethod
    def approved(self) -> Collection[Alternative]:
        pass

    @property
    @abstractmethod
    def disapproved(self) -> Collection[Alternative]:
        pass

class TrichotomousBallot(AbstractTrichotomousBallot):
    """
    Represents a mutable trichotomous ballot, where alternatives are categorized into approved, disapproved, or
    implicitly neutral.

    Parameters
    ----------
    approved : Iterable[Alternative], optional
        Approved alternatives.
    disapproved : Iterable[Alternative], optional
        Disapproved alternatives.

    Attributes
    ----------
    approved : set[Alternative]
        The alternatives the voter approves of.
    disapproved : set[Alternative]
        The alternatives the voter disapproves of.
    """

    def __init__(self, *, approved: Iterable[Alternative] = None, disapproved: Iterable[Alternative] = None):
        if approved is None:
            self._approved = set()
        else:
            self._approved = set(approved)

        if disapproved is None:
            self._disapproved = set()
        else:
            self._disapproved = set(disapproved)

        AbstractTrichotomousBallot.__init__(self)

    @property
    def approved(self) -> set[Alternative]:
        """Set of approved alternatives."""
        return self._approved

    @approved.setter
    def approved(self, value: Iterable[Alternative]):
        self._approved = set(value)

    @property
    def disapproved(self) -> set[Alternative]:
        """Set of disapproved alternatives."""
        return self._disapproved

    @disapproved.setter
    def disapproved(self, value: Iterable[Alternative]):
        self._disapproved = set(value)

    def add_approved(self, alt: Alternative) -> None:
        """
        Add an alternative to the approved set.

        Parameters
        ----------
        alt : Alternative
            The alternative to approve.
        """
        self.approved.add(alt)

    def add_disapproved(self, alt: Alternative) -> None:
        """
        Add an alternative to the disapproved set.

        Parameters
        ----------
        alt : Alternative
            The alternative to disapprove.
        """
        self.disapproved.add(alt)

    def freeze(self) -> FrozenTrichotomousBallot:
        """
        Return an immutable version of this ballot.

        Returns
        -------
        FrozenTrichotomousBallot
            A frozen (immutable) copy of this ballot.
        """
        return FrozenTrichotomousBallot(
            approved=self.approved,
            disapproved=self.disapproved,
        )

    def __contains__(self, item):
        """
        Check if an alternative is in either the approved or disapproved sets.

        Parameters
        ----------
        item : Alternative

        Returns
        -------
        bool
        """
        return item in self.approved or item in self.disapproved

    def __len__(self):
        """
        Return the total number of alternatives in the ballot (both approved and disapproved).

        Returns
        -------
        int
        """
        return len(self.approved) + len(self.disapproved)

    def __str__(self):
        return f"{{{self.approved}}} // {{{self.disapproved}}}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, TrichotomousBallot):
            return self.approved == other.approved and self.disapproved == other.disapproved
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, TrichotomousBallot):
            return self.approved < other.approved
        return NotImplemented


class FrozenTrichotomousBallot(AbstractTrichotomousBallot):
    """
    Represents an immutable trichotomous ballot using tuples for storage.

    This version is suitable for hashing and storing in sets or as keys in dictionaries.

    Parameters
    ----------
    approved : Iterable[Alternative], optional
        Approved alternatives.
    disapproved : Iterable[Alternative], optional
        Disapproved alternatives.

    Attributes
    ----------
    approved : tuple[Alternative, ...]
        The alternatives the voter approves of.
    disapproved : tuple[Alternative, ...]
        The alternatives the voter disapproves of.
    """

    def __init__(self,  *, approved: Iterable[Alternative] = None, disapproved: Iterable[Alternative] = None):
        if approved is None:
            self._approved = tuple()
        else:
            self._approved = tuple(approved)

        if disapproved is None:
            self._disapproved = tuple()
        else:
            self._disapproved = tuple(disapproved)

        AbstractTrichotomousBallot.__init__(self)

    @property
    def approved(self) -> tuple[Alternative, ...]:
        """Tuple of approved alternatives."""
        return self._approved

    @property
    def disapproved(self) -> tuple[Alternative, ...]:
        """Tuple of disapproved alternatives."""
        return self._disapproved

    def __contains__(self, item):
        """
        Check if an alternative is in either the approved or disapproved sets.

        Parameters
        ----------
        item : Alternative

        Returns
        -------
        bool
        """
        return item in self.approved or item in self.disapproved

    def __len__(self):
        """
        Return the total number of alternatives in the ballot (both approved and disapproved).

        Returns
        -------
        int
        """
        return len(self.approved) + len(self.disapproved)

    def __str__(self):
        return f"{{{self.approved}}} // {{{self.disapproved}}}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, FrozenTrichotomousBallot):
            return self.approved == other.approved and self.disapproved == other.disapproved
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, FrozenTrichotomousBallot):
            return (self.approved, self.disapproved) < (other.approved, other.disapproved)
        return NotImplemented

    def __hash__(self):
        return hash((self.approved, self.disapproved))
