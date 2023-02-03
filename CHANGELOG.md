# Changelog

### 0.2.3 (2023-02-03)

Added a new testcase for merging nonstandard CAS. Removed some verbose output from `CompartmentManager`

### 0.2.2 (2023-02-02)

Change approach to dealing with nonstandard CAS numbers.  On an input of '0034-56-7', the non-standard
entry (which still matches the regexp) should be accepted as a synonym, though other possible 
defective entries are not.  Inspired by defects observed in ecoinvent 'Naphtalene' _(sic)_.

Also renamed `compartments.compartment.NullContext` (exception) to `NullContextException`. 

### 0.2.1 (2021-03-17)

Fix error with improper adding of query terms to reverse-lookup dictionary (issue #6).

## 0.2.0 (2021-03-09)

Wrap-up release that encapsulates improvements with "non-specific" compartments and performance improvements.
 * Anything named "xxx, unspecified" is no longer considered distinct from the thing named "xxx" (close #4)
 * Tuples are now acknowledged as the "proper" way to reference a compartment
 * Major performance improvement when testing SynonymSet membership (0.1.6.post0)
 * Upgrade "example" cases to full-blown subclasses and improve exports

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
