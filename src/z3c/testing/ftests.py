import layer
from zope.app.testing import functional
import unittest

def appSetUp(app):
    # just some stupid assertion
    assert(app.__name__ is None)


layer.defineLayer('MyLayer', zcml='test.zcml',
                  appSetUp=appSetUp, clean=True)


def test_suite():
    suite = unittest.TestSuite()
    suites = (
        functional.FunctionalDocFileSuite('BROWSER.txt'),
        )
    for s in suites:
        s.layer=MyLayer
        suite.addTest(s)
        return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
