##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
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
"""Setup for z3c.testing package

$Id$
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='z3c.testing',
      version='0.3.2',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='High-level Testing Support',
      long_description=(
          read('README.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      keywords = "zope3 testing layer zodb",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://pypi.python.org/pypi/z3c.testing',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['z3c'],
      extras_require=dict(test=[
          'zope.app.rotterdam',
          'zope.browserpage',
          'zope.browserresource',
          'zope.principalregistry',
          'zope.publisher',
          'zope.securitypolicy',
          'zope.testbrowser',
          ]),
      install_requires = ['setuptools',
                          'ZODB3',
                          'zope.app.appsetup',
                          'zope.app.publication',
                          'zope.app.testing',
                          'zope.container',
                          'zope.site',
                          'zope.component',
                          'zope.configuration',
                          'zope.interface',
                          'zope.testing',
                          ],
      include_package_data = True,
      zip_safe = False,
      )
