import warnings
from collections.abc import Iterable

from trivoting.election.alternative import Alternative


class Selection:
    """
    A selection is the outcome of a rule. It contains both the alternatives that have been selected and the ones that
    have been rejected.

    Parameters
    ----------
        selected : Iterable[Alternative], optional
            A collection of alternatives that are selected. Defaults to an empty list.
        rejected : Iterable[Alternative], optional
            A collection of alternatives that are explicitly rejected. Defaults to an empty list.
        implicit_reject : bool, optional
            If True, all alternatives not in `selected` are considered rejected by default.
            If False, only alternatives in `rejected` are considered rejected. Defaults to True.

    Attributes
    ----------
        selected : list of Alternative
            Alternatives that are selected.
        rejected : list of Alternative
            Alternatives that are rejected.
        implicit_reject : bool
            Whether rejection is implicit for alternatives not in the selection.
    """

    def __init__(
            self,
            selected: Iterable[Alternative] = None,
            rejected: Iterable[Alternative] = None,
            implicit_reject: bool = True
    ):
        if selected is None:
            self.selected = list()
        else:
            self.selected = list(selected)
        if rejected is None:
            self.rejected = list()
        else:
            self.rejected = list(rejected)
        self.implicit_reject = implicit_reject

    def is_selected(self, a: Alternative) -> bool:
        """
        Check whether an alternative is considered selected. Same as `a in selection.selected`.

        Parameters
        ----------
            a : Alternative
                The alternative to check.

        Returns
        -------
            bool
                True if the alternative is selected; False otherwise.
        """
        return a in self.selected

    def is_rejected(self, a: Alternative) -> bool:
        """
        Check whether an alternative is considered rejected. If `implicit_reject` is set to `True`, checks
        that the alternative is not selected. Otherwise, checks that the alternative is rejected.

        Parameters
        ----------
            a : Alternative
                The alternative to check.

        Returns
        -------
            bool
                True if the alternative is selected; False otherwise.
        """
        if self.implicit_reject:
            return a not in self.selected
        return a in self.rejected

    def add_selected(self, alt: Alternative) -> None:
        """
        Add a single alternative to the selected list.

        Parameters
        ----------
            alt : Alternative
                The alternative to add to the selection.
        """
        self.selected.append(alt)

    def extend_selected(self, alts: Iterable[Alternative]) -> None:
        """
        Extend the selected list with multiple alternatives.

        Parameters
        ----------
            alts : Iterable[Alternative]
                An iterable of alternatives to add to the selection.
        """
        self.selected.extend(alts)

    def add_rejected(self, alt: Alternative) -> None:
        """
        Add a single alternative to the rejected list. Issues a warning if `implicit_reject` is set to `True`.

        Parameters
        ----------
            alt : Alternative
                The alternative to add to the rejection list.
        """
        if self.implicit_reject:
            warnings.warn("You are adding rejected alternatives to a selection that has implicit_reject=True. The "
                          "selection may not behave as you think it does.")
        self.rejected.append(alt)

    def extend_rejected(self, alts: Iterable[Alternative]) -> None:
        """
        Extend the rejected list with multiple alternatives. Issues a warning if `implicit_reject` is set to `True`.

        Parameters
        ----------
            alts : Iterable[Alternative]
                An iterable of alternatives to add to the rejection list.
        """
        if self.implicit_reject:
            warnings.warn("You are adding rejected alternatives to a selection that has implicit_reject=True. The "
                          "selection may not behave as you think it does.")
        self.rejected.extend(alts)

    def sort(self) -> None:
        """
        Sort both selected and rejected alternatives in place.
        """
        self.selected.sort()
        self.rejected.sort()

    def copy(self) -> "Selection":
        """
        Create a copy of the current selection.

        Returns
        -------
            Selection
                A deep copy of the current selection object.
        """
        return Selection(self.selected, self.rejected, self.implicit_reject)

    def __contains__(self, item):
        return item in self.selected or item in self.rejected

    def __len__(self):
        return len(self.selected)

    def total_len(self) -> int:
        """
            Get the total number of alternatives (selected and rejected).

            Returns
            -------
                int
                    Total count of selected and rejected alternatives.
            """
        return len(self.selected) + len(self.rejected)

    def __str__(self):
        if self.implicit_reject:
            return f"{{{self.selected}}} // {{implicit}}"
        else:
            return f"{{{self.selected}}} // {{{self.rejected}}}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Selection):
            return self.selected == other.selected and self.rejected == other.rejected
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Selection):
            return self.selected < other.selected
        return NotImplemented

