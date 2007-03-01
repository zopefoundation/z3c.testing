##############################################################################
#
# Copyright (c) 2006 Lovely Systems and Contributors.
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
"""A test layer to use a saved database.

The testlayer creates a database using a configurator and uses the
database for all tests.

$Id$
"""
__docformat__ = "reStructuredText"

import unittest
import os
import transaction

from ZODB.FileStorage import FileStorage

from zope import component
from zope import schema

from zope.app.appsetup import database
from zope.app.testing import functional
from zope.app.publication.zopepublication import ZopePublication
import sys

class BufferedDatabaseTestLayer(object):
    """A test layer which creates a filestorage database.
    
    The created database is later used without the need to run through the
    setup again.
    This speeds up functional tests.
    """

    __name__ = "BufferedTestLayer"
    __bases__ = ()
    path = None

    def __init__(self, config_file=None, module=__module__,
                 name="BufferedTestLayer"):
        self.config_file = config_file
        self.__module__ = module
        self.__name__ = name

    def setUpApplication(self, app):
        # to be overridden by subclass
        pass
        
    def setUp(self):

        dbpath = self.path or os.path.dirname(__file__)
        dbDirName = 'var_%s' % self.__module__
        if dbDirName not in os.listdir(dbpath):
            os.mkdir(os.path.join(dbpath, dbDirName))
        filename = os.path.join(dbpath, dbDirName, 'TestData.fs')

        fsetup = functional.FunctionalTestSetup(self.config_file)
        self.original = fsetup.base_storage

        if not os.path.exists(filename):
            import pdb; pdb.set_trace()
            # Generate a new database from scratch and fill it
            db = database(filename)
            connection = db.open()
            root = connection.root()
            app = root[ZopePublication.root_name]
            self.setUpApplication(app)
            transaction.commit()
            connection.close()
            db.close()

        fsetup.base_storage = FileStorage(filename)
        fsetup.setUp()

    def tearDown(self):
        fsetup = functional.FunctionalTestSetup()
        fsetup.base_storage.close()
        fsetup.base_storage = self.original
        fsetup.tearDown()

def createLayer(name='BufferedTestLayer', zcml=None, setUp=None):
    """Helper function for defining layers.

    Usage: defineLayer('foo')
    """
    globals = sys._getframe(1).f_globals
    if zcml is not None:
        zcml = os.path.join(os.path.split(globals['__file__'])[0], zcml)
    l = BufferedDatabaseTestLayer(zcml, globals['__name__'], name)
    if setUp is not None:
        l.setUpApplication = setUp
    return l
