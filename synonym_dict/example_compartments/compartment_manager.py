"""
It is unfortunate that "context managers" are a thing in python and other languages- but here they mean something
different.

So I'm going to bow to the reserved keyword and call these things compartments instead of contexts.


"""

from ..synonym_dict import SynonymDict
from .compartment import Compartment

NullCompartment = Compartment.null()

# these are not-really-subcompartments whose names should be modified if they have parents
NONSPECIFIC_LOWER = {'unspecified', 'non-specific', 'nonspecific', 'unknown', 'undefined', 'none'}


class NonSpecificCompartment(Exception):
    pass


class InconsistentLineage(Exception):
    pass


class CompartmentManager(SynonymDict):

    _entry_group = 'Compartments'
    _syn_type = Compartment
    _ignore_case = True

    _null_entry = NullCompartment

    def _add_from_dict(self, j):
        """
        JSON dict has mandatory 'name', optional 'parent', and 'synonyms'
        We POP from it because it only gets processed once
        :param j:
        :return:
        """
        name = j.pop('name')
        syns = j.pop('synonyms', [])
        parent = j.pop('parent', None)
        self.new_entry(name, *syns, parent=parent, **j)

    def load_dict(self, j):
        comps = j[self._entry_group]
        subs = []
        while len(comps) > 0:
            for obj in comps:
                if 'parent' in obj:
                    try:
                        self._d[obj['parent']]
                    except KeyError:
                        subs.append(obj)
                        continue
                self._add_from_dict(obj)
            comps = subs
            subs = []

    def _list_entries(self):
        return [c for c in self.objects]

    @property
    def top_level_compartments(self):
        for v in self.entries:
            if v.parent is None:
                yield v

    @property
    def objects(self):
        for tc in self.top_level_compartments:
            for c in tc.self_and_subcompartments:
                yield c

    def new_entry(self, *args, parent=None, **kwargs):
        """
        If a new object is added with unmodified non-specific synonyms like "unspecified", modify them to include their
        parents' name
        :param args:
        :param parent:
        :param kwargs:
        :return:
        """
        if parent is not None:
            if not isinstance(parent, self._syn_type):
                parent = self._d[parent]
        nonspec = tuple([k for k in args if k.lower() in NONSPECIFIC_LOWER])
        args = tuple([k for k in args if k.lower() not in NONSPECIFIC_LOWER])
        if len(args) == 0:
            if parent is None:
                raise NonSpecificCompartment(nonspec)
            # no specific content
            out = pn = parent

        else:
            out = super(CompartmentManager, self).new_entry(*args, parent=parent, **kwargs)
            if parent is None:
                pn = out
            else:
                pn = parent
        for k in nonspec:
            self.add_synonym(out.name, self._fuller_name(k, pn))  # this is crucial--
        return out

    def _merge(self, existing_entry, ent):
        """
        Need to check lineage. We adopt the rule: merge is acceptable if both entries have the same top-level
        compartment or if ent has no parent.  existing entry will obviously be dominant
        :param existing_entry:
        :param ent:
        :return:
        """
        print('merging %s into %s' % (ent, existing_entry))
        if ent.parent is not None:
            if not ent.top() is existing_entry.top():
                raise InconsistentLineage('"%s": existing top %s | incoming top %s' % (ent,
                                                                                       existing_entry.top(),
                                                                                       ent.top()))

        super(CompartmentManager, self)._merge(existing_entry, ent)
        ent.parent = None
        for sub in list(ent.subcompartments):
            sub.parent = existing_entry

    @staticmethod
    def _fuller_name(name, parent):
        """
        more-precise name, given the parent
        used when renaming a compartment due to a collision
        :param name:
        :param parent:
        :return:
        """
        if parent is None:
            raise NonSpecificCompartment(name)
        return ', '.join([parent.name, name])

    @staticmethod
    def _tuple_to_name(comps):
        return '; '.join(filter(None, comps))

    def _check_subcompartment_lineage(self, current, c):
        """
        Determines whether the incoming compartment name 'c' already exists in the database with an inconsistent
        lineage from the current parent 'current'.

        If the term is not found, creates a new subcompartment with current as parent.

        If the term is found and has a valid lineage, the found subcompartment is used.

        If the term is found to be an orphan, then current is assigned as its parent, unless the "orphan" is an
        elementary root context ('emissions' or 'resources'), in which case all terms in current + parents are removed
        from the dictionary and assigned to _disregarded

        Otherwise, raises InconsistentLineage
        :param current:
        :param c:
        :return:
        """
        if c in self._d:
            new = self.get(c)
            if current is None:
                return new
            if new.is_subcompartment(current):
                return new
            if new.parent is None:
                new.parent = current
                return new
            raise InconsistentLineage('"%s": existing parent "%s" | incoming parent "%s"' % (c,
                                                                                             new.parent,
                                                                                             current))
        else:
            new = self.new_entry(c, parent=current)
            return new

    def add_compartments(self, comps, conflict=None):
        """
        comps should be a list of Compartment objects or strings, in descending order
        :param comps:
        :param conflict: ['rename'] strategy to resolve inconsistent lineage problems.
          'rename' changes the name of the conflicting entry to include its native (nonconflicting) parent
          'attach' sticks the whole encountered (existing) hierarchy onto the incoming hierarchy at current- could
            result in major structural changes to the hierarchy
          'match' hunts among the subcompartments of parent for a regex find
          'skip' simply drops the conflicting entry
          None or else: raise InconsistentLineage

        :return: the last (most specific) Compartment created
        """
        if len(comps) == 0 or comps is None:
            return self._null_entry
        current = None
        auto_name = tuple(comps)
        try:
            return self[auto_name]
        except (KeyError, InconsistentLineage):  # either of these can show up if auto_name is not known
            pass
        for c in comps:
            try:
                new = self._check_subcompartment_lineage(current, c)
            except InconsistentLineage as e:
                if conflict == 'match':
                    try:
                        new = next(s for s in current.subcompartments if s.contains_string(c, ignore_case=True))
                    except StopIteration:
                        raise e
                elif conflict == 'attach':
                    new = self.get(c)
                    new.top().parent = current

                elif conflict == 'skip':
                    new = current
                elif conflict == 'rename':
                    new_c = ', '.join([current.name, c])
                    new = self._check_subcompartment_lineage(current, new_c)
                else:
                    raise e

            current = new
        self.add_synonym(current.name, auto_name)
        return current

    def _is_known_compartment(self, item):
        e = None
        for i in item:
            if str(i).lower() in NONSPECIFIC_LOWER:
                continue
            g = self.__getitem__(i)
            if e and not g.is_subcompartment(e):
                try:
                    g = self.__getitem__(self._fuller_name(i, e))
                except KeyError:
                    raise InconsistentLineage(item, i, g)
            e = g
        return e

    def __getitem__(self, item):
        try:
            return super(CompartmentManager, self).__getitem__(item)
        except KeyError:
            if isinstance(item, tuple):
                match = self._is_known_compartment(item)  # or else KeyError
                self.add_synonym(match, item)
                return match
            elif str(item).lower() in NONSPECIFIC_LOWER:
                if isinstance(item, self._syn_type):
                    return self.__getitem__(item.parent)
                raise NonSpecificCompartment(item)
            raise
