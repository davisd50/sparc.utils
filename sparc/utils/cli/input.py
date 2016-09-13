from zope import interface
from zope.component.factory import Factory

from .exceptions import CliInvalidInput, CliTooManyAtempts
from interfaces import ICliInput
from __builtin__ import int


class CliInput(object):
    interface.implements(ICliInput)
    
    def _get_return_value(self, input_):
        if not self._selections:
            return input_
        for sel in self._selections:
            if input_ == sel[0]:
                return sel[2]
        # shouldn't ever get here
        raise AssertionError("Unknown internal code error.")

    def _raw_input(self):
        return raw_input() #blocks
    
    def _get_input(self, constraints):
        input_ = self._raw_input()
        self._check_constraints(input_, constraints)
        return self._get_return_value(input_)
    
    def _check_constraints(self, input_, constraints):
        for constraint in constraints:
            constraint(input_)
    
    def _required(self, input_):
        if not input_:
            raise CliInvalidInput(u"Expected non empty string.")
    
    def _selection_constraint(self, input_):
        for sel in self._selections:
            if input_ == sel[0]:
                return
        raise CliInvalidInput(u"Expected valid selection choice.")
    
    def _prepare_selections(self, selections = ()):
        new = []
        for sel in selections:
            new.append(sel if len(sel)>2 else (sel[0], sel[1], sel[1]))
        return new

    def _print(self, text):
        print text

    def ask(self, question, required = True, tries = 3, selections = (), constraints = ()):
        tries = abs(int(tries)) if abs(int(tries)) else 1
        constraints = list(constraints) if constraints else []
        self._selections = self._prepare_selections(selections)
        
        if required:
            constraints.append(self._required)
        if selections:
            constraints.append(self._selection_constraint)
        
        self._print(question)
        
        for sel in selections:
            self._print("(" + sel[0] + ") " + sel[1])
        
        _attempts = 0
        while _attempts < tries:
            if _attempts:
                self._print(u"Invalid input, please try again.")
            try:
                input_ = self._get_input(constraints) # blocks
            except CliInvalidInput as e:
                self._print(str(e))
                _attempts += 1
            else:
                return input_
        raise CliTooManyAtempts

cliInputFactory = Factory(CliInput)