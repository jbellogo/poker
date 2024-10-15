'''
Card entities are Card object owners. Deck, Players, 

'''

from pydantic import BaseModel
from models.cards import Card, Suit, Rank
from typing import List, Union
import random
from enum import IntEnum
from models.entity import Entity



class BoardStage(IntEnum):
    ZERO = 0
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4


class Board(Entity):
    '''
    shows the community cards. 
    '''
    stage : BoardStage = 0

    # def __init__(self):
    #     super().__init__()

    def __str__(self) -> str:
        return super().__str__()
    
    def current_stage(self) -> BoardStage:
        return self.stage

    def next_stage(self) -> bool:
        indicator = self.stage < BoardStage.RIVER
        if indicator:
            self.stage +=1
        
        return indicator

    def best_hand(self, player_hand : List[Card]):
        pass

    def cards_dealt(self) -> int:
        if self.stage == BoardStage.PREFLOP:
            return 3
        if self.stage > BoardStage.PREFLOP:
            return 1
        return 0

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

    
    def deal_cards(self, entity : Entity) -> List[Card]:
        '''
        Removes card from deck and deals it to entity according to enty type.
        Removed cards returned for testing
        '''
        cards = []
        for i in range(0, entity.cards_dealt()):
            card = self.cards.pop()
            entity.add_card(card)    
            cards.append(card)   
        return cards
    
    def cards_dealt(self) -> int:
        return 0
    


        




