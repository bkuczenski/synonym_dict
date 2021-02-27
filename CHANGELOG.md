# Changelog

### 0.1.6 (2021-02-19)

Nonspecific child compartments submitted to `CompartmentManager.__getitem__` can be bypassed. 
I think we are getting close to 0.2.0 here!

 - `post0` (2021-02-24) Major performance improvement on `SynonymSet.__contains__`

### 0.1.5 (2021-02-19)

Bug fixes: patch a recursion bomb, leaky subcompartments. 'attach' method for avoiding lineage
conflicts.

 - `.post0` - test code changes for ease of subclassing

### 0.1.4 (2021-01-29)

Add CAS number detection to Flowables.add_synonym().  Previously it had only worked on new_entry.

### 0.1.3 (2020-12-27)

Don't check every query for NONSPECIFIC_LOWER.

Now, it's debatable that the right solution here is to actually have the null_entry _be_ an entry, whose synonyms 
are exactly the NONSPECIFIC terms.  After all, isn't the whole point of this to return specific entries for specific
query terms?  But for WHATEVER reason I took steps to prevent the null_entry from having any other terms besides
'None', and I hate to second-guess myself.  But please note that this issue should perhaps be revisited. 

### 0.1.2 (2020-12-27)

When compartments are presented as lists, parent names added for disambiguation should be stripped back out.

### 0.1.1 (2020-05-28)

Typical rookie errors in first-ever PyPI upload

### 0.1.0 (2020-05-27)

First public release.
