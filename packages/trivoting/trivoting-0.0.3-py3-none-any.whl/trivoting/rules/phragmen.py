from __future__ import annotations

from copy import deepcopy

from trivoting.election.alternative import Alternative
from trivoting.election.trichotomous_ballot import AbstractTrichotomousBallot
from trivoting.election.trichotomous_profile import AbstractTrichotomousProfile
from trivoting.fractions import Numeric, frac
from trivoting.election.selection import Selection
from trivoting.tiebreaking import TieBreakingRule, lexico_tie_breaking


class PhragmenVoter:
    """
    Represents a voter during a run of the sequential Phragmén rule.

    Parameters
    ----------
    ballot : AbstractTrichotomousBallot
        The ballot of the voter.
    load : Numeric
        The initial load assigned to the voter.
    multiplicity : int
        The number of identical ballots represented by this voter.

    Attributes
    ----------
    ballot : AbstractTrichotomousBallot
        The ballot of the voter.
    load : Numeric
        The current load of the voter.
    multiplicity : int
        The multiplicity of the ballot.
    """

    def __init__(
        self, ballot: AbstractTrichotomousBallot, load: Numeric, multiplicity: int
    ):
        self.ballot = ballot
        self.load = load
        self.multiplicity = multiplicity

    def total_load(self):
        return self.multiplicity * self.load


def sequential_phragmen(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    initial_loads: list[Numeric] | None = None,
    initial_selection: Selection | None = None,
    tie_breaking: TieBreakingRule | None = None,
    resoluteness: bool = True,
) -> Selection | list[Selection]:
    """
    Compute the selections of the sequential Phragmén's rule.

    The definition of the sequential Phragmén's rule for the trichotomous context is taken from Section 3.2 of
    ``Proportionality in Thumbs Up and Down Voting`` (Kraiczy, Papasotiropoulos, Pierczyński and Skowron, 2025).

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        Maximum number of alternatives to select.
    initial_loads : list of Numeric, optional
        Initial loads for each ballot in the profile. Defaults to zero for all ballots.
    initial_selection : Selection, optional
        An initial selection that fixes some alternatives as selected or rejected.
        If `implicit_reject` is True, no alternatives are fixed to be rejected.
    tie_breaking : TieBreakingRule, optional
        Tie-breaking rule used when multiple alternatives tie.
        Defaults to lexicographic tie-breaking.
    resoluteness : bool, optional
        If True, returns a single selection (resolute).
        If False, returns all tied optimal selections (irresolute).
        Defaults to True.

    Returns
    -------
    Selection | list[Selection]
        The selection if resolute (:code:`resoluteness == True`), or a list of selections
        if irresolute (:code:`resoluteness == False`).
    """

    def _sequential_phragmen_rec(alternatives: set[Alternative], voters: list[PhragmenVoter], selection: Selection):
        if len(alternatives) == 0 or len(selection) == max_size_selection:
            if not resoluteness:
                selection.sort()
                if selection not in all_selections:
                    all_selections.append(selection)
            else:
                all_selections.append(selection)
        else:
            min_new_maxload = None
            arg_min_new_maxload = None
            for alt in alternatives:
                for considered_voters, veto in ((supporters[alt], False), (opposants[alt], True)):
                    num_considered_voters = len(considered_voters)
                    if num_considered_voters > 0:
                        new_maxload = frac(
                            sum(voters[i].total_load() for i in considered_voters) + 1, num_considered_voters,
                        )
                        if min_new_maxload is None or new_maxload < min_new_maxload:
                            min_new_maxload = new_maxload
                            arg_min_new_maxload = [(alt, veto)]
                        elif min_new_maxload == new_maxload:
                            arg_min_new_maxload.append((alt, veto))

            tied_alternatives = tie_breaking.order(profile, arg_min_new_maxload, key=lambda x: x[0])
            if resoluteness:
                selected_alternative, vetoed = tied_alternatives[0]
                for voter in voters:
                    if not vetoed and selected_alternative in voter.ballot.approved:
                        voter.load = min_new_maxload
                    elif vetoed and selected_alternative in voter.ballot.disapproved:
                        voter.load = min_new_maxload
                if not vetoed:
                    selection.add_selected(selected_alternative)
                alternatives.remove(selected_alternative)
                _sequential_phragmen_rec(alternatives, voters, selection)
            else:
                for selected_alternative, vetoed in tied_alternatives:
                    new_voters = deepcopy(voters)
                    for voter in new_voters:
                        if not vetoed and selected_alternative in voter.ballot.approved:
                            voter.load = min_new_maxload
                        elif vetoed and selected_alternative in voter.ballot.disapproved:
                            voter.load = min_new_maxload
                    new_selection = deepcopy(selection)
                    if not vetoed:
                        new_selection.add_selected(selected_alternative)
                    new_alternatives = deepcopy(alternatives)
                    new_alternatives.remove(selected_alternative)
                    _sequential_phragmen_rec(new_alternatives, new_voters, new_selection)

    try:
        max_size_selection = int(max_size_selection)
    except ValueError:
        raise ValueError('max_size_selection must be an integer.')

    if tie_breaking is None:
        tie_breaking = lexico_tie_breaking

    if initial_selection is not None:
        max_size_selection -= len(initial_selection)
    else:
        initial_selection = Selection(implicit_reject=True)

    if initial_loads is None:
        initial_voters = [PhragmenVoter(b, 0, profile.multiplicity(b)) for b in profile]
    else:
        initial_voters = [
            PhragmenVoter(b, initial_loads[i], profile.multiplicity(b))
            for i, b in enumerate(profile)
        ]

    supporters = {}
    opposants = {}
    initial_alternatives = set()
    for alt in profile.alternatives:
        if alt not in initial_selection.rejected:
            supps = [i for i, v in enumerate(initial_voters) if alt in v.ballot.approved]
            opps = [i for i, v in enumerate(initial_voters) if alt in v.ballot.disapproved]
            if supps or opps:
                supporters[alt] = supps
                opposants[alt] = opps
                initial_alternatives.add(alt)

    all_selections = []

    _sequential_phragmen_rec(initial_alternatives, initial_voters, initial_selection)

    if resoluteness:
        return all_selections[0]
    return all_selections
