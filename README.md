caseid
======

`caseid` is a Python library for getting information about Case Western Reserve
University students, faculty, and staff.  It interfaces with a few CWRU
resources that can provide different information depending on your needs.


caseid.directory
----------------

An interface to the [directory](https://webapps.case.edu/directory/index.html)
service.  This is actually a fairly useful service (there's even a phonetic
search), but it's slow and can't do searches in bulk.  This module provides two
functions, both of which work by scraping the results webpage.

The annoying limitation is that it doesn't provide students' Case IDs.  It just
gives a real-name alias email.  In order to view Case IDs, you must log in with
your own Case ID (which I haven't implemented yet and probably never will).


caseid.ldap
-----------

I plan to add an LDAP interface.  This would (at least, theoretically) allow you
to access Case IDs and a lot more interesting information about people.
Unfortunately, LDAP is a rather arcane sort of interface, and getting it right
may take a little time.


Installation
------------

Dependencies should be listed in `requirements.txt`.  You need to have those
installed to use this.  Then, just plop the `caseid` folder somewhere in your
Python path, and you're good to go.  Maybe one day I'll package this up on PyPI,
if anyone actually uses it.
