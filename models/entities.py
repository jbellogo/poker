'''
Entities are Card object owners. Deck, Players, 

'''

from pydantic import BaseModel
from models.cards import Card, Suit, Rank
from typing import List, Union
from abc import ABC, abstractmethod
import random


class Entity(BaseModel, ABC):
    '''A Card Owner'''
    cards : List[Card] = []

    # @abstractmethod
    def add_card(self, card : Card) -> None:
        self.cards.append(card)

    def length(self):
        return len(self.cards)
    
    def has(self, card: Card) -> bool:
        return card in self.cards      



class Player(Entity):
    ## status: inactive, active
    ## username?
    def make_move() -> None:
        pass 


class Board(Entity):
    pass



class Deck(Entity):
    def __init__(self):
        super().__init__()
        self.initialize_deck()
        self.shuffle()

    def initialize_deck(self):
        for suit in Suit.list():
            for rank in Rank.list():
                card = Card(suit=suit, rank=rank)
                self.add_card(card)

    def shuffle(self):
        random.shuffle(self.cards)
        random.shuffle(self.cards)

    
    def deal_card(self, entity : Union[Player, Board]) -> Card:
        '''
        Removes card from deck and deals it to entity.
        Removed card is returned for testing
        '''
        card = self.cards.pop()
        entity.add_card(card)
        return card

    
