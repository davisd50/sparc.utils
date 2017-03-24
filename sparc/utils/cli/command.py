import os
from zope import interface
from zope.component.factory import Factory
from .interfaces import ICommandLaunch

@interface.implementer(ICommandLaunch)
class CommandLaunch(object):
    
    def __init__(self, name, arguments=None, parent=None):
        """Initialize a ICommandLaunch object
        
        If location is not specified, system path will be searched to find 
        executable.
        
        Args:
            name: String executable name to launch
        
        Kwargs:
            arguments: List of command argument strings to use in command line launch string
            parent: String directory path containing executable to be used
        
        Returns:
            Argument list that can be delivered to subprocess.call() as *args
        """
        self._arguments = arguments if arguments  else []
        
        # ILocation
        self.__name__ = name
        self.__parent__ = parent if parent else self._get_parent(self.__name__)

    def _get_parent(self, name):
        for p in os.getenv('PATH').split(os.path.pathsep):
            if os.path.exists(os.path.join(p,name)):
                return p
        raise LookupError("expected to find executable {} in system path".format(name) )

    # ICommandLaunch
    def __iter__(self):
        #return [os.path.join(self.__name__, self.__location__)] + self._arguments
        for arg in [os.path.join(self.__parent__, self.__name__)] + self._arguments:
            yield arg
    
    def validate(self):
        return os.access(os.path.join(self.__parent__, self.__name__), os.X_OK)

CommandLaunchFactory = Factory(CommandLaunch, u'sparc.asset.command_launch')

