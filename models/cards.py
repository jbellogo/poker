from pydantic import BaseModel
from enum import Enum, IntEnum

# class syntax
class Suit(str, Enum):
    SPADES = "S"
    HEARTS = "H"
    CLUBS = "C"
    DIAMONDS = "D"

    @classmethod
    def list(cls):
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




