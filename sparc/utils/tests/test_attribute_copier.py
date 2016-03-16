import unittest
from doctest import DocTestSuite
from doctest import DocFileSuite

import sparc.utils

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('attribute_copier.txt',
                     package=sparc.utils),))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')