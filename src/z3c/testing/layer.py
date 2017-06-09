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
"""
import os
import transaction
import shutil
from ZODB.FileStorage import FileStorage

from zope.app.appsetup import database
from zope.app.testing import functional
from zope.app.publication.zopepublication import ZopePublication
import sys
from zope.site import hooks


class BufferedDatabaseTestLayer(object):
    """A test layer which creates a filestorage database.

    The created database is later used without the need to run through the
    setup again.
    This speeds up functional tests.
    """

    __name__ = "BufferedTestLayer"
    __bases__ = ()
    path = None

    def __init__(self, config_file=None, module=__module__,  # noqa
                 name="BufferedTestLayer", path=None, clean=False):
        self.config_file = config_file or functional.Functional.config_file
        self.__module__ = module
        self.__name__ = name
        self.path = path
        self.dbDir = os.path.join(self.path,
                                  'var_%s' % self.__module__)
        if clean and os.path.isdir(self.dbDir):
            shutil.rmtree(self.dbDir)

    def setUpApplication(self, app):
        # to be overridden by subclass
        pass

    def setUp(self):
        if not os.path.exists(self.dbDir):
            os.mkdir(self.dbDir)
        filename = os.path.join(self.dbDir, 'TestData.fs')
        fsetup = functional.FunctionalTestSetup(self.config_file)
        self.original = fsetup.base_storage
        if not os.path.exists(filename):

            # Generate a new database from scratch and fill it
            db = database(filename)
            connection = db.open()
            root = connection.root()
            app = root[ZopePublication.root_name]
            # store the site, because the connection gets closed
            site = hooks.getSite()
            self.setUpApplication(app)
            transaction.commit()
            connection.close()
            db.close()
            hooks.setSite(site)

        # sets up the db stuff normal
        fsetup.setUp()
        # replace the storage with our filestorage
        fsetup.base_storage = FileStorage(filename)
        # override close on this instance, so files dont get closed on
        # setup/teardown of functionsetup
        fsetup.base_storage.close = lambda: None

    def tearDown(self):
        fsetup = functional.FunctionalTestSetup(self.config_file)
        # close the filestorage files now by calling the original
        # close on our storage instance
        FileStorage.close(fsetup.base_storage)
        # replace the storage with the original, so functionalsetup
        # can do what it wants with it
        fsetup.base_storage = self.original
        fsetup.tearDown()
        fsetup.tearDownCompletely()


def defineLayer(name, zcml=None, appSetUp=None, clean=False):
    """Helper function for defining layers.

    Defines a new buffered database layer

    :name: the name of the layer in the module
    :zcml: optional zcml file relative to package dir
    :appSetUp: a callable which takes an application object as argument
    :clean: if True the database directory is deleted on init
    """
    globals = sys._getframe(1).f_globals
    if zcml is not None:
        zcml = os.path.join(os.path.split(globals['__file__'])[0], zcml)
    l = BufferedDatabaseTestLayer(
        zcml, globals['__name__'], name,
        path=os.path.dirname(globals['__file__']),
        clean=clean)
    if appSetUp is not None:
        l.setUpApplication = appSetUp
    globals[name] = l
