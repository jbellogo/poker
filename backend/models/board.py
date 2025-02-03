from models.definitions import *
from models.entity import Entity

class Board(Entity):
    '''
    shows the community cards. 
    '''
    stage : BoardStage = "PREFLOP"

    def __str__(self) -> str:
        return super().__str__()
    
    # def current_stage(self) -> BoardStage:
    #     return self.stage

    # def next_stage(self) -> bool:
    #     indicator = self.stage < BoardStage.RIVER
    #     if indicator:
    #         self.stage +=1
        
    #     return indicator
    def set_round(self, stage : BoardStage):
        self.stage = stage

    def best_hand(self, player_hand : List[Card]):
        pass

    def show(self)->None:
        print(self.cards) ## for now. 

    def get_state(self) -> BoardState:
        return BoardState(stage=self.stage, cards =self.cards)

    def _cards_dealt(self) -> int:
        '''Number of cards dealt. 3 on FLOP, 1 On turn, 1 on river.'''
        if self.stage == BoardStage.PREFLOP:
            return 3
        if self.stage > BoardStage.PREFLOP:
            return 1
        return 0