from models.definitions import *
from models.entity import Entity
from models.deck import Deck

class Board(Entity):
    '''
    shows the community cards. 
    '''
    stage : BoardStage = "PREFLOP"

    def __str__(self) -> str:
        return super().__str__()
    
    # def _set_state(self, state : BoardState):
    #     self.stage = state['stage']
    #     self.cards = state['cards']

    def set_stage(self, stage : BoardStage):
        '''Sets the stage and deals the cards.'''
        self.stage = stage


    def show(self)->None:
        print(self.cards) ## for now. 

    def get_state(self) -> BoardState:
        return BoardState(stage=self.stage, cards =self.cards)

    def _cards_dealt(self) -> int:
        '''Number of cards dealt. 3 on FLOP, 1 On turn, 1 on river.'''
        if self.stage == "FLOP":
            return 3
        elif self.stage == "TURN" or self.stage == "RIVER":
            return 1
        else:
            return 0