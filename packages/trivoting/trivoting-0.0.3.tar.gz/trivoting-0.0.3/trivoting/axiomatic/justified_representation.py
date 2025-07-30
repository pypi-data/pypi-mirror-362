from collections.abc import Iterable, Iterator, Callable

from trivoting.election.alternative import Alternative
from trivoting.election.trichotomous_profile import AbstractTrichotomousProfile
from trivoting.fractions import frac
from trivoting.election.selection import Selection
from trivoting.utils import generate_subsets


def is_cohesive_for_l(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    l: int,
    group: AbstractTrichotomousProfile
) -> bool:
    """
    Tests whether the given set of voters is cohesive for level `l` as defined in Definition 1 of
    ``Proportionality in Thumbs Up and Down Voting`` (Kraiczy, Papasotiropoulos, Pierczyński and Skowron, 2025).

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        The maximum number of alternatives that can be selected.
    l : int
        The required representation level.
    group : AbstractTrichotomousProfile
        The subset of voters being tested for cohesion.

    Returns
    -------
    bool
        True if the group is l-cohesive, False otherwise.
    """
    if l > max_size_selection:
        return False
    if l == 0:
        return True
    if group.num_ballots() == 0:
        return False

    commonly_approved_alts = group.commonly_approved_alternatives()
    # Does not matter if we can find subsets with more than l
    commonly_approved_alts_subsets = list(generate_subsets(commonly_approved_alts, min_size=l, max_size=l))

    # Shortcut if there are no commonly approved alternatives of the suitable size
    if len(commonly_approved_alts_subsets) == 0:
        return l == 0

    group_size = group.num_ballots()
    relative_group_size = frac(group_size, profile.num_ballots())
    for selection in profile.all_feasible_selections(max_size_selection):
        if relative_group_size <= frac(l, selection.total_len() + l):
            return False
        exists_set_x = False
        for extra_alts in commonly_approved_alts_subsets:
            if any(a in selection.rejected for a in extra_alts):
                continue
            if len(set(extra_alts).union(selection.selected)) <= max_size_selection:
                exists_set_x = True
        if not exists_set_x:
            return False
    return True

def all_cohesive_groups(
        profile: AbstractTrichotomousProfile,
        max_size_selection: int,
        min_l: int = 1,
        max_l: int = None,
        test_cohesive_func: Callable = None
) -> Iterator[tuple[AbstractTrichotomousProfile, int]]:
    """
    Yields all voter groups that are cohesive for some level `l`. Yields both the group and the level `l`.

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        The maximum number of alternatives that can be selected.
    min_l : int, optional
        The minimum level of cohesion to test for. Defaults to 1.
    max_l : int, optional
        The maximum level of cohesion to test for. Defaults to the number of alternatives.
    test_cohesive_func : Callable, optional
        The function used to test cohesion. Defaults to `is_cohesive_for_l`.

    Yields
    ------
    tuple of (AbstractTrichotomousProfile, int)
        A cohesive group and the smallest level l for which it is cohesive.
    """
    if test_cohesive_func is None:
        test_cohesive_func = is_cohesive_for_l
    if max_l is None:
        max_l = len(profile.alternatives)
    for group in profile.all_sub_profiles():
        for l in range(min_l, max_l + 1):
            if test_cohesive_func(profile, max_size_selection, l, group):
                yield group, l
            else:
                break

def is_base_ejr_brute_force(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    selection: Selection
) -> bool:
    """
    Determines whether a selection satisfies Base Extended Justified Representation (Base EJR) as defined in Definition 1 of
    ``Proportionality in Thumbs Up and Down Voting`` (Kraiczy, Papasotiropoulos, Pierczyński and Skowron, 2025). Looks
    for every cohesive group and verifies that they are all satisfied.

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        The maximum number of alternatives that can be selected.
    selection : Selection
        The selection of alternatives to test.

    Returns
    -------
    bool
        True if Base EJR is satisfied, False otherwise.
    """
    for group, l in all_cohesive_groups(profile, max_size_selection):
        group_satisfied = False
        for ballot in group:
            satisfaction = sum(1 for a in ballot.approved if selection.is_selected(a))
            satisfaction += sum(1 for a in ballot.disapproved if selection.is_rejected(a))
            if satisfaction >= l:
                group_satisfied = True
                break
        if not group_satisfied:
            return False
    return True

def is_base_ejr(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    selection: Selection
) -> bool:
    """
    Determines whether a selection satisfies Base Extended Justified Representation (Base EJR) as defined in Definition 1 of
    ``Proportionality in Thumbs Up and Down Voting`` (Kraiczy, Papasotiropoulos, Pierczyński and Skowron, 2025).
    Makes used of the close formula provided in Lemma 1 of the same paper.

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        The maximum number of alternatives that can be selected.
    selection : Selection
        The selection of alternatives to test.

    Returns
    -------
    bool
        True if Base EJR is satisfied, False otherwise.
    """
    n = profile.num_ballots()
    m = len(profile.alternatives)
    def group_claim(sub_profile):
        group_size = sub_profile.num_ballots()
        relative_size = frac(n, n - group_size)
        inverse_relative_size = frac(n - group_size, n)
        num_commonly_approved_alts = len(sub_profile.commonly_approved_alternatives())
        num_commonly_disapproved_alts = len(sub_profile.commonly_disapproved_alternatives())

        if relative_size * max_size_selection <= num_commonly_disapproved_alts:
            return num_commonly_disapproved_alts - max_size_selection
        if (inverse_relative_size * max_size_selection <= num_commonly_disapproved_alts <= relative_size * max_size_selection) and \
            (frac(2*n - group_size, n) * num_commonly_approved_alts + inverse_relative_size * num_commonly_disapproved_alts >= max_size_selection):
            return frac(group_size, 2*n - group_size) * (num_commonly_disapproved_alts + max_size_selection)
        if (num_commonly_disapproved_alts + num_commonly_approved_alts >= max_size_selection) and \
                (num_commonly_disapproved_alts <= inverse_relative_size * max_size_selection) and \
                    (num_commonly_approved_alts <= m - inverse_relative_size * max_size_selection):
            return frac(group_size, n) * max_size_selection
        if (num_commonly_disapproved_alts + num_commonly_approved_alts >= max_size_selection) and \
                (num_commonly_disapproved_alts <= inverse_relative_size * max_size_selection) and \
                    (num_commonly_approved_alts >= m - inverse_relative_size * max_size_selection) and \
                        (num_commonly_approved_alts + max_size_selection - m <= frac(group_size, n) * (num_commonly_approved_alts + num_commonly_disapproved_alts)):
            return num_commonly_approved_alts + max_size_selection - m
        return frac(group_size, n) * (num_commonly_approved_alts + num_commonly_disapproved_alts)

    for group in profile.all_sub_profiles():
        exists_i = False
        for ballot in group:
            satisfaction = sum(1 for a in ballot.approved if selection.is_selected(a))
            satisfaction += sum(1 for a in ballot.disapproved if selection.is_rejected(a))
            if satisfaction >= group_claim(group):
                exists_i = True
        if not exists_i:
            return False
    return True


def is_base_pjr(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    selection: Selection
) -> bool:
    """
    Determines whether a selection satisfies Base Proportional Justified Representation (Base PJR) as defined in
    Definition 2 of ``Proportionality in Thumbs Up and Down Voting`` (Kraiczy, Papasotiropoulos, Pierczyński and
    Skowron, 2025).

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        The maximum number of alternatives that can be selected.
    selection : Selection
        The selection of alternatives to test.

    Returns
    -------
    bool
        True if Base PJR is satisfied, False otherwise.
    """

    for group, l in all_cohesive_groups(profile, max_size_selection):
        coincident_alternatives = set()
        for ballot in group:
            coincident_alternatives.update(a for a in ballot.approved if selection.is_selected(a))
            coincident_alternatives.update(a for a in ballot.disapproved if selection.is_rejected(a))
        if len(coincident_alternatives) < l:
            return False
    return True

def is_positively_cohesive_for_l(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    l: int,
    group: AbstractTrichotomousProfile
) -> bool:
    """
    Tests whether a group of voters is positively cohesive for level `l`.

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        The maximum number of alternatives that can be selected.
    l : int
        The required representation level.
    group : AbstractTrichotomousProfile
        The subset of voters being tested.

    Returns
    -------
    bool
        True if the group is positively cohesive, False otherwise.
    """
    if l > max_size_selection:
        return False
    if l == 0:
        return True
    if group.num_ballots() == 0:
        return False

    commonly_approved_alts = group.commonly_approved_alternatives()
    # Does not matter if we can find subsets with more than l
    commonly_approved_alts_subsets = list(generate_subsets(commonly_approved_alts, min_size=l, max_size=l))

    # Shortcut if there are no commonly approved alternatives of the suitable size
    if len(commonly_approved_alts_subsets) == 0:
        return l == 0

    for alt_subset in commonly_approved_alts_subsets:
        suitable_subset = True
        for alt in alt_subset:
            num_disapprovers = profile.disapproval_score(alt)
            if group.num_ballots() - num_disapprovers < l * frac(profile.num_ballots(), max_size_selection):
                suitable_subset = False
                break
        if suitable_subset:
            return True
    return False

def is_positive_ejr(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    selection: Selection
) -> bool:
    """
    Determines whether a selection satisfies Extended Justified Positive Representation (EJPR).

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        The maximum number of alternatives that can be selected.
    selection : Selection
        The selection of alternatives to test.

    Returns
    -------
    bool
        True if EJPR is satisfied, False otherwise.
    """
    for group, l in all_cohesive_groups(profile, max_size_selection, test_cohesive_func=is_positively_cohesive_for_l):
        group_satisfied = False
        for ballot in group:
            if sum(1 for a in ballot.approved if selection.is_selected(a)) >= l:
                group_satisfied = True
                break
        if not group_satisfied:
            return False
    return True

def is_negatively_cohesive_for_l_t(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    l: int,
    alt_set: Iterable[Alternative],
    group: AbstractTrichotomousProfile
) -> bool:
    """
    Tests whether a group of voters is l-T negatively cohesive for a given set of alternatives.

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        The maximum number of alternatives that can be selected.
    l : int
        The level of allowed violation.
    alt_set : Iterable[Alternative]
        The set of alternatives in question.
    group : AbstractTrichotomousProfile
        The subset of voters being tested.

    Returns
    -------
    bool
        True if the group is l-T negatively cohesive, False otherwise.
    """
    if not group.commonly_disapproved_alternatives().issubset(alt_set):
        return False

    num_disapprovers = 0
    for ballot in profile:
        if len(set(ballot.disapproved).intersection(alt_set)) > 0:
            num_disapprovers += profile.multiplicity(ballot)

    return group.num_ballots() >= num_disapprovers - l * frac(profile.num_ballots(), max_size_selection)

def is_group_veto(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    selection: Selection
) -> bool:
    """
    Determines whether a selection satisfies the group veto property.

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        The maximum number of alternatives that can be selected.
    selection : Selection
        The selection of alternatives to test.

    Returns
    -------
    bool
        True if the group veto condition is satisfied, False otherwise.
    """
    for group in profile.all_sub_profiles():
        commonly_disapproved_alts = group.commonly_disapproved_alternatives()
        for alt_set in generate_subsets(commonly_disapproved_alts, min_size=1):
            for l in range(1, len(profile.alternatives) + 1):
                if is_negatively_cohesive_for_l_t(profile, max_size_selection, l, alt_set, group):
                    if sum(1 for a in alt_set if selection.is_selected(a)) > l:
                        return False
    return True
