from __future__ import annotations

from collections.abc import Callable

import pabutools.election as pb_election
import pabutools.rules as pb_rules

from trivoting.election.alternative import Alternative
from trivoting.election.trichotomous_profile import AbstractTrichotomousProfile
from trivoting.fractions import frac
from trivoting.election.selection import Selection
from trivoting.tiebreaking import TieBreakingRule


def tax_pb_instance(
        profile: AbstractTrichotomousProfile,
        max_size_selection: int,
        initial_selection: Selection | None = None,
) -> tuple[pb_election.Instance, pb_election.ApprovalMultiProfile, dict[pb_election.Project, Alternative]]:
    """
    Construct a Participatory Budgeting (PB) instance and PB profile from a trichotomous profile.

    This function translates the trichotomous voting profile into a PB instance,
    setting project costs inversely proportional to net support.

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        The budget limit or maximum number of alternatives to be selected.
    initial_selection : Selection or None, optional
        An initial selection fixing some alternatives as selected or rejected.

    Returns
    -------
    pb_election.Instance
        The generated PB instance containing projects.
    pb_election.ApprovalMultiProfile
        The PB profile created from approval ballots derived from the trichotomous profile.
    dict
        A mapping from PB projects back to the original alternatives.
    """
    app_scores, disapp_scores = profile.approval_disapproval_score_dict()

    if initial_selection is None:
        initial_selection = Selection()

    alt_to_project = dict()
    project_to_alt = dict()
    running_alternatives = set()
    pb_instance = pb_election.Instance(budget_limit=max_size_selection)
    for alt, app_score in app_scores.items():
        support = app_score - disapp_scores[alt]
        if support > 0 and alt not in initial_selection:
            project = pb_election.Project(alt.name, cost=frac(app_score, support))
            pb_instance.add(project)
            running_alternatives.add(alt)
            alt_to_project[alt] = project
            project_to_alt[project] = alt

    pb_profile = pb_election.ApprovalMultiProfile(instance=pb_instance)
    for ballot in profile:
        pb_profile.append(
            pb_election.FrozenApprovalBallot(alt_to_project[alt] for alt in ballot.approved if alt in running_alternatives)
        )
    return pb_instance, pb_profile, project_to_alt

def tax_pb_rule_scheme(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    pb_rule: Callable,
    initial_selection: Selection | None = None,
    tie_breaking: TieBreakingRule | None = None,
    resoluteness: bool = True,
    pb_rule_kwargs: dict = None,
) -> Selection | list[Selection]:
    """
    Apply a participatory budgeting rule to a trichotomous profile by translating it into a suitable PB instance with
    opposition tax.

    This function converts the given profile into a PB instance and profile,
    applies the specified PB rule using pabutools, and converts the results back.

    The taxed PB rule scheme has been defined in Section 4.2 of
    ``Proportionality in Thumbs Up and Down Voting`` (Kraiczy, Papasotiropoulos, Pierczyński and Skowron, 2025).

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The trichotomous profile.
    max_size_selection : int
        The maximum number of alternatives allowed in the selection.
    pb_rule : callable
        The participatory budgeting rule function to apply.
    initial_selection : Selection or None, optional
        An initial selection fixing some alternatives as selected or rejected.
    tie_breaking : TieBreakingRule or None, optional
        Tie-breaking rule used for resolving ties.
        Defaults to lexicographic tie-breaking if None.
    resoluteness : bool, optional
        Whether to return a single resolute selection (True) or all tied selections (False).
        Defaults to True.
    pb_rule_kwargs : dict, optional
        Additional keyword arguments passed to the PB rule.

    Returns
    -------
    Selection or list of Selection
        The resulting selection(s) after applying the PB rule.
    """
    if pb_rule_kwargs is None:
        pb_rule_kwargs = dict()

    if initial_selection is None:
        initial_selection = Selection(implicit_reject=True)

    if profile.num_ballots() == 0:
        return initial_selection if resoluteness else [initial_selection]

    pb_instance, pb_profile, project_to_alt = tax_pb_instance(profile, max_size_selection, initial_selection)

    budget_allocation = pb_rule(
        pb_instance,
        pb_profile,
        tie_breaking=tie_breaking,
        resoluteness=resoluteness,
        **pb_rule_kwargs
    )

    if resoluteness:
        initial_selection.extend_selected(project_to_alt[p] for p in budget_allocation)
        if not initial_selection.implicit_reject:
            initial_selection.extend_rejected(project_to_alt[p] for p in pb_instance if p not in budget_allocation)
        return initial_selection
    else:
        all_selections = []
        for alloc in budget_allocation:
            selection = initial_selection.copy()
            selection.extend_selected(project_to_alt[p] for p in alloc)
            if not selection.implicit_reject:
                selection.extend_rejected(project_to_alt[p] for p in pb_instance if p not in alloc)
            all_selections.append(selection)
        return all_selections

def tax_method_of_equal_shares(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    initial_selection: Selection | None = None,
    tie_breaking: TieBreakingRule | None = None,
    resoluteness: bool = True,
) -> Selection | list[Selection]:
    """
    Apply the Tax method of equal shares to a trichotomous profile.

    This method uses participatory budgeting rules to compute proportional selections
    with the method of equal shares adapted for approval-disapproval profiles.

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The input profile.
    max_size_selection : int
        The maximum number of alternatives to select.
    initial_selection : Selection or None, optional
        Initial fixed selection state.
    tie_breaking : TieBreakingRule or None, optional
        Tie-breaking rule. Defaults to lexicographic.
    resoluteness : bool, optional
        Whether to return a single or multiple tied selections.

    Returns
    -------
    Selection | list[Selection]
        The selection if resolute (:code:`resoluteness == True`), or a list of selections
        if irresolute (:code:`resoluteness == False`).
    """
    return tax_pb_rule_scheme(
        profile,
        max_size_selection,
        pb_rules.method_of_equal_shares,
        initial_selection=initial_selection,
        tie_breaking=tie_breaking,
        resoluteness=resoluteness,
        pb_rule_kwargs={"sat_class": pb_election.Cardinality_Sat}
    )

def tax_sequential_phragmen(
    profile: AbstractTrichotomousProfile,
    max_size_selection: int,
    initial_selection: Selection | None = None,
    tie_breaking: TieBreakingRule | None = None,
    resoluteness: bool = True,
) -> Selection | list[Selection]:
    """
    Apply Tax sequential Phragmén method on a trichotomous profile.

    This rule transforms the profile into a participatory budgeting instance
    and applies sequential Phragmén via pabutools.

    Parameters
    ----------
    profile : AbstractTrichotomousProfile
        The input voting profile.
    max_size_selection : int
        The maximum size of the selection.
    initial_selection : Selection or None, optional
        Initial fixed selections.
    tie_breaking : TieBreakingRule or None, optional
        Tie-breaking rule, defaulting to lexicographic.
    resoluteness : bool, optional
        Whether to return one selection or all tied selections.

    Returns
    -------
    Selection | list[Selection]
        The selection if resolute (:code:`resoluteness == True`), or a list of selections
        if irresolute (:code:`resoluteness == False`).
    """

    return tax_pb_rule_scheme(
        profile,
        max_size_selection,
        pb_rules.sequential_phragmen,
        initial_selection=initial_selection,
        tie_breaking=tie_breaking,
        resoluteness=resoluteness,
        pb_rule_kwargs={"global_max_load": frac(max_size_selection, profile.num_ballots()) if profile.num_ballots() else None}
    )
