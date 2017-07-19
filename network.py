import random as r  # to ensure the tie-breaking property

from settings import VALIDATOR_NAMES
from view import View
from validator import Validator


class Network:
    def __init__(self):
        self.validators = dict()
        for v in VALIDATOR_NAMES:
            self.validators[v] = Validator(v)
        self.global_view = set()

    @profile
    def propagate_message_to_validator(self, message, validator_name):
        assert message in self.global_view, "...expected only to propagate messages from the global view"
        self.validators[validator_name].receive_messages(set([message]))

    def get_message_from_validator(self, validator_name):
        assert validator_name in VALIDATOR_NAMES, "...expected a known validator"

        if self.validators[validator_name].decided:
            return True

        new_message = self.validators[validator_name].make_new_message()
        self.global_view.add(new_message)
        return new_message

    def random_propagation_and_message(self):

        destination = r.choice(tuple(VALIDATOR_NAMES))
        if len(self.global_view) == 0:
            self.get_message_from_validator(destination)
        else:
            message = r.choice(tuple(self.global_view))
            self.propagate_message_to_validator(message, destination)
            self.get_message_from_validator(destination)

    # def let_validator_push

    def view_initialization(self, view):
        assert isinstance(view, View)
        self.global_view = view.messages

        latest = view.latest_messages

        for v in latest:
            self.validators[v].receive_messages(set([latest[v]]))

    def random_initialization(self):
        for v in VALIDATOR_NAMES:
            self.get_message_from_validator(v)

    def report(self, safe_messages, edges):
        messageset = set()
        for v in VALIDATOR_NAMES:
            if self.validators[v].my_latest_message() is not None:
                messageset.add(self.validators[v].my_latest_message())

#        View(messageset).plot_view(safe_messages, use_edges=edges)
