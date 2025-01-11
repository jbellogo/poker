from typing_extensions import TypedDict
from typing import Literal, List, Tuple
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
class BoardStage(IntEnum):
    # ZERO = 0     ### Can we get rid of this one?
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
        
class PotState(TypedDict):
    call_amount : int
    check_allowed : bool
    minimum_raise : int
    pot_size : int

class BoardState(TypedDict):
    cards : List[Card]
    stage : BoardStage

class GameState(TypedDict):
    '''
    Contains necessary pot and board information avaliable to players before acting.
    Board Stage is public information 
    '''
    pot: PotState
    board: BoardState


#
class PlayerStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive' # will have 10 players created, corresponding to 10 reserved seats but they only become active when someone joins a session.
    ALLIN = 'all-in'
    FOLDED = 'fold'

class PlayerRole(str, Enum):
    SMALL_BLIND = 'sb'
    BIG_BLIND = 'bb'
    OTHER = 'other'


class PlayerAction(str, Enum):
    CALL = 'call'
    RAISE = 'raise'
    FOLD = 'fold'
    CHECK = 'check'
    ALLIN = 'all-in'

    def to_status(self) -> PlayerStatus:
        keys = {
            'call': 'active',
            'raise': 'active',
            'fold' : 'fold',
            'check': 'active',
            'all-in': 'all-in'
        }
        return PlayerStatus(keys[self.value])





class PlayerBetResponse(TypedDict):
    pid : int
    player_funds : int
    amount_bet : int 
    role : Literal["sb", "bb", "other"] = "other"
    action : PlayerAction
    hand : Tuple[Card, Card]


class BettingRoundRecord(TypedDict):
    '''
    ## To save in database for subsequent analysis. 
    Not tested yet
    '''
    pid : int
    game_state : GameState     # the state before player made their move. 
    response : PlayerBetResponse # The move the player made given the pot_state

################################################################################################
################################################################################################
# Pending Implementation:
################################################################################################
################################################################################################
    


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
