from zope.interface import Interface

class IReferenceAttributeCopier(Interface):
    """Shallow copy object attribute and schema field values
    
    This will copy the attribute and schema field values on from_object onto
    to_object.  Python object attributes will be created on to_object if they
    don't already exist.
    
    This only copies object references, it does not deep-copy mutable objects 
    such as Python lists.
    """
    def __call__(from_object, to_object, *interfaces):
        """copies all Attributes contained in interfaces list"""