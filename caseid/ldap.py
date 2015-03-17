#!/usr/bin/env python3
"""Python interface to CWRU LDAP for student lookups."""

import ldap3

_ADDRESS = 'ldap.case.edu'
_PORT = 389
_BASE = 'ou=People,o=cwru.edu,o=isp'
_ATTR = ('sn', 'cn', 'uid', 'mail', 'eduPersonScopedAffiliation')


def _get_server():
    return ldap3.Server(_ADDRESS, port=_PORT)


def _get_connection():
    return ldap3.Connection(_get_server())


def _search(filter):
    c = _get_connection()
    c.open()
    c.search(_BASE, filter, ldap3.SUBTREE, attributes=_ATTR)
    results = [entry['attributes'] for entry in c.response]
    c.unbind()
    return results


def id(caseid):
    return _search('(uid=%s)' % caseid)


def name(name):
    return _search('(cn=%s)' % name)
