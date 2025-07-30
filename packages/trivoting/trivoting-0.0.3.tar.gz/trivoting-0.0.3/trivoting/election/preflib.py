from __future__ import annotations

from preflibtools.instances import CategoricalInstance, get_parsed_instance

from trivoting.election.alternative import Alternative
from trivoting.election.trichotomous_ballot import TrichotomousBallot
from trivoting.election.trichotomous_profile import TrichotomousProfile


def cat_preferences_to_trichotomous_ballot(
    pref: tuple[tuple[int]],
    alt_map: dict[int, Alternative]
) -> TrichotomousBallot:
    """
    Converts a categorical preference from PrefLib into a trichotomous ballot.

    The first category in the preference is treated as the set of approved alternatives.
    If a second category is present, it is treated as neutral and ignored in the ballot.
    If a third category is present, it is treated as the set of disapproved alternatives.

    Parameters
    ----------
    pref : tuple[tuple[int]]
        The categorical preferences, typically a tuple of up to 3 ranked groups of alternative IDs.
    alt_map : dict[int, Alternative]
        A mapping from PrefLib integer IDs to Alternative objects.

    Returns
    -------
    TrichotomousBallot
        The corresponding trichotomous ballot.

    Raises
    ------
    ValueError
        If the number of categories is not between 1 and 3.
    """
    if len(pref) == 0 or len(pref) > 3:
        raise ValueError("Only categorical preferences between 1 and 3 categories can be converted to"
                         f"a trichotomous ballot. Pref {pref} has {len(pref)} categories.")
    ballot = TrichotomousBallot(approved=[alt_map[j] for j in pref[0]])
    if len(pref) < 2:
        return ballot
    ballot.disapproved = [alt_map[j] for j in pref[-1]]
    return ballot


def cat_instance_to_trichotomous_profile(
    cat_instance: CategoricalInstance
) -> TrichotomousProfile:
    """
    Converts a PrefLib CategoricalInstance into a trichotomous profile. The PrefLib instance should have 1, 2 or 3
    categories. If there is a single categories, it is assumed to represent the approved alternatives. If there are
    2 categories, it is assumed that they represent the approved and neutral alternatives. In case of 3 categories,
    the categories are assumed to represent approved, neutral and disapproved alternatives, in that order.

    Each ballot in the categorical instance is converted using
    `cat_preferences_to_trichotomous_ballot`.

    Parameters
    ----------
    cat_instance : CategoricalInstance
        A parsed categorical instance from PrefLib.

    Returns
    -------
    TrichotomousProfile
        A profile composed of trichotomous ballots.
    """
    if cat_instance.num_categories == 0 or cat_instance.num_categories > 3:
        raise ValueError("Only categorical preferences between 1 and 3 categories can be converted to"
                         f"a trichotomous profile. Categorical instance {cat_instance} has "
                         f"{cat_instance.num_categories} categories.")

    alt_map = {j: Alternative(j) for j in cat_instance.alternatives_name}
    profile = TrichotomousProfile(alternatives=alt_map.values())

    for p, m in cat_instance.multiplicity.items():
        for _ in range(m):
            profile.append(cat_preferences_to_trichotomous_ballot(p, alt_map))
    return profile

def parse_preflib(file_path: str) -> TrichotomousProfile:
    """
    Parses a PrefLib file and returns the corresponding trichotomous profile.

    The file is parsed using `preflibtools.get_parsed_instance`, and only
    categorical instances with 1–3 categories are supported.

    Parameters
    ----------
    file_path : str
        The file path to a PrefLib categorical instance.

    Returns
    -------
    TrichotomousProfile
        A trichotomous profile built from the given file.
    """

    instance = get_parsed_instance(file_path, autocorrect=True)
    if isinstance(instance, CategoricalInstance):
        return cat_instance_to_trichotomous_profile(instance)
    raise ValueError(f"PrefLib instances of type {type(instance)} cannot be converted to trichotomous profiles.")
