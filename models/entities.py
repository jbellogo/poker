'''
Entities are Card object owners. Deck, Players, 

'''

from pydantic import BaseModel
from models.cards import Card, Suit, Rank
from typing import List, Union
from abc import ABC, abstractmethod
import random
from enum import Enum, IntEnum



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


class Player(Entity):
    player_id : int
    number_cards_dealt : int = 2

    def cards_dealt(self) -> int:
        return self.number_cards_dealt


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

    
    def deal_cards(self, entity : Union[Player, Board]) -> List[Card]:
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
    


# class Hand(str, Enum):
#     '''
#     it should also have tie-breaking information
#     Each hand has a number associated with it. We use this number for breaking ties.
#     --Ex) Straight has the biggest number. In the event of two players having straights, 
#           the player whose straight hand has the maximum number wins.
#           Royal_flush has none. 
#           Straight Flush has largest number. 
#           Four_of_a_kind has the number. 
#           full_house has the triple number THEN the secondary number. 
#           flush has the suit ranks  
#           three of a kind the number 

#     '''

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





class Game():
    '''
    creates a deck, deals cards to board and players
    '''

    def __init__(self, num_players: int) -> None:
        self.deck : Deck = Deck()
        self.players : List[Player] = [Player(i) for i in range(0, num_players)]
        self.board : Board = Board()

    def start(self):
        for player in self.players:
            self.deck.deal_cards(player)
        while(self.board.next_stage()):
            print(self.board)
            ## betting 
            ##



