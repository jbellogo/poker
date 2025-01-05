from typing_extensions import TypedDict
from typing import Literal
from enum import Enum, IntEnum
from pydantic import BaseModel



# Card definitions
class Suit(str, Enum):
    SPADES = "S"
    HEARTS = "H"
    CLUBS = "C"
    DIAMONDS = "D"

    @classmethod
    def list(cls):
        ''' Called Suit.list()???'''
        return list(map(lambda c: c.value, cls))
    
class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14   ## How to deal with this? just do it in the straight checks

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    

## BaseModel is only for these simple classes
class Card(BaseModel):
    suit: Suit  
    rank: Rank  

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

######## BETTING
        
class PotState(TypedDict):
    call_amount : int
    check_allowed : bool
    minimum_raise : int
    pot_size : int


class PlayerBetResponse(TypedDict):
    pid : int
    player_funds : int
    role : Literal["sb", "bb", "other"] = "other"
    action : Literal["call", "raise", "fold", "check"]
    amount_bet : int 
    # pot_state : PotState
    # blind_tax : int = - BettingRoles.value * SMALL_BLIND
    # def update_pot_state(self, new_state : PotState):
    #     self.pot_state = new_state


################################################################################################
################################################################################################
# Pending Implementation:
################################################################################################
################################################################################################
    
# class BettingRoundRecord(TypedDict):
#     '''
#     ## To save in database for subsequent analysis. 
#     Not tested yet
#     '''
#     response : PlayerBetResponse # The move the player made given the pot_state
#     pot_state : PotState # the state before player made their move. 


# class BettingRoles(intEnum):
#     OTHER  = 0
#     SMALL_BLIND = 1
#     BIG_BLIND = 2


# class Hand(str, Enum):
#     ROYAL_FLUSH = "royal_flush"
#     STRAIGHT_FLUSH = "straight_flush"
#     FOUR_OF_A_KIND = "four_of_a_kind"
#     FULLHOUSE = "full_house"
#     FLUSH = "flush"
#     STRAIGHT = "straight"
#     THREE_OF_A_KIND = "three_of_a_kind"
#     TWO_PAIR = "two_pair"
#     PAIR = "pair"
#     HIGH_CARD = "high_card"
