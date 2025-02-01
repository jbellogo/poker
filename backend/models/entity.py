'''
Abstract Base Class for Deck, Board, Players.
An entity is a card owner. 
'''

from pydantic import BaseModel
from models.definitions import *
from abc import ABC, abstractmethod

###  
### Entities are Card owners.

class Entity(BaseModel, ABC):
    '''A Card Owner'''
    cards : List[Card] = []

    def add_card(self, card : Card) -> None:
        self.cards.append(card)

    def length(self):
        return len(self.cards)
    
    def has(self, card: Card) -> bool:
        return card in self.cards      
    
    def __str__(self) -> str:
        return self.cards
    
    @abstractmethod
    def _cards_dealt(self) -> int:
        '''
        Number of cards, entity takes. 
        ej. Players take 2 cards, Board takes 3,1,1, etc
        '''
        pass


        




