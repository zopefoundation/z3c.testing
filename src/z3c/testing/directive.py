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
try:
    from cStringIO import StringIO
except:
    from io import StringIO

from zope.configuration.xmlconfig import xmlconfig
from zope.configuration.xmlconfig import XMLConfig
import zope.component
import zope.security


# helper for directive testing
template = """<configure
   xmlns='http://namespaces.zope.org/zope'
   xmlns:browser='http://namespaces.zope.org/browser'
   xmlns:test='http://www.zope.org/NS/Zope3/test'
   i18n_domain='z3c'>
   %s
   </configure>"""


def registerDirective(directive, template=template):
    xmlconfig(StringIO(template % directive))


# Zope (content) Meta Directives
# ----------------------------------------------------------------------------

def setUpContentMetaDirectives():
    XMLConfig('meta.zcml', zope.component)()
    XMLConfig('meta.zcml', zope.security)()
