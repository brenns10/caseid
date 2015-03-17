caseid
======

`caseid` is a Python library for getting information about Case Western Reserve
University students, faculty, and staff.  It interfaces with a few CWRU
resources that can provide different information depending on your needs.

**WARNING:** This library is, like, rough.  It doesn't really do any input
checks, and it doesn't really do any post-processing of output.  I'm thinking of
adding such features, (so that all search results have similar formats).  But
right now, don't expect that the return values of these functions will act the
same forever.


caseid.directory
----------------

An interface to the [directory](https://webapps.case.edu/directory/index.html)
service.  This is actually a fairly useful service (there's even a phonetic
search), but it's slow and can't do searches in bulk.  This module provides two
functions, both of which work by scraping the results webpage.

The annoying limitation is that it doesn't provide students' Case IDs.  It just
gives a real-name alias email.  In order to view Case IDs, you must log in with
your own Case ID (which I haven't implemented yet and probably never will).

### Functions

* `caseid.directory.simple(search_text, search_method='regular'`: Simple search.
  Just searches any text.  `search_method` can take the value `'phonetic'`,
  which performs a phonetic search (offered by the directory service, YMMV).
* `caseid.directory.advanced(**kwargs)`: Advanced search.  Can take arguments:
    * `surname`
    * `givenname`
    * `department` - not listed for most, really not that useful.
    * `location` - I have no idea what this is.
    * `category` - `'STUDENT'`, `'FACULTY'`, `'STAFF'`, or `'EMERITI'`.
    * `search_method` - regular by default, but can do phonetic as well
      (theoretically).

All these functions return an iterator of dictionaries, which have the following
attributes:

* `category` - as above
* `name` - full name
* `phone` - as a string (not likely to exist)
* `email` - again, it's a full name alias
* `department` - not likely to exist

### Example

```python
from caseid import directory

for result in directory.simple('Stephen'):
    # Send every Stephen at Case an email.  You monster.
```


caseid.ldap
-----------

This is an interface to the shady underworld of CWRU's LDAP server.  This poorly
documented horror show probably holds more secrets than ITS would like to think
are accessible to the public.  But since they're undocumented, they're probably
safe.  Unfortunately, since they're undocumented, I don't know what attributes
hold important information for searching.

On the bright side, LDAP shows off everybody's Case ID like nobody's business.
So if you need a Case ID, or you already know it, LDAP can get you a result much
better than the directory.

The functions below return lists of results.  Each result is a dictionary.  The
dictionaries contain attributes that exist in LDAP (which don't provide much
information beyond a name and email address).

### Functions

* `caseid.ldap.id(caseid)`: Search for a given Case ID.  Returns a dictionary
  full of goodies that I'm too tired to document right now.  Try it and see.
* `caseid.ldap.name(name)`: Search for a name.  Allows the `*` wildcard.  Use
  with caution.  Get ready for an unreasonable amount of results, because I
  don't think they purge old accounts.


### Example

```python
from caseid import ldap

print(ldap.id('smb196'))
# Hey, that's me!

print(ldap.name('Stephen *'))
# Sploosh!  Tons of results.
```


Installation
------------

Dependencies should be listed in `requirements.txt`.  You need to have those
installed to use this.  Then, just plop the `caseid` folder somewhere in your
Python path, and you're good to go.  Maybe one day I'll package this up on PyPI,
if anyone actually uses it.
