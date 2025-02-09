from models.player import Player
from uuid import UUID
from models.definitions import *
import pprint



class Pot():
    '''
    Saves betting history in a single hand.
    awaits responses in methods betting_round()
    Gets Updated after every single player action. how would MVC design work?
    {
        "call_total" : 100,   # needs to match each player's current bet.
        "check_allowed" : False,
        "minimum_raise" : 80,
        "pot_size" : 0
    }
    '''   
    def __init__(self, sb_amount:int): 
        self.sb_amount : int = sb_amount 
        self.bb_amount : int = sb_amount*2
        self.pot_state : PotState = None
        self.initialize(board_stage="PREFLOP")
       

    def get_state(self) -> PotState:
        '''
        returns the necessary information about the pot state for any player to make a decision. 
        '''
        return self.pot_state.copy()
    

    def initialize(self, board_stage:BoardStage):
        struct = {
            'call_total' : self.bb_amount,
            'check_allowed' : False,
            'minimum_raise' : 2*self.bb_amount,
            'pot_size' : 0
        }
        if board_stage == "PREFLOP":
            struct['check_allowed'] = False
        else:
            struct['check_allowed'] = True
        self.pot_state = PotState(**struct)

    def collect_blinds(self, sb_amount : int):
        self.pot_state['pot_size'] += 3*sb_amount
    
    def update_pot_state(self, last_action : PlayerBetResponse, last_player_total: int, next_player_total : int) -> None:
        self.pot_state['pot_size'] += last_action['amount_bet']

        if last_action['action'] == 'raise' or last_action['action'] == 'all-in':
            self.pot_state['call_total'] = last_player_total
            self.pot_state['minimum_raise'] = 2*last_action['amount_bet']

        if next_player_total == self.pot_state['call_total']:
            self.pot_state['check_allowed'] = True
        else:
            self.pot_state['check_allowed'] = False


    def overwrite_state(self, new_pot_state : PotState):
        self.pot_state = new_pot_state
