import abc
from src.utils.hand import HandChecker


class Display(abc.ABC):
    def __init__(self):
        self.hand_checker = HandChecker()

    @abc.abstractmethod
    def show(self, game_state, *args, **kwargs):
        pass
