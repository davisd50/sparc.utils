import requests
import warnings
from zope.component import getSiteManager
from zope.component.factory import Factory
from zope.interface import implementer
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from interfaces import IRequest
from sparc.entity.entity import BaseSchemaObject 

class Request(BaseSchemaObject):
    implements(IRequest)
    req_kwargs = FieldProperty(IRequest['req_kwargs'])
    gooble_warnings = FieldProperty(IRequest['gooble_warnings'])
    
    def request(self, *args, **kwargs):
        kwargs_updated = self.req_kwargs.copy()
        kwargs_updated.update(kwargs)
        if self.gooble_warnings:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return requests.request(*args, **kwargs_updated)
        else:
            return requests.request(*args, **kwargs_updated)
requestFactory = Factory(Request)
SparcRequest = requestFactory()

@implementer(IRequest)
def request_resolver(**kwargs):
    """Resolve for a IRequest and return
    
    This will return a IRequest based on the following resolution order:
    1. 'request' is given in kwargs and provides IRequest
    2.  IRequest is available as a unnamed utility in zca
    3.  A new IRequest is created and returned
    """
    if 'request' in kwargs and IRequest.providedBy(kwargs['request']):
        return kwargs['request']
    sm = getSiteManager()
    return sm.queryUtility(IRequest, default=requestFactory())