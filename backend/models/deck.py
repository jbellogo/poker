from models.definitions import *
from models.entity import Entity
import random
from typing import Optional
from models.board import Board

class Deck(Entity):

    seed : Optional[int] = None


    def shuffle(self):
        if self.seed is not None:
            random.seed(self.seed)
        random.shuffle(self.cards)
        random.shuffle(self.cards)

    def initialize(self):
        for suit in Suit.list():
            for rank in Rank.list():
                card = Card(suit=suit, rank=rank)
                self.add_card(card)
        self.shuffle()
    
    def deal_cards(self, entity : Entity) -> List[Card]:
        '''
        Removes card from deck and deals it to entity according to enty type.
        Removed cards returned for testing
        '''
        cards = []
        for _ in range(0, entity._cards_dealt()):
            card = self.cards.pop(0)
            entity.add_card(card)    
            cards.append(card)   
        return cards
    
    def _cards_dealt(self) -> int:
        return 0
    
