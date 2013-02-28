##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
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
"""Tests for z3c.testing

$Id$
"""
import unittest
import zope.interface
try:
    from zope.app.testing import functional
    from z3c.testing import layer
    HAVE_FTEST = True
except ImportError:
    HAVE_FTEST = False

from z3c import testing

def appSetUp(app):
    # just some stupid assertion
    assert(app.__name__ is None)


MyLayer = None
if HAVE_FTEST:
    layer.defineLayer('MyLayer', zcml='test.zcml',
                      appSetUp=appSetUp, clean=True)

class ISample(zope.interface.Interface):
    """Sample interface."""

@zope.interface.implementer(ISample)
class Sample(object):
    """Sample object."""


class TestTestCase(testing.InterfaceBaseTest):

    def getTestClass(self):
        return Sample

    def getTestInterface(self):
        return ISample


class ExamplePage(object):

    def __call__(self):
        return "Example succeeded."


def test_suite():
    suite = unittest.TestSuite()
    # Unit Tests
    suite.addTest(unittest.makeSuite(TestTestCase))
    # Functional Tests
    if HAVE_FTEST:
        suites = (
            functional.FunctionalDocFileSuite('BROWSER.txt'),
            # test setup/teardown by calling it twice
            functional.FunctionalDocFileSuite('BROWSER.txt'),
            )
        for s in suites:
            s.layer=MyLayer
            suite.addTest(s)
    return suite
