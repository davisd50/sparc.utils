from zope.interface import Interface

from .exceptions import CliTooManyAtempts

class ICliInput(Interface):
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
            CliInvalidInput
            CliTooManyAtempts
        Returns:
            if no selections, then direct user input
            if selections, then
                tuple entry 3 (if given) of selected entry else tuple entry 2
        """