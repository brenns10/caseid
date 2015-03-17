#!/usr/bin/env python3
"""Python interface to the CWRU directory."""

from lxml import html
import requests

_DIRECTORY_URL = 'https://webapps.case.edu/directory/lookup'


class SearchResult(object):
    """Represents a directory search result.

    Exposes five result fields as attributes:
    * category - FACULTY/STAFF/STUDENT/etc..., as a string
    * name - full name as a string
    * phone - as a string, not likely to exist.
    * email - as a string, and it's the fullname version (not the caseid).
    * department - string, not likely to exist.
    """

    def __init__(self, row1, row2, category):
        """Create a directory search result from HTML tree.

        :param row1: The first row in the HTML result table.
        :param row2: The second row in the HTML result table.
        :param category: The heading this result was under.
        """

        self.category = category

        self.name = row1[0].text_content()
        self.phone = row1[1].text_content()

        self.email = row2[0].text_content()
        self.department = row2[1].text_content()

    def __str__(self):
        return '%s <%s>' % (self.name, self.email)

    def __repr__(self):
        return self.__str__()


class DirectorySearch(object):
    """A search class for the CWRU directory service."""

    def __init__(self, **args):
        """Creates a search object.  Kwargs are added as search args."""
        self._args = args

    def _generate_results(self, rows):
        """Generate SearchResults from a list of table rows."""
        rows = iter(rows)
        category = None  # contains last read category

        # Loop until next() raises a StopIteration.
        while True:

            r1 = next(rows)
            if r1[0].tag.lower() == 'th':
                # This row is a catgory header.
                category = r1[0].text_content()
            elif r1[0].attrib.get('class', '') == 'breaker':
                # This row is just padding.
                pass
            else:
                # This row is the first of a pair of rows corresponding to a
                # single search result.
                r2 = next(rows)
                yield SearchResult(r1, r2, category)

    def execute(self):
        """Run the search, returning an generator of SearchResult's."""
        page = requests.get(_DIRECTORY_URL, params=self._args)
        tree = html.fromstring(page.text)
        rows = tree.xpath('//table[@class="dirresults"]/tr')
        return list(self._generate_results(rows))


def directory_simple(search_text, search_method='regular'):
    """Run a simple directory search for a string.

    :param search_text: The search text
    :param search_method: Search method - 'regular' or 'phonetic'
    :return: A generator of SearchResult's
    """
    return DirectorySearch(search_text=search_text,
                           search_method=search_method).execute()


def directory_advanced(**kwargs):
    """Run an advanced directory search.

    Useful arguments are surname, givenname, category, and search_method.
    Category would be one of 'STUDENT', 'FACULTY', 'STAFF', or 'EMERITI'.
    Search_method would be either 'regular' or 'phonetic'.  Other (not very
    useful) arguments could be department and location.

    """
    options = {'search_text': '',
               'surname': '',
               'givenname': '',
               'department': '',
               'location': '',
               'category': 'all',
               'search_method': 'regular'}.update(kwargs)
    return DirectorySearch(**options).execute()
