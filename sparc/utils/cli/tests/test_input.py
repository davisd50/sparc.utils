import os
import unittest
import zope.testrunner
from zope import component
from sparc.testing.fixture import test_suite_mixin
from sparc.utils.testing import SPARC_UTILS_INTEGRATION_LAYER

import sparc.utils.cli
from sparc.utils.cli.exceptions import CliTooManyAtempts, CliInvalidInput

class SparcUtilsCliInputTestCase(unittest.TestCase):
    layer = SPARC_UTILS_INTEGRATION_LAYER
    sm = component.getSiteManager()
    
    def test_factory(self):
        asker = component.createObject(u"sparc.utils.cli.input")
        self.assertTrue(sparc.utils.cli.ICliInput.providedBy(asker))
    
    def test_basic_input(self):
        asker = component.createObject(u"sparc.utils.cli.input")
        asker._raw_input = lambda :u"test1"
        asker._print = lambda x: None
        self.assertEquals(u"test1", asker.ask(u"this is a test"))

    def test_required(self):
        asker = component.createObject(u"sparc.utils.cli.input")
        asker._raw_input = lambda :u""
        asker._print = lambda x: None
        with self.assertRaises(CliTooManyAtempts):
            asker.ask(u"this should raise exception", required=True, tries=1)
        asker._raw_input = lambda :u"valid response"
        self.assertEquals(u"valid response", asker.ask(u"valid response", required=True, tries=1))


    _attempts = 0
    _succeed = 0
    def _raw_input(self):
        SparcUtilsCliInputTestCase._attempts += 1
        return u"" if SparcUtilsCliInputTestCase._succeed > SparcUtilsCliInputTestCase._attempts else u'a'
    
    def test_tries(self):
        asker = component.createObject(u"sparc.utils.cli.input")
        asker._raw_input = self._raw_input
        asker._print = lambda x: None
        
        SparcUtilsCliInputTestCase._attempts = 0
        SparcUtilsCliInputTestCase._succeed = 1
        self.assertEquals(u"a", asker.ask(u"valid response", required=True, tries=2))
        self.assertEquals(SparcUtilsCliInputTestCase._attempts, 1)
        
        SparcUtilsCliInputTestCase._attempts = 0
        SparcUtilsCliInputTestCase._succeed = 2
        self.assertEquals(u"a", asker.ask(u"valid response", required=True, tries=2))
        self.assertEquals(SparcUtilsCliInputTestCase._attempts, 2)
        
        SparcUtilsCliInputTestCase._attempts = 0
        SparcUtilsCliInputTestCase._succeed = 3 #one more than tries...will fail
        with self.assertRaises(CliTooManyAtempts):
            asker.ask(u"this should raise exception", required=True, tries=2)
        self.assertEquals(SparcUtilsCliInputTestCase._attempts, 2)

    def test_selections(self):
        asker = component.createObject(u"sparc.utils.cli.input")
        asker._raw_input = self._raw_input
        asker._print = lambda x: None
        
        selections = [('a','b','c')]
        
        SparcUtilsCliInputTestCase._attempts = 0
        SparcUtilsCliInputTestCase._succeed = 1
        self.assertEquals(u"c", asker.ask(u"valid response", tries=1, selections=selections))
        
        SparcUtilsCliInputTestCase._attempts = 0
        SparcUtilsCliInputTestCase._succeed = 2
        with self.assertRaises(CliTooManyAtempts):
            asker.ask(u"this should raise exception", tries=1, selections=selections)
            
        selections = [('a','b')]
        
        SparcUtilsCliInputTestCase._attempts = 0
        SparcUtilsCliInputTestCase._succeed = 1
        self.assertEquals(u"b", asker.ask(u"valid response", tries=1, selections=selections))
        
    def test_constraints(self):
        asker = component.createObject(u"sparc.utils.cli.input")
        asker._raw_input = self._raw_input
        asker._print = lambda x: None
        
        
        SparcUtilsCliInputTestCase._attempts = 0
        SparcUtilsCliInputTestCase._succeed = 1
        self.assertEquals(u"a", asker.ask(u"valid response", required=True, tries=2))
        self.assertEquals(SparcUtilsCliInputTestCase._attempts, 1)
        
        def _contraint(input_):
            raise CliInvalidInput('testing')

        SparcUtilsCliInputTestCase._attempts = 0
        SparcUtilsCliInputTestCase._succeed = 1
        with self.assertRaises(CliTooManyAtempts):
            asker.ask(u"this should raise exception", constraints=[_contraint])


class test_suite(test_suite_mixin):
    layer = SPARC_UTILS_INTEGRATION_LAYER
    package = 'sparc.utils.cli'
    module = 'input'
    
    def __new__(cls):
        suite = super(test_suite, cls).__new__(cls)
        suite.addTest(unittest.makeSuite(SparcUtilsCliInputTestCase))
        return suite


if __name__ == '__main__':
    zope.testrunner.run([
                         '--path', os.path.dirname(__file__),
                         '--tests-pattern', os.path.splitext(
                                                os.path.basename(__file__))[0]
                         ])