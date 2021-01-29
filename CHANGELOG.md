# Changelog

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
