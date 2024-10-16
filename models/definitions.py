from typing_extensions import TypedDict
from typing import Literal
from enum import Enum
from pydantic import BaseModel


############
# class BettingRoles(intEnum):
#     OTHER  = 0
#     SMALL_BLIND = 1
#     BIG_BLIND = 2

        
class PotState(TypedDict):
    call_amount : int
    check_allowed : bool
    minimum_raise : int
    pot_size : int


class PlayerBetResponse(BaseModel):
    pid : int
    player_funds : int
    role : Literal["sb", "bb", "other"] = "other"
    action : Literal["call", "raise", "fold"]
    amount_bet : int 
    # pot_state : PotState
    # blind_tax : int = - BettingRoles.value * SMALL_BLIND
    # def update_pot_state(self, new_state : PotState):
    #     self.pot_state = new_state

class BettingRoundRecord(TypedDict):
    response : PlayerBetResponse
    pot_state : PotState


class Hand(str, Enum):
    ROYAL_FLUSH = "royal_flush"
    STRAIGHT_FLUSH = "straight_flush"
    FOUR_OF_A_KIND = "four_of_a_kind"
    FULLHOUSE = "full_house"
    FLUSH = "flush"
    STRAIGHT = "straight"
    THREE_OF_A_KIND = "three_of_a_kind"
    TWO_PAIR = "two_pair"
    PAIR = "pair"
    HIGH_CARD = "high_card"
