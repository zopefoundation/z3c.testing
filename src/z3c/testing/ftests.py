import layer
from zope.app.testing import functional
import unittest

layer.defineLayer('MyLayer', zcml='test.zcml')

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
