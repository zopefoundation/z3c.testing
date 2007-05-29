#!python
from setuptools import setup, find_packages

setup(name='z3c.testing',
      version='0.1',
      author = "Zope Community",
      author_email = "zope3-dev@zope.org",
      description = "Test Helpers for Zope3",
      license = "ZPL 2.1",
      keywords = "zope zope3 testing",
      url='http://svn.zope.org/z3c.testing',
      zip_safe=False,
      packages=find_packages('src'),
      include_package_data=True,
      package_dir = {'':'src'},
      namespace_packages=['z3c',],
      install_requires = ['setuptools',
                          # the layer does not work with 3.8
                          # it throughs an IOError, because somewhere
                          # a file is closed too early
                          'ZODB3 < 3.8a',
                          'zope.app.appsetup',
                          'zope.app.container',
                          'zope.app.folder',
                          'zope.app.publication',
                          'zope.app.security',
                          'zope.app.testing',
                          'zope.component',
                          'zope.configuration',
                          'zope.interface',
                          'zope.testing',
                          ],
      )

