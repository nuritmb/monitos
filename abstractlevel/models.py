
from typing import List, Dict

class MonkeySays(List[str]):
    def __init__(self, statelist: List[int]) -> None:
            self.statelist = statelist

class MonkeySees(List[int]):
    def __init__(self, statelist: List[int]) -> None:
            self.statelist = statelist

class MonkeyHears(List[int]):
    def __init__(self, statelist: List[int]) -> None:
            self.statelist = statelist

class MonkeyDoes(List[int]):
    def __init__(self, statelist: List[int]) -> None:
        self.statelist = statelist

class Monkey:
    def __init__(self, wordmap: Dict[MonkeySees, MonkeySays], actionmap: Dict[MonkeyHears, MonkeyDoes]) -> None:
        self.wordmap = wordmap
        self.actionmap = actionmap

    def emmit(self, perception: MonkeySees) -> MonkeySays:
        return self.wordmap[perception]

    def receive(self, perception: MonkeyHears) -> MonkeyDoes:
        return self.actionmap[perception]