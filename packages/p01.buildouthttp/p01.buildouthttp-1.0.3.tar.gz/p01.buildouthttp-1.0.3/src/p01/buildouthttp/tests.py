##############################################################################
#
# Copyright (c) 2015 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id:$
"""
__docformat__ = "reStructuredText"

import doctest
import unittest
import tempfile
import shutil


def setUp(test):
    test.globs['tmp'] = tempfile.mkdtemp()


def tearDown(test):
    shutil.rmtree(test.globs['tmp'])


def test_suite():
    uSuites = (
        doctest.DocFileSuite(
            'README.txt',
            setUp=setUp,
            tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            ),
        doctest.DocTestSuite(
            'p01.buildouthttp.buildouthttp',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            ),
        doctest.DocFileSuite('checker.txt', encoding='utf8',
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        )
    return unittest.TestSuite(uSuites)
