from models.cards import Card, Suit, Rank
from typing import List
from abc import ABC, abstractmethod
from pydantic import BaseModel


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
    def cards_dealt(self) -> int:
        pass
