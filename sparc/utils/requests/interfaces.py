from zope.interface import Interface

class IRequestKwArgs(Interface):
    """A Python dict for Requests.api.request kwargs
    
    Implementers should make sure these objects can be passed into such as
    Requests.api.request(method, url, **implementation)
    
    Sample implementation:
        >>> from zope.interface import implements
        >>> class MyRequestKwArgs(dict):
        ...     implements(IRequestKwArgs)
    """
