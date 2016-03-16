# Configuration (this package only)
from importlib import import_module
from sparc.configuration.zcml import Configure as SparcConfigure
def Configure():
    SparcConfigure([import_module(__name__)])
def ConfigureTest():
    SparcConfigure([import_module(__name__)])

from interfaces import IReferenceAttributeCopier