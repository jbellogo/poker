from pydantic import BaseModel, PositiveInt, IntEnum
from enum import Enum

# class syntax
class Suit(str, Enum):
    SPADES = "spades"
    HEARTS = "hearts"
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    
class Rank(IntEnum):
    TWO = 2, "2"
    THREE = 3, "3"
    FOUR = 4, "4"
    FIVE = 5, "5"
    SIX = 6, "6"
    SEVEN = 7, "7"
    EIGHT = 8, "8"
    NINE = 9, "9"
    TEN = 10, "10"
    JACK = 11, "J"
    QUEEN = 12, "Q"
    KING = 13, "K"
    ACE = 14, "A"   ## How to deal with this? 
    

class Card(BaseModel):
    suit: Suit  
    value: Value  


