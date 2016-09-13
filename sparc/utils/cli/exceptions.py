
class CliUserWarning(UserWarning):
    """Basic CLI user exception"""

class CliInvalidInput(CliUserWarning):
    """User provided invalid input"""

class CliTooManyAtempts(CliUserWarning):
    """Too man attempts"""