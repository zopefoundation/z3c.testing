###############################################################################
#
# Copyright 2006 by refline (Schweiz) AG, CH-5630 Muri
#
###############################################################################
import os

from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
from ZODB.DemoStorage import DemoStorage

import doctest
from zope.app.publication.zopepublication import ZopePublication
from zope.app.testing import setup


###############################################################################
#
# Test component
#
###############################################################################

class ContextStub(object):
    """Stub for the context argument passed to evolve scripts.

    >>> from zope.app.zopeappgenerations import getRootFolder
    >>> context = ContextStub()
    >>> getRootFolder(context) is context.root_folder
    True

    """

    class ConnectionStub(object):
        def __init__(self, root_folder, db):
            self.root_folder = root_folder
            self.db = db

        def root(self):
            return {ZopePublication.root_name: self.root_folder}

        @property
        def _storage(self):
            return self.db._storage._base

        def get(self, oid):
            return self.db.open().get(oid)

    def __init__(self, rootFolder, db):
        self.root_folder = rootFolder
        self.connection = self.ConnectionStub(self.root_folder, db)


def getDBRoot(db):
    """Return the Zope root folder."""
    connection = db.open()
    root = connection.root()
    return root[ZopePublication.root_name]


def getDB(filename, package=None):
    """Return a DB by it's path."""
    if package is not None:
        filename = doctest._module_relative_path(package, filename)
        package = package.__file__
    else:
        package = __file__
    filename = os.path.join(os.path.dirname(package), filename)
    fileStorage = FileStorage(filename)
    storage = DemoStorage("Demo Storage", fileStorage)
    return DB(storage)


###############################################################################
#
# Test setup
#
###############################################################################

def setUpGeneration(test):
    setup.placefulSetUp()


def tearDownGeneration(test):
    setup.placefulTearDown()
