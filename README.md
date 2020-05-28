# synonym_dict

A class that allows retrieval of a given object by any of its synonyms.

[![Build Status](https://travis-ci.com/bkuczenski/synonym_dict.svg?branch=master)](https://travis-ci.com/bkuczenski/synonym_dict)[![Coverage Status](https://coveralls.io/repos/github/bkuczenski/synonym_dict/badge.svg?branch=master)](https://coveralls.io/github/bkuczenski/synonym_dict?branch=master)

# Overview

There are many situations in which an object may be known by several names.  `synonym_dict` provides a way to:

  1. Retrieve an object by its name or any synonyms
  2. Ensure that synonyms are distinct and non-overlapping
  3. Support case-insensitive tests

## Installation

```{bash}
$ pip install synonym_dict
```

The package has no dependencies.

### Testing

```{bash}
$ python -m unittest
```

Or, on `python2`:
```{bash}
$ python -m unittest discover
```

# Code Design

### SynonymSet

A `SynonymSet`  a set of synonyms called "terms" in a hashable collection.  Its "name" is canonically its first term, but can be set to any term in the collection. It can also have child objects, all of whose terms are taken to be synonyms.

```{python}
# from TestSynonymSet.test_name()
s = SynonymSet('hello', 'aloha', 'Ni hao')
assert str(s) == 'hello'
assert s.object == 'hello'
s.set_name('aloha')
assert s.object == 'aloha'
```

Each synonym set can represent a particular object, such that the terms are synonymous names for that object.  The object for the base `SynonymSet` is simply the name of the set, but subclasses can override this.

### SynonymDict

```{python}
# from TestSynonymDict.test_explicit_merge()
g = SynonymDict(ignore_case=False)  # default
g.new_entry('hello', 'hola', 'hi', 'aloha')
g.new_entry('Hello', 'HELLO', 'Hi', 'HI')
assert g['hi'] == 'hello'
assert g['HI'] == 'Hello'
g.merge('hi', 'HI')
assert g['HI'] == 'hello'
```

A `SynonymDict` is a typed collection of `SynonymSets` or subclasses, each of which is called an `entry`.  The `SynonymDict` is responsible for managing the set of terms and preventing collisions.  It can be case-sensitive or case-insensitive.

A key functionality of the dict is in combining entries.  When creating a new entry, the dict first checks to see if any terms are already assigned to an existing entry.  If they are, the merge strategy determines what to do among the choices of "merge", "prune", or "strict":

  - The default is to merge the terms into the existing entry.  This fails with `MergeError` if the incoming terms match two or more entries.
  - If "prune" is specified, the duplicate terms are removed from the new entry and it is created using only unknown terms.
  - If neither "merge" nor "prune" are specified, the new entry is created only if every term is unknown; otherwise a `TermExists` error is raised.

### LowerDict

```{python}
d = LowerDict()
d['smeeb'] = 42
assert d['   SMeeB '] == 42
d[' dRoOl '] = 17
assert d['drool'] == 17
assert list(d.keys()) == ['smeeb', 'dRoOl']
```

A simple `dict` subclass that implements case-insensitivity.  Also strips leading and trailing whitespace.  Used to implement case-insensitivity in `SynonymDicts`

## Subclasses

The main utility of these classes comes in subclassing.  The standard approach is to create a subclass of `SynonymSet` that describes an object of some sort, and then to subclass `SynonymDict` to manage the set of entries.  Two examples are provided and tested and will someday be documented.


# Contributing

Fork or open an issue! Please!  I crave critical appraisals of my design and/or implementation decisions.

