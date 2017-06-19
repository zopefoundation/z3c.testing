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
import unittest

from zope.container.tests.test_icontainer import BaseTestIContainer as BTIC
from zope.container.tests.test_icontainer import DefaultTestData
from zope.interface.verify import verifyObject, verifyClass


###############################################################################
#
# TestCase
#
###############################################################################
marker_pos = object()
marker_kws = object()


class TestCase(unittest.TestCase):

    iface = None
    klass = None
    pos = marker_pos
    kws = marker_kws

    def getTestInterface(self):
        if self.iface is not None:
            return self.iface

        msg = 'Subclasses has to implement getTestInterface()'
        raise NotImplementedError(msg)

    def getTestClass(self):
        if self.klass is not None:
            return self.klass

        raise NotImplementedError('Subclasses has to implement getTestClass()')

    def getTestPos(self):
        return self.pos

    def getTestKws(self):
        return self.kws

    def makeTestObject(self, object=None, *pos, **kws):
        # provide default positional or keyword arguments
        ourpos = self.getTestPos()
        if ourpos is not marker_pos and not pos:
            pos = ourpos

        ourkws = self.getTestKws()
        if ourkws is not marker_kws and not kws:
            kws = ourkws

        testclass = self.getTestClass()

        if object is None:
            # a class instance itself is the object to be tested.
            return testclass(*pos, **kws)
        else:
            # an adapted instance is the object to be tested.
            return testclass(object, *pos, **kws)


###############################################################################
#
# Public Base Tests
#
###############################################################################
class InterfaceBaseTest(TestCase):
    """Base test for IContainer including interface test."""

    def test_verifyClass(self):
        # class test
        self.assertTrue(
            verifyClass(self.getTestInterface(), self.getTestClass()))

    def test_verifyObject(self):
        # object test
        self.assertTrue(
            verifyObject(self.getTestInterface(), self.makeTestObject()))


###############################################################################
#
# IContainer Base Tests
#
###############################################################################
class BaseTestIContainer(InterfaceBaseTest, BTIC):

    def makeTestData(self):
        return DefaultTestData()

    def getUnknownKey(self):
        return '10'

    def getBadKeyTypes(self):
        return [None, ['foo'], 1, b'\xf3abc']
