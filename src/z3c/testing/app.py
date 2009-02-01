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
"""
$Id$
"""

import unittest


###############################################################################
#
# TestCase
#
###############################################################################
marker_pos = object()
marker_kws = object()

class TestCase(unittest.TestCase):

    def getTestInterface(self):
        msg = 'Subclasses has to implement getTestInterface()'
        raise NotImplementedError, msg

    def getTestClass(self):
        raise NotImplementedError, 'Subclasses has to implement getTestClass()'

    def getTestPos(self):
        return marker_pos

    def getTestKws(self):
        return marker_kws
    
    def makeTestObject(self, object=None, *pos, **kws):
        # provide default positional or keyword arguments
        if self.getTestPos() is not marker_pos and not pos:
            pos = self.getTestPos()

        if self.getTestKws() is not marker_kws and not kws:
            kws = self.getTestKws()
       
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
from zope.interface.verify import verifyObject
from z3c.testing.verify import verifyClass


class InterfaceBaseTest(TestCase):
    """Base test for IContainer including interface test."""

    def test_verifyClass(self):
        # class test
        self.assert_(verifyClass(self.getTestInterface(), self.getTestClass())) 

    def test_verifyObject(self):
        # object test
        self.assert_(verifyObject(self.getTestInterface(), 
            self.makeTestObject()))


###############################################################################
#
# IContainer Base Tests
#
###############################################################################

from zope.container.tests.test_icontainer import BaseTestIContainer as BTIC
from zope.container.tests.test_icontainer import DefaultTestData


class BaseTestIContainer(InterfaceBaseTest, BTIC):

    def makeTestData(self):
        return DefaultTestData()

    def getUnknownKey(self):
        return '10'

    def getBadKeyTypes(self):
        return [None, ['foo'], 1, '\xf3abc']
