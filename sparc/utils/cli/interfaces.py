from zope import interface
from zope import location

class ICliInput(interface.Interface):
    def ask(question, required = True, tries = 3, selections = (), constraints = ()):
        """Ask for user input from STDIN (i.e. CLI)
        
        Warning: this method interacts with STDOUT and will block until the
                 responds via STDIN.
        
        Args:
            question: Text question to display to user for input
        kwargs:
            required: True indicates to continue to ask question until a valid
                      answer is given or until attempts is reached (if 
                      specified)
            selections: a sequence of tuples with either 2 or 3 entries.  The
                        first entry is a string that indicates the selection
                        choice (1, 2, 3 or a, b, c etc...).  The second is text
                        that gives the selection option description.  The
                        third (optional) entry is the return value of the user
                        selected choice (else the return value is second tuple
                        entry)
            tries: Number of tries the user should be given to input a valid
                   response before CliTooManyAtempts is raised.  This will
                   print messages to STDOUT for invalid attempts.
            constraint:  iterable of Callables raising CliInvalidInput if
                         user input does not pass contraint check.
        Raises:
            .exceptions.CliInvalidInput
            .exceptions.CliTooManyAtempts
        Returns:
            if no selections, then direct user input
            if selections, then
                tuple entry 3 (if given) of selected entry else tuple entry 2
        """

class ICommandLaunch(location.ILocation):
    """Create Python subprocess.call() arguments with potentially unknown executable location
    
    Also provides ILocation where __parent__ is the directory the executable
    is location and __name__ is the executable.
    """
    
    def __iter__():
        """iterator of args that can be delivered to subprocess.call()"""
    
    def validate():
        """True if executable can be located (Windows) and can be executed (Unix)"""