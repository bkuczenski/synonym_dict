# synonym_dict

A class that allows retrieval of a given object by any of its synonyms.

# Overview

There are many situations in which an object may be known by several names.  `synonym_dict` provides a way to:

  1. Retrieve an object by its name or any synonyms
  2. Ensure that synonyms are distinct and non-overlapping
  3. Support case-insensitive tests

## Installation

```{python}
$ pip install synonym_dict
```

The package has no dependencies.

### Testing

```{python}
$ python -m unittest
```

Or, on `python2`:
```{python}
$ python -m unittest discover
```

# SynonymSet

A Synonym