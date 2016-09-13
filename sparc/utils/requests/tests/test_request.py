import os
import unittest
import zope.testrunner
from zope import component
from sparc.testing.fixture import test_suite_mixin
from sparc.utils.testing import SPARC_UTILS_INTEGRATION_LAYER
from sparc.utils.requests.interfaces import IRequest
from zope.component import createObject

import sparc.utils.requests.request

class SparcUtilsRequestTestCase(unittest.TestCase):
    layer = SPARC_UTILS_INTEGRATION_LAYER
    sm = component.getSiteManager()
    
    def unregister_request(self):
        self.sm.unregisterUtility(
            component=sparc.utils.requests.request.SparcRequest, 
            provided=IRequest)
    
    def register_request(self):
        self.sm.registerUtility(
            component=sparc.utils.requests.request.SparcRequest, 
            provided=IRequest)

    def test_factory(self):
        self.assertTrue(IRequest.providedBy(createObject(u'sparc.utils.requests.request')))
    
    def test_singleton(self):
        self.assertTrue(IRequest.providedBy(self.sm.getUtility(IRequest)))
    
    def test_request_resolver(self):
        req = createObject(u'sparc.utils.requests.request')
        
        resolver = self.sm.getUtility(IRequest, u'sparc.utils.requests.request_resolver')
        self.assertIs(resolver(request=req), req)
        
        registered_req = self.sm.getUtility(IRequest)
        self.assertIs(resolver(), registered_req)
        
        self.unregister_request()
        self.assertIsNot(resolver(), registered_req)
        
        self.register_request()
        self.assertIs(resolver(), registered_req)
        

class test_suite(test_suite_mixin):
    layer = SPARC_UTILS_INTEGRATION_LAYER
    package = 'sparc.utils.requests'
    module = 'request'
    
    def __new__(cls):
        suite = super(test_suite, cls).__new__(cls)
        suite.addTest(unittest.makeSuite(SparcUtilsRequestTestCase))
        return suite


if __name__ == '__main__':
    zope.testrunner.run([
                         '--path', os.path.dirname(__file__),
                         '--tests-pattern', os.path.splitext(
                                                os.path.basename(__file__))[0]
                         ])