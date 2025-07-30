from __future__ import annotations

from trivoting.election.alternative import Alternative
from trivoting.election.trichotomous_ballot import TrichotomousBallot
from trivoting.election.trichotomous_profile import TrichotomousProfile

from pabutools.election import AbstractApprovalProfile, AbstractApprovalBallot, Instance, Project
from pabutools.election import parse_pabulib as pabutools_parse_pabulib

def pb_approval_ballot_to_trichotomous_ballot(
        app_ballot: AbstractApprovalBallot,
        alt_map: dict[Project, Alternative]
) -> TrichotomousBallot:
    """
    Converts an approval ballot from a PaBuLib profile into a trichotomous ballot.

    Parameters
    ----------
    app_ballot : AbstractApprovalBallot
        A ballot where projects are approved in a PaBuLib approval profile.
    alt_map : dict[Project, Alternative]
        A mapping from PaBuLib projects to Trivoting alternatives.

    Returns
    -------
    TrichotomousBallot
        A trichotomous ballot with approved alternatives (no disapprovals).
    """
    return TrichotomousBallot(approved=[alt_map[p] for p in app_ballot])

def pb_approval_profile_to_trichotomous_profile(
        instance: Instance,
        app_profile: AbstractApprovalProfile
) -> TrichotomousProfile:
    """
    Converts a PaBuLib approval profile into a trichotomous profile.

    Parameters
    ----------
    instance : Instance
        The project instance from PaBuLib.
    app_profile : AbstractApprovalProfile
        The approval profile from PaBuLib.

    Returns
    -------
    TrichotomousProfile
        A trichotomous profile with approved alternatives from the approval profile.
    """
    alt_map = {p: Alternative(p.name) for p in instance}
    profile = TrichotomousProfile()
    for ballot in app_profile:
        for _ in range(app_profile.multiplicity(ballot)):
            profile.append(pb_approval_ballot_to_trichotomous_ballot(ballot, alt_map))
    return profile

def parse_pabulib(file_path: str) -> TrichotomousProfile:
    """
    Parses a PaBuLib file and returns the corresponding trichotomous profile.

    Parameters
    ----------
    file_path : str
        Path to the PaBuLib file to be parsed.

    Returns
    -------
    TrichotomousProfile
        The profile corresponding to the file.
    """
    pb_instance, pb_profile = pabutools_parse_pabulib(file_path)
    if isinstance(pb_profile, AbstractApprovalProfile):
        profile = pb_approval_profile_to_trichotomous_profile(pb_instance, pb_profile)
        profile.max_size_selection = pb_instance.budget_limit
        return profile
    raise ValueError(f"PaBuLib profiles of type {type(pb_instance)} cannot be converted as a trichotomous profile.")
