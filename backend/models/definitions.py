from typing_extensions import TypedDict
from typing import Literal, List, Tuple
from enum import Enum, IntEnum
from pydantic import BaseModel


##############################################################################
######### CARD DEFINITIONS
##############################################################################


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
    ACE_LOW = 1
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
    ACE = 14   ## @TODO How to deal with the 2 possible values of ACE? just do it in the straight checks

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
class Card(BaseModel):
    suit: Suit  
    rank: Rank  

    def __str__(self) -> str:
        return f"{self.rank.name}_{self.suit.name}"
    
    def __repr__(self) -> str:
        return self.__str__()
    

class HandRankings(IntEnum):
    ROYAL_FLUSH = 1
    STRAIGHT_FLUSH = 2
    FOUR_OF_A_KIND = 3
    FULL_HOUSE = 4
    FLUSH = 5
    STRAIGHT = 6
    THREE_OF_A_KIND = 7
    TWO_PAIR = 8
    PAIR = 9
    HIGH_CARD = 10
    
    
##############################################################################
######## BETTING
##############################################################################

class BoardStage(str, Enum):
    PREFLOP = 'PREFLOP'
    FLOP = 'FLOP'
    TURN = 'TURN'
    RIVER = 'RIVER'
        
class PotState(TypedDict):
    call_total : int   # call_amount changes from player to player, so it is set
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

class PlayerStatus(str, Enum):
    ACTIVE = 'active'
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
    NO_ACTION = 'no-action'

    def to_status(self) -> PlayerStatus:
        keys = {
            'call': 'active',
            'raise': 'active',
            'fold' : 'fold',
            'check': 'active',
            'all-in': 'all-in'
        }
        return keys[self.value]


class PlayerBetResponse(TypedDict):
    pid : int
    sid : str
    player_funds : int
    amount_bet : int 
    role : PlayerRole
    action : PlayerAction
    hand : List[Card]



class PlayerPublicInfo(TypedDict):
    name : str
    pid : int
    sid : str
    funds : int
    role : PlayerRole
    current_bet : int
    last_action : PlayerAction
    betting_status : PlayerStatus

class PlayerPrivateInfo(TypedDict):
    cards : List[Card]

class PlayerState(TypedDict):
    public_info : PlayerPublicInfo
    private_info : PlayerPrivateInfo


class BettingRoundRecord(TypedDict):
    '''
    ## To save in database for subsequent analysis. 
    Not tested yet
    '''
    sid : str
    game_state : GameState     # the state before player made their move. 
    response : PlayerBetResponse # The move the player made given the pot_state
    player_state : PlayerState

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
