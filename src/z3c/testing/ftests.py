import layer
from zope.app.testing import functional
import unittest

MyLayer = layer.createLayer(zcml='test.zcml')

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
