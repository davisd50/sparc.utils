from zope import schema
from zope.interface import Interface


class IRequest(Interface):
    """Provides requests.request implementation"""
    req_kwargs = schema.Dict(
            title=u'kwargs',
            description=u'A dict-like object containing a default set of' +\
                        u'kwargs to be used by request()')
    gooble_warnings = schema.Bool(
            title=u'Gooble warnings',
            description=u'True indicates to gooble warnings issued by calls to request()',
            default=False)
    def request(*args,**kwargs):
        """wrapper for requests.request
        
        kwargs delivered to method will over-ride competing entries found in
        IRequest.req_kwargs defaults
        """