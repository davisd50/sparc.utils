from zope.component.factory import Factory
from zope.interface import implements
from interfaces import IRequestKwArgs

class RequestKwArgs(dict):
    implements(IRequestKwArgs)
requestKwArgsFactory = Factory(RequestKwArgs)