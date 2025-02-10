from models.player import Player
from uuid import UUID
from models.definitions import *
import pprint

## There is no way to set the board stage for now


class Pot():
    '''
    Contains betting state/rules.
    Gets Updated after every single player action.
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
    

    def initialize(self, board_stage : BoardStage):
        pot_size = self.pot_state['pot_size'] if self.pot_state else 0
        call_total = self.pot_state['call_total'] if self.pot_state else self.bb_amount
        struct = {
            'call_total' : call_total,
            'check_allowed' : board_stage != "PREFLOP",
            'minimum_raise' : 2*self.bb_amount,
            'pot_size' : pot_size # preserve it across betting rounds, may be null
        }
        self.pot_state = PotState(**struct)

    def collect_blinds(self, sb_amount : int):
        self.pot_state['pot_size'] += 3*sb_amount
    
    def update_pot_state(self, last_action : PlayerBetResponse, last_player_total: int, next_player_total : int) -> None:
        self.pot_state['pot_size'] += last_action['amount_bet']
        if last_action['action'] == 'raise' or last_action['action'] == 'all-in':
            self.pot_state['call_total'] = last_player_total
            self.pot_state['minimum_raise'] = 2*last_action['amount_bet']

        # print(f"next_player_total: {next_player_total} =? call_total: {self.pot_state['call_total']}")
        if next_player_total == self.pot_state['call_total']:
            self.pot_state['check_allowed'] = True
        else:
            self.pot_state['check_allowed'] = False


    def _set_state(self, new_pot_state : PotState):
        self.pot_state = new_pot_state
