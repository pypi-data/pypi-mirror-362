from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from collections.abc import Iterable, MutableSequence, MutableMapping, Iterator, Collection
from itertools import product

from trivoting.election.alternative import Alternative
from trivoting.election.selection import Selection
from trivoting.election.trichotomous_ballot import TrichotomousBallot, AbstractTrichotomousBallot, \
    FrozenTrichotomousBallot
from trivoting.fractions import Numeric
from trivoting.utils import generate_subsets, generate_two_list_partitions


class AbstractTrichotomousProfile(ABC, Iterable[AbstractTrichotomousBallot]):
    """
    Abstract class representing a profile, i.e., a collection of ballots.
    This class is only meant to be inherited and provides a common interface for trichotomous profiles.

    Attributes
    ----------
    alternatives : set[Alternative]
        The set of all alternatives in the profile.
    max_size_selection : int or None
        The maximum number of alternatives that can be selected in a feasible selection (optional).
    """

    def __init__(self, alternatives: Iterable[Alternative] = None, max_size_selection : int = None):
        if alternatives is None:
            self.alternatives = set()
        else:
            self.alternatives = set(alternatives)
        self.max_size_selection = max_size_selection

    def get_alternative_by_name(self, alt_name: str) -> Alternative | None:
        """
        Retrieves an alternative by its name.

        Parameters
        ----------
        alt_name : str
            The name of the alternative.

        Returns
        -------
            Alternative | None
                The alternative with the given name. None if there is no such alternative.
        """
        for alt in self.alternatives:
            if alt.name == alt_name:
                return alt

    @property
    @abstractmethod
    def _ballot_container(self) -> Collection[AbstractTrichotomousBallot]:
        """
        Returns the inner object used to collect ballots.
        """

    @abstractmethod
    def multiplicity(self, ballot: AbstractTrichotomousBallot) -> int:
        """
        Returns the multiplicity of a ballot.

        Parameters
        ----------
            ballot : AbstractTrichotomousBallot
                The ballot whose multiplicity is inquired.

        Returns
        -------
            int
                The multiplicity of the ballots.
        """

    @abstractmethod
    def num_ballots(self) -> int:
        """
        Returns the number of ballots in the profile.

        Returns
        -------
            int
                The multiplicity of the ballots.
        """

    @abstractmethod
    def add_ballot(self, ballot: AbstractTrichotomousBallot):
        """
        Adds a ballot to the profile.

        Parameters
        ----------
            ballot : AbstractTrichotomousBallot
                The ballot to add.
        """

    def add_ballots(self, ballots: Iterable[AbstractTrichotomousBallot]):
        """
        Adds multiple ballots to the profile.

        Parameters
        ----------
            ballots : Iterable[AbstractTrichotomousBallot]
                The ballots to add.
        """
        for ballot in ballots:
            self.add_ballot(ballot)

    @abstractmethod
    def support(self, alternative: Alternative) -> Numeric:
        """
        Returns the support of an alternative, i.e., the net number of voters supporting it (the number of approvers
        minus the number of disapprovers).
        
        Parameters
        ----------
            alternative: Alternative
                The alternative to consider.

        Returns
        -------
            int
                The support of the alternative.
        """

    @abstractmethod
    def support_dict(self) -> defaultdict[Alternative, int]:
        """
        Returns the support of the alternatives of the instance as a dictionary.

        Returns
        -------
            collections.defaultdict[Alternative, int]
                The support of each alternative appearing in at least one ballot.
                Alternatives never appearing (approved or disapproved) in any ballot will be absent, but accessing them
                returns 0.
        """
        
    @abstractmethod
    def approval_score(self, alternative: Alternative) -> int:
        """
        Returns the approval score of an alternative, i.e., the number of voters approving of it.
        
        Parameters
        ----------
            alternative: Alternative
                The alternative to consider.

        Returns
        -------
            int
                The approval score of the alternative.
        """

    @abstractmethod
    def approval_score_dict(self) -> defaultdict[Alternative, int]:
        """
        Returns the approval scores of the alternatives of the profile as a dictionary.

        Returns
        -------
            collections.defaultdict[Alternative, int]
                The approval score of each alternative appearing in at least one ballot.
                Alternatives never approved in any ballot will be absent, but accessing them returns 0.
        """
        

    @abstractmethod
    def disapproval_score(self, alternative: Alternative) -> int:
        """
        Returns the disapproval score of an alternative, i.e., the number of voters disapproving of it.
        
        Parameters
        ----------
            alternative: Alternative
                The alternative to consider.

        Returns
        -------
            int
                The disapproval score of the alternative.
        """
       

    @abstractmethod
    def disapproval_score_dict(self) -> defaultdict[Alternative, int]:
        """
        Returns the disapproval scores of the alternatives of the profile as a dictionary.

        Returns
        -------
            collections.defaultdict[Alternative, int]
                The disapproval score of each alternative appearing in at least one ballot.
                Alternatives never disapproved in any ballot will be absent, but accessing them returns 0.
        """

    @abstractmethod
    def approval_disapproval_score(self, alternative: Alternative) -> tuple[int, int]:
        """
        Returns the approval and disapproval score of an alternative together at the same time.
        
        Parameters
        ----------
            alternative: Alternative
                The alternative to consider.

        Returns
        -------
            tuple[int, int]
                The approval and the disapproval score of the alternative.
        """
       

    @abstractmethod
    def approval_disapproval_score_dict(self) -> tuple[defaultdict[Alternative, int], defaultdict[Alternative, int]]:
        """
        Returns the dictionaries of the approval score and of the disapproval score.

        Returns
        -------
            tuple[collections.defaultdict[Alternative, int], collections.defaultdict[Alternative, int]]
                The approval score and the disapproval score dictionaries.
                Alternatives never appearing (approved or disapproved) in any ballot will be absent, but accessing them
                returns 0.
        """

    def all_feasible_selections(self, max_size_selection: int) -> Iterator[Selection]:
        """
        Returns an iterator that yields all feasible (partial) selections.

        Parameters
        ----------
            max_size_selection: int
                Maximum number of alternatives that can be selected in a selection.

        Returns
        -------
            Iterator[Selection]
                An iterator that yields all feasible (partial) selections.

        """
        for l1, l2 in generate_two_list_partitions(self.alternatives, first_list_max_size=max_size_selection):
            yield Selection(selected=l1, rejected=l2, implicit_reject=False)

    @abstractmethod
    def all_sub_profiles(self) -> Iterator[AbstractTrichotomousProfile]:
        """
        Returns an iterator over all subprofiles of the profile.
        A subprofile is any multiset of ballots that is a subset (in terms of multiplicity) of the original profile.

        Returns
        -------
        Iterator[AbstractTrichotomousProfile]
            An iterator over all subprofiles of the profile.
        """

    def commonly_approved_alternatives(self) -> set[Alternative]:
        """
        Returns the pairwise intersection of the approved alternatives of all ballots in the profile.

        Returns
        -------
            set[Alternative]
                The set of alternatives commonly approved by all ballots.
        """
        return set.intersection(*(set(ballot.approved) for ballot in self._ballot_container))

    def commonly_disapproved_alternatives(self) -> set[Alternative]:
        """
        Returns the pairwise intersection of the disapproved alternatives of all ballots in the profile.

        Returns
        -------
            set[Alternative]
                The set of alternatives commonly disapproved by all ballots.
        """
        if len(self._ballot_container) == 0:
            return set()
        return set.intersection(*(set(ballot.disapproved) for ballot in self._ballot_container))

class TrichotomousProfile(AbstractTrichotomousProfile, MutableSequence[TrichotomousBallot]):
    """
    Represents a trichotomous profile, i.e., a collection of trichotomous ballots, one per voter.

    Parameters
    ----------
    init : Iterable[TrichotomousBallot], optional
        An iterable of trichotomous ballots used to initialize the profile. Defaults to empty.
    alternatives : Iterable[Alternative], optional
        An iterable of alternatives representing all alternatives of the instance.
    max_size_selection : int, optional
        The maximum number of alternatives to be selected when computing the outcome of a rule on the profile.
        Used notably when reading files from preference libraries.

    Attributes
    ----------
    alternatives : set[Alternative]
        A set of alternatives representing all the alternatives of the instance.
    max_size_selection : int or None
        The maximum number of alternatives to be selected when computing the outcome of a rule on the profile.
    """


    def __init__(
        self,
        init: Iterable[TrichotomousBallot] = (),
        *,
        alternatives: Iterable[Alternative] = None,
        max_size_selection: int = None,
    ) -> None:
        self._ballots_list = list(init)
        if alternatives is None and isinstance(init, AbstractTrichotomousProfile):
            alternatives = init.alternatives
        if max_size_selection is None and isinstance(init, AbstractTrichotomousProfile):
            max_size_selection = init.max_size_selection
        AbstractTrichotomousProfile.__init__(self, alternatives, max_size_selection)

    @property
    def _ballot_container(self) -> Iterable[AbstractTrichotomousBallot]:
        return self._ballots_list

    def support(self, alternative: Alternative) -> int:
        score = 0
        for ballot in self:
            if alternative in ballot.approved:
                score += 1
            elif alternative in ballot.disapproved:
                score -= 1
        return score

    def support_dict(self) -> defaultdict[Alternative, int]:
        res = defaultdict(int)
        for ballot in self:
            for alt in ballot.approved:
                res[alt] += 1
            for alt in ballot.disapproved:
                res[alt] -= 1
        return res

    def approval_score(self, alternative: Alternative) -> int:
        score = 0
        for ballot in self:
            if alternative in ballot.approved:
                score += 1
        return score

    def approval_score_dict(self) -> defaultdict[Alternative, int]:
        res = defaultdict(int)
        for ballot in self:
            for alt in ballot.approved:
                res[alt] += 1
        return res

    def disapproval_score(self, alternative: Alternative) -> int:
        score = 0
        for ballot in self:
            if alternative in ballot.disapproved:
                score += 1
        return score

    def disapproval_score_dict(self) -> defaultdict[Alternative, int]:
        res = defaultdict(int)
        for ballot in self:
            for alt in ballot.disapproved:
                res[alt] += 1
        return res

    def approval_disapproval_score(self, alternative: Alternative) -> tuple[int, int]:
        app_score = 0
        disapp_score = 0
        for ballot in self:
            if alternative in ballot.approved:
                app_score += 1
            if alternative in ballot.disapproved:
                disapp_score += 1
        return app_score, disapp_score

    def approval_disapproval_score_dict(self) -> tuple[defaultdict[Alternative, int], defaultdict[Alternative, int]]:
        app_scores = defaultdict(int)
        disapp_scores = defaultdict(int)
        for ballot in self:
            for alt in ballot.approved:
                app_scores[alt] += 1
            for alt in ballot.disapproved:
                disapp_scores[alt] += 1
        return app_scores, disapp_scores

    def num_ballots(self) -> int:
        return len(self)

    def add_ballot(self, ballot: TrichotomousBallot):
        self.append(ballot)

    def multiplicity(self, ballot: TrichotomousBallot) -> int:
        """
        Returns the multiplicity of a ballot in the profile.

        Note: This implementation returns 1 for any ballot regardless of its presence in the profile,
        to save computation time.

        Parameters
        ----------
        ballot : TrichotomousBallot
            The ballot whose multiplicity is inquired.

        Returns
        -------
        int
            The multiplicity of the ballot, always 1.
        """
        return 1

    def as_multiprofile(self) -> TrichotomousMultiProfile:
        """
        Returns the multiprofile corresponding to this profile. Ballots are converted to immutable frozen ballots.

        Returns
        -------
        TrichotomousMultiProfile
            The multiprofile representation of this profile with frozen ballots.
        """

        return TrichotomousMultiProfile([ballot.freeze() for ballot in self], alternatives=self.alternatives, max_size_selection=self.max_size_selection)

    def all_sub_profiles(self) -> Iterator[TrichotomousProfile]:
        """
        Returns an iterator over all possible sub-profiles of the current profile.

        A sub-profile is any subset of the ballots from the current profile.

        Returns
        -------
        Iterator[TrichotomousProfile]
            An iterator that yields all possible sub-profiles.
        """

        for subset in generate_subsets(self._ballots_list):
            yield TrichotomousProfile(subset, alternatives=self.alternatives, max_size_selection=self.max_size_selection)

    def __getitem__(self, index):
        if isinstance(index, slice):
            new_obj = TrichotomousProfile(self)
            new_obj._ballots_list = self._ballots_list[index]
            return new_obj
        return self._ballots_list[index]

    def __setitem__(self, index, value):
        self._ballots_list[index] = value

    def __delitem__(self, index):
        del self._ballots_list[index]

    def __len__(self):
        return len(self._ballots_list)

    def __iter__(self):
        return iter(self._ballots_list)

    def __contains__(self, item):
        return item in self._ballots_list

    def __reversed__(self):
        return reversed(self._ballots_list)

    def append(self, value):
        self._ballots_list.append(value)

    def extend(self, iterable):
        self._ballots_list.extend(iterable)

    def insert(self, index, value):
        self._ballots_list.insert(index, value)

    def remove(self, value):
        self._ballots_list.remove(value)

    def pop(self, index=-1):
        return self._ballots_list.pop(index)

    def clear(self):
        self._ballots_list.clear()

    def index(self, value, start=0, end=None):
        if end is None:
            end = len(self._ballots_list)
        return self._ballots_list.index(value, start, end)

    def count(self, value):
        return self._ballots_list.count(value)

    def sort(self, *, key=None, reverse=False):
        self._ballots_list.sort(key=key, reverse=reverse)

    def reverse(self):
        self._ballots_list.reverse()

    def copy(self):
        return TrichotomousProfile(self)

    def __add__(self, other):
        new_profile = TrichotomousProfile(self)
        if isinstance(other, TrichotomousProfile):
            new_profile._ballots_list += other._ballots_list
        else:
            new_profile._ballots_list += other
        return new_profile

    def __iadd__(self, other):
        if isinstance(other, TrichotomousProfile):
            self._ballots_list += other._ballots_list
        else:
            self._ballots_list += other
        return self

    def __mul__(self, n):
        if not isinstance(n, int):
            return ValueError("Cannot multiply profiles with non-int.")
        new_profile = TrichotomousProfile(self)
        new_profile._ballots_list *= n
        return new_profile

    def __imul__(self, n):
        if not isinstance(n, int):
            return ValueError("Cannot multiply profiles with non-int.")
        self._ballots_list *= n
        return self

    def __repr__(self):
        return self._ballots_list.__repr__()

    def __str__(self):
        return self._ballots_list.__str__()


class TrichotomousMultiProfile(AbstractTrichotomousProfile, MutableMapping[FrozenTrichotomousBallot, int]):
    """
    Represents a trichotomous multi-profile, i.e., a collection of trichotomous ballots where identical ballots
    are stored together with their multiplicities.

    This class models a multi-set of ballots, where each unique frozen ballot is associated with an integer
    count indicating how many times it appears in the profile.

    Parameters
    ----------
    init : Iterable[FrozenTrichotomousBallot], optional
        An iterable of frozen trichotomous ballots used to initialize the multi-profile.
        Defaults to an empty iterable.
    alternatives : Iterable[Alternative], optional
        An iterable of all alternatives present in the profile. If not provided and `init` is
        an `AbstractTrichotomousProfile`, its alternatives are used.
    max_size_selection : int, optional
        The maximum number of alternatives to be selected when computing the outcome of a rule on the profile.
        Used notably when reading files from preference libraries. If not provided and `init` is an
        `AbstractTrichotomousProfile`, its `max_size_selection` is used.

    Attributes
    ----------
    _ballots_counter : collections.Counter
        Internal counter mapping each frozen trichotomous ballot to its multiplicity.

    alternatives : set[Alternative]
        The set of all alternatives in the profile.

    max_size_selection : int
        Maximum number of alternatives to select in an outcome (optional).
    """

    def __init__(
        self,
        init: Iterable[FrozenTrichotomousBallot] = (),
        *,
        alternatives: Iterable[Alternative] = None,
        max_size_selection: int = None,
    ) -> None:
        self._ballots_counter = Counter(init)
        if alternatives is None and isinstance(init, AbstractTrichotomousProfile):
            alternatives = init.alternatives
        if max_size_selection is None and isinstance(init, AbstractTrichotomousProfile):
            max_size_selection = init.max_size_selection
        AbstractTrichotomousProfile.__init__(self, alternatives, max_size_selection)

    @property
    def _ballot_container(self) -> Iterable[AbstractTrichotomousBallot]:
        return self._ballots_counter

    def support(self, alternative: Alternative) -> int:
        score = 0
        for ballot, count in self.items():
            if alternative in ballot.approved:
                score += count
            elif alternative in ballot.disapproved:
                score -= count
        return score

    def support_dict(self) -> defaultdict[Alternative, int]:
        res = dict()
        for ballot, count in self.items():
            for alt in ballot.approved:
                if alt in res:
                    res[alt] += count
                else:
                    res[alt] = count
            for alt in ballot.disapproved:
                if alt in res:
                    res[alt] -= count
                else:
                    res[alt] = -count
        return res

    def approval_score(self, alternative: Alternative) -> int:
        score = 0
        for ballot, count in self.items():
            if alternative in ballot.approved:
                score += count
        return score

    def approval_score_dict(self) -> defaultdict[Alternative, int]:
        res = defaultdict(int)
        for ballot, count in self.items():
            for alt in ballot.approved:
                res[alt] += count
        return res
    def disapproval_score(self, alternative: Alternative) -> int:
        score = 0
        for ballot, count in self.items():
            if alternative in ballot.disapproved:
                score += count
        return score

    def disapproval_score_dict(self) -> defaultdict[Alternative, int]:
        res = defaultdict(int)
        for ballot, count in self.items():
            for alt in ballot.disapproved:
                res[alt] += count
        return res

    def approval_disapproval_score(self, alternative: Alternative) -> tuple[int, int]:
        app_score = 0
        disapp_score = 0
        for ballot, count in self.items():
            if alternative in ballot.approved:
                app_score += count
            if alternative in ballot.disapproved:
                disapp_score += count
        return app_score, disapp_score

    def approval_disapproval_score_dict(self) -> tuple[defaultdict[Alternative, int], defaultdict[Alternative, int]]:
        app_scores = defaultdict(int)
        disapp_scores = defaultdict(int)
        for ballot, count in self.items():
            for alt in ballot.approved:
                app_scores[alt] += count
            for alt in ballot.disapproved:
                disapp_scores[alt] += count
        return app_scores, disapp_scores

    def total(self):
        """
        Computes the total number of ballots in the profile, counting multiplicities.

        Returns
        -------
        int
            Total number of ballots.
        """
        # Re-implemented as it is not available in Python <3.10
        return sum(self.values())

    def num_ballots(self) -> int:
        return self.total()

    def add_ballot(self, ballot: FrozenTrichotomousBallot):
        """
        Adds a ballot to the multi-profile, increasing its multiplicity by one.

        Parameters
        ----------
        ballot : FrozenTrichotomousBallot
            The frozen ballot to add.
        """
        if isinstance(ballot, TrichotomousBallot):
            raise ValueError("You are trying to add a non-frozen ballot to a multiprofile. This is not possible, "
                             "please freeze the ballot via ballot.freeze() before adding it.")
        self[ballot] += 1

    def multiplicity(self, ballot: FrozenTrichotomousBallot) -> int:
        """
        Returns the multiplicity of a given ballot in the profile.

        Parameters
        ----------
        ballot : FrozenTrichotomousBallot
            The ballot whose multiplicity is requested.

        Returns
        -------
        int
            The number of times the ballot appears in the profile.
        """
        return self[ballot]

    def all_sub_profiles(self) -> Iterator[TrichotomousMultiProfile]:
        """
        Generates all possible sub-profiles of the current multi-profile.

        A sub-profile is any profile obtained by choosing any number (including zero) of occurrences
        of each ballot up to their multiplicity in the current profile.

        Yields
        ------
        TrichotomousMultiProfile
            Each possible sub-profile.
        """
        items = list(self._ballots_counter.items())
        for counts in product(*(range(count + 1) for _, count in items)):
            sub_profile = TrichotomousMultiProfile({key: count for (key, _), count in zip(items, counts) if count > 0},
                                              alternatives=self.alternatives,
                                              max_size_selection=self.max_size_selection,)
            yield sub_profile

    def __getitem__(self, key):
        return self._ballots_counter[key]

    def __setitem__(self, key, value):
        if value <= 0:
            del self._ballots_counter[key]
        else:
            self._ballots_counter[key] = value

    def __delitem__(self, key):
        del self._ballots_counter[key]

    def __iter__(self):
        return iter(self._ballots_counter)

    def __len__(self):
        return len(self._ballots_counter)

    def __contains__(self, key):
        return key in self._ballots_counter

    def __repr__(self):
        return repr(self._ballots_counter)

    def __str__(self):
        return self._ballots_counter.__str__()

    def __add__(self, other):
        new_profile = TrichotomousMultiProfile(self)
        if isinstance(other, TrichotomousMultiProfile):
            new_profile._ballots_counter = self._ballots_counter + other._ballots_counter
        else:
            new_profile._ballots_counter = self._ballots_counter + other
        return new_profile

    def __iadd__(self, other):
        if isinstance(other, TrichotomousMultiProfile):
            self._ballots_counter += other._ballots_counter
        else:
            self._ballots_counter += other
        return self

    def __sub__(self, other):
        new_profile = TrichotomousMultiProfile(self)
        if isinstance(other, TrichotomousMultiProfile):
            new_profile._ballots_counter = self._ballots_counter - other._ballots_counter
        else:
            new_profile._ballots_counter = self._ballots_counter - other
        return new_profile

    def __isub__(self, other):
        if isinstance(other, TrichotomousMultiProfile):
            self._ballots_counter -= other._ballots_counter
        else:
            self._ballots_counter -= other
        return self

    def __or__(self, other):
        new_profile = TrichotomousMultiProfile(self)
        if isinstance(other, TrichotomousMultiProfile):
            new_profile._ballots_counter = self._ballots_counter | other._ballots_counter
        else:
            new_profile._ballots_counter = self._ballots_counter | other
        return new_profile

    def __ior__(self, other):
        if isinstance(other, TrichotomousMultiProfile):
            self._ballots_counter |= other._ballots_counter
        else:
            self._ballots_counter |= other
        return self

    def __and__(self, other):
        new_profile = TrichotomousMultiProfile(self)
        if isinstance(other, TrichotomousMultiProfile):
            new_profile._ballots_counter = self._ballots_counter & other._ballots_counter
        else:
            new_profile._ballots_counter = self._ballots_counter & other
        return new_profile

    def __iand__(self, other):
        if isinstance(other, TrichotomousMultiProfile):
            self._ballots_counter &= other._ballots_counter
        else:
            self._ballots_counter &= other
        return self

    def elements(self):
        return self._ballots_counter.elements()

    def most_common(self, n=None):
        return self._ballots_counter.most_common(n)

    def subtract(self, other):
        self._ballots_counter.subtract(other)

    def update(self, iterable=None, **kwargs):
        self._ballots_counter.update(iterable, **kwargs)

    def clear(self):
        self._ballots_counter.clear()

    def copy(self):
        return TrichotomousMultiProfile(self)
