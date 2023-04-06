from dataclasses import dataclass
from enum import Enum, auto
from typing import Union


class BetOption(Enum):
    check = auto()
    call = auto()
    bet = auto()
    fold = auto()


@dataclass
class BettingInfo:
    pass


@dataclass
class BettingDecision:
    choice: BetOption
    bet_amount: Union[float, int]


