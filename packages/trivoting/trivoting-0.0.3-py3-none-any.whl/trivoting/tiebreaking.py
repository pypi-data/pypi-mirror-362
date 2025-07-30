from __future__ import annotations

from collections.abc import Callable, Iterable
from trivoting.election.trichotomous_profile import TrichotomousProfile, AbstractTrichotomousProfile
from trivoting.election.alternative import Alternative
from trivoting.fractions import Numeric


class TieBreakingException(Exception):
    """Raised when a tie occurs and no tie-breaking rule is provided."""


class TieBreakingRule:
    """
    Implements a tie-breaking rule.

    Parameters
    ----------
        func : Callable[[TrichotomousProfile, Alternative], Numeric]
            A function taking as input an instance, a profile and a project and returning the value on which the
            project will be sorted.

    Attributes
    ----------
        func : Callable[[TrichotomousProfile, Alternative], Numeric]
            A function taking as input an instance, a profile and a project and returning the value on which the
            project will be sorted.
    """

    def __init__(self, func: Callable[[AbstractTrichotomousProfile, Alternative], Numeric]):
        self.func = func

    def order(
        self,
        profile: AbstractTrichotomousProfile,
        alternatives: Iterable,
        key: Callable[..., Alternative] | None = None,
    ) -> list[Alternative]:
        """
        Break the ties among all the alternatives provided in input and returns them ordered.

        Parameters
        ----------
            profile : TrichotomousProfile
                The profile.
            alternatives : Iterable
                The set of alternatives between which ties are to be broken.
            key : Callable[..., Alternative], optional
                A key function to select the value associated with each alternative, passed as the
                `key` argument of the `sorted` function. Defaults to `lambda x: x`.

        Returns
        -------
            list[Alternative]
                The alternatives, ordered by the tie-breaking rule.
        """

        def default_key(p):
            return p

        if not alternatives:
            return []

        if key is None:
            key = default_key
        return sorted(
            alternatives,
            key=lambda alt: self.func(profile, key(alt)),
        )

    def untie(
        self,
        profile: AbstractTrichotomousProfile,
        alternatives: Iterable,
        key: Callable[..., Alternative] | None = None,
    ) -> Alternative:
        """
        Break the ties among all the alternatives provided in input and returns a single one of them. Orders the
        alternatives according to the tie-breaking rule and return the first element of the order.

        Parameters
        ----------
            profile : TrichotomousProfile
                The profile.
            alternatives : Iterable
                The set of alternatives between which ties are to be broken.
            key : Callable[..., Alternative], optional
                A key function to select the value associated with each alternative, passed as the
                `key` argument of the `sorted` function. Defaults to `lambda x: x`.

        Returns
        -------
            Alternative
                The first alternative according to the tie-breaking order.
        """

        def default_key(p):
            return p

        if key is None:
            key = default_key
        return self.order(profile, alternatives, key)[0]


lexico_tie_breaking = TieBreakingRule(lambda prof, alt: alt.name)
"""
Implements lexicographic tie breaking, i.e., tie-breaking based on the name of the alternatives.
"""

support_tie_breaking = TieBreakingRule(
    lambda prof, alt: -prof.support(alt)
)
"""
Implements tie breaking based on the support where the projects with the highest support in the profile is selected.
"""

app_score_tie_breaking = TieBreakingRule(
    lambda prof, alt: -prof.approval_score(alt)
)
"""
Implements tie breaking based on the approval score where the projects with the highest approval score in the profile
 is selected.
"""

def refuse_tie_breaking(profile, alternative):
    raise TieBreakingException("A tie occurred, but no tie-breaking rule was provided.")

refuse_tie_breaking = TieBreakingRule(refuse_tie_breaking)
"""
Special tie-breaking function that simply raises an error when a tie needs to be broken.
"""
