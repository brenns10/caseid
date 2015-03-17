#!/usr/bin/env python3
"""Python interface to the CWRU directory."""

from lxml import html
import requests

_DIRECTORY_URL = 'https://webapps.case.edu/directory/lookup'


def _result(row1, row2, category):
    """Create a directory search result from HTML tree.

    :param row1: The first row in the HTML result table.
    :param row2: The second row in the HTML result table.
    :param category: The heading this result was under.
    """
    res = {}
    res['category'] = category
    res['name'] = row1[0].text_content()
    res['phone'] = row1[1].text_content()
    res['email'] = row2[0].text_content()
    res['department'] = row2[1].text_content()
    return res


def _generate_results(rows):
    """Generate results from a list of table rows."""
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
            yield _result(r1, r2, category)


def _search(**args):
    """Run the search, returning an generator of result dicts."""
    page = requests.get(_DIRECTORY_URL, params=args)
    tree = html.fromstring(page.text)
    rows = tree.xpath('//table[@class="dirresults"]/tr')
    return _generate_results(rows)


def simple(search_text, search_method='regular'):
    """Run a simple directory search for a string.

    :param search_text: The search text
    :param search_method: Search method - 'regular' or 'phonetic'
    :return: A generator of SearchResult's
    """
    return _search(search_text=search_text, search_method=search_method)


def advanced(**kwargs):
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
    return _search(**options)
