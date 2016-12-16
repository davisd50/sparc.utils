import requests
import warnings
from zope import component
from zope.component.factory import Factory
from zope import interface
from zope.schema.fieldproperty import FieldProperty
from .interfaces import IRequest, IRequestResolver
from sparc.configuration import container
from sparc.entity.entity import BaseSchemaObject 

@interface.implementer(IRequest)
class Request(BaseSchemaObject):
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

@interface.implementer(IRequestResolver)
def request_resolver(**kwargs):
    """Resolve for a IRequest and return
    
    This will return a IRequest based on the following resolution order:
    1. 'request' is given in kwargs and provides IRequest
    2.  IRequest is available as a unnamed utility in zca
    3.  A new IRequest is created and returned
    """
    if 'request' in kwargs and IRequest.providedBy(kwargs['request']):
        return kwargs['request']
    sm = component.getSiteManager()
    return sm.queryUtility(IRequest, default=requestFactory())

@interface.implementer(IRequest)
@component.adapter(container.ISparcAppPyContainerConfiguration)
class RequestFromSparcAppPyContainerConfiguration(Request):
    """Adapts from the first RequestOptions found"""
    def __init__(self, context):
        self.context = context
        RequestOptions = container.IPyContainerConfigValue(context).query('RequestOptions')
        if RequestOptions:
            if 'req_kwargs' in RequestOptions:
                self.req_kwargs = RequestOptions['req_kwargs']
            if 'gooble_warnings' in RequestOptions:
                self.gooble_warnings = RequestOptions['gooble_warnings']