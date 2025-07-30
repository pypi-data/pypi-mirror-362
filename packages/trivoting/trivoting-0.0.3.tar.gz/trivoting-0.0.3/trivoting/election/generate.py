from collections.abc import Callable

from trivoting.election.alternative import Alternative
from trivoting.election.trichotomous_ballot import TrichotomousBallot
from trivoting.election.trichotomous_profile import TrichotomousProfile


def generate_random_ballot(
        alternatives: list[Alternative],
        approved_disapproved_sampler: Callable,
        approved_sampler: Callable,
        disapproved_sampler: Callable
) -> TrichotomousBallot:
    """
    Generates a random trichotomous ballot based on the given sampling functions. Sampling functions are expected to
    behave as the ones from the `prefsampling` package.
    
    First samples a set of potentially approved alternatives. The set of the potentially disapproved alternatives 
    is the complement of the former. For both of these sets, an extra sampling function is applied to determine the
    definitively approved and disapproved alternatives.

    Parameters
    ----------
    alternatives : list of Alternative
        List of alternatives available in the election.
    approved_disapproved_sampler : Callable
        Function that samples a split between potentially approved and disapproved alternatives.
        It should take `num_voters` and `num_candidates` as keyword arguments and return a list of index sets.
    approved_sampler : Callable
        Function that samples which of the potentially approved alternatives are definitively approved.
        Same interface as `approve_disapproved_sampler`.
    disapproved_sampler : Callable
        Function that samples which of the potentially disapproved alternatives are definitively disapproved.
        Same interface as `approve_disapproved_sampler`.

    Returns
    -------
    TrichotomousBallot
        A randomly generated trichotomous ballot.
    """
    ballot = TrichotomousBallot()
    approved_disapproved = approved_disapproved_sampler(num_voters=1, num_candidates=len(alternatives))[0]
    potentially_approved = []
    potentially_disapproved = []
    for i, a in enumerate(alternatives):
        if i in approved_disapproved:
            potentially_approved.append(a)
        else:
            potentially_disapproved.append(a)
    if len(potentially_approved) == 0:
        approved_indices = []
    else:
        approved_indices = approved_sampler(num_voters=1, num_candidates=len(potentially_approved))[0]
    ballot.approved = [alternatives[i] for i in approved_indices]
    if len(potentially_disapproved) == 0:
        disapproved_indices = []
    else:
        disapproved_indices = disapproved_sampler(num_voters=1, num_candidates=len(potentially_disapproved))[0]
        disapproved_indices = [i for i in disapproved_indices if i not in approved_indices]
    ballot.disapproved = [alternatives[i] for i in disapproved_indices]
    return ballot

def generate_random_profile(
        num_alternatives: int,
        num_voters: int,
        approved_disapproved_sampler: Callable,
        approved_sampler: Callable,
        disapproved_sampler: Callable
) -> TrichotomousProfile:
    """
    Generates a random trichotomous profile composed of several ballots. Uses the function `generate_random_ballot`
    to generate the ballots.

    Parameters
    ----------
    num_alternatives : int
        The number of alternatives in the profile.
    num_voters : int
        The number of voters (ballots) in the profile.
    approved_disapproved_sampler : Callable
        Function that samples a split between potentially approved and disapproved alternatives.
        It should take `num_voters` and `num_candidates` as keyword arguments and return a list of index sets.
    approved_sampler : Callable
        Function that samples which of the potentially approved alternatives are definitively approved.
        Same interface as `approve_disapproved_sampler`.
    disapproved_sampler : Callable
        Function that samples which of the potentially disapproved alternatives are definitively disapproved.
        Same interface as `approve_disapproved_sampler`.

    Returns
    -------
    TrichotomousProfile
        A profile containing randomly generated trichotomous ballots.
    """
    alternatives = [Alternative(i) for i in range(num_alternatives)]
    profile = TrichotomousProfile(alternatives=alternatives)
    for _ in range(num_voters):
        ballot = generate_random_ballot(
            alternatives,
            approved_disapproved_sampler,
            approved_sampler,
            disapproved_sampler
        )
        profile.add_ballot(ballot)
    return profile
