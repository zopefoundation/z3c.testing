##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Verify interface implementations

$Id$
"""
from zope.interface.exceptions import BrokenImplementation, DoesNotImplement
from zope.interface.exceptions import BrokenMethodImplementation
from types import FunctionType
from zope.interface.interface import fromMethod, fromFunction, Method
from zope.interface.verify import _incompat, MethodTypes


def _verify(iface, candidate, tentative=0, vtype=None):
    """Fix broken testing decorated methods.
    
    You can find such a broken interfaces test in z3c.proxy where the
    methods are decorated within ``@non_overridable``.
    """

    if vtype == 'c':
        tester = iface.implementedBy
    else:
        tester = iface.providedBy

    if not tentative and not tester(candidate):
        raise DoesNotImplement(iface)

    # Here the `desc` is either an `Attribute` or `Method` instance
    for name, desc in iface.namesAndDescriptions(1):
        if not hasattr(candidate, name):
            if (not isinstance(desc, Method)) and vtype == 'c':
                # We can't verify non-methods on classes, since the
                # class may provide attrs in it's __init__.
                continue

            raise BrokenImplementation(iface, name)

        attr = getattr(candidate, name)
        if not isinstance(desc, Method):
            # If it's not a method, there's nothing else we can test
            continue

        if isinstance(attr, FunctionType):
            # should never get here, since classes should not provide functions
            meth = fromFunction(attr, iface, name=name)
        elif (isinstance(attr, MethodTypes)
              and type(attr.im_func) is FunctionType):
            meth = fromMethod(attr, iface, name)
        elif isinstance(attr, property):
            # We can't verify decorated methods on classes.
            continue
        else:
            if not callable(attr):
                raise BrokenMethodImplementation(name, "Not a method")
            # sigh, it's callable, but we don't know how to intrspect it, so
            # we have to give it a pass.
            continue

        # Make sure that the required and implemented method signatures are
        # the same.
        desc = desc.getSignatureInfo()
        meth = meth.getSignatureInfo()

        mess = _incompat(desc, meth)
        if mess:
            raise BrokenMethodImplementation(name, mess)

    return True

def verifyClass(iface, candidate, tentative=0):
    return _verify(iface, candidate, tentative, vtype='c')
