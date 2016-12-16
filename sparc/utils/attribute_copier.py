from zope.interface import Attribute
from zope.interface import implementer
from zope.schema.interfaces import IField
from .interfaces import IReferenceAttributeCopier

@implementer(IReferenceAttributeCopier)
def attribute_copier(from_object, to_object, *interfaces):
    """copies all Attributes contained in interfaces list"""
    flatten = set()
    for iface in interfaces:
        
        for attr in [atr for atr in iface if 
                     (type(iface[atr])==Attribute
                        or IField.providedBy(iface[atr]))
                     ]:
            flatten.add(attr)
    
    for attr in flatten:
        if not hasattr(to_object, attr):
            setattr(to_object, attr, getattr(from_object, attr))
        else:
            if getattr(from_object, attr) != getattr(to_object, attr):
                setattr(to_object, attr, getattr(from_object,attr))