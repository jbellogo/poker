from pydantic import BaseModel
from .cards import Card, Suit, Rank
from types import List, Union
from abc import ABC, abstractmethod
import random


class Entity(BaseModel, ABC):
    '''A Card Owner'''
    cards : List[Card] = []

    # @abstractmethod
    def add_card(self, card : Card):
        self.cards.append(card)


class Player(Entity):
    pass 


class Board(Entity):
    pass



class Deck():
    def __init__(self):
        self.cards = []
        self.initialize_deck()
        self.shuffle()

    def initialize_deck(self):
        for suit in Suit.list():
            for rank in Rank.list():
                card = Card(suit=suit, rank=rank)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)
        random.shuffle(self.cards)

    
    def deal_card(self, entity :Union[Player, Board]):
        '''removes card from deck and deals it to entity'''
        card = self.cards.pop()
        entity.add_card(card)
