from zope import schema
from zope.interface import Interface


class IRequest(Interface):
    """Provides requests.request implementation"""
    req_kwargs = schema.Dict(
            title=u'kwargs',
            description=u'A dict-like object containing a default set of' +\
                        u'kwargs to be used by request()',
            default={})
    gooble_warnings = schema.Bool(
            title=u'Gooble warnings',
            description=u'True indicates to gooble warnings issued by calls to request()',
            default=False)
    def request(*args,**kwargs):
        """wrapper for requests.request
        
        kwargs delivered to method will over-ride competing entries found in
        IRequest.req_kwargs defaults
        """

class IRequestResolver(Interface):
    def __call__(request=None):
        """Return IRequest provider
        
        Return an appropriate IRequest provider based on the following
        resolution order for the related requests.request object:
         - return kwarg['request'] if it provides IRequest
         - return unnamed utility singleton providing IRequest in ZCA if found
         - return newly created IRequest with new requests.request
        
        kwargs:
            request: IRequest provider
        """