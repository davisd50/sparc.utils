import requests
import warnings
from zope.component.factory import Factory
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
                return requests.request(*args, **kwargs_updated)
        else:
            return requests.request(*args, **kwargs_updated)
requestFactory = Factory(Request)