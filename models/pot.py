from models.entities import BoardStage, Player, PlayerBetResponse
from typing import List, Dict
from uuid import UUID
from models.definitions import PotState, PlayerBetResponse, BettingRoundRecord, PlayerStatus, PlayerAction
import pprint



class Pot():
    '''
    Saves betting history in a single hand.
    awaits responses in methods betting_round()
    Gets Updated after every single player action. how would MVC design work?
    {
        "pre-flop" : [
            {
                "<player_id>" : {
                        "record" :
                "role" : "sb",
                "price_to_call" : 20
                "action" : "call",
                "amount" : 20,
            }
        ]
    }
    '''   
    def __init__(self, sb_amount:int): 
        self.sb_amount : int = sb_amount 
        self.bb_amount : int = sb_amount*2
        self.pot_state : PotState = PotState(call_amount = self.bb_amount,
                                             check_allowed=False,   # Default
                                            minimum_raise=2*self.bb_amount,
                                            pot_size=0) ## Initial default. 


    def get_state(self) -> PotState:
        '''
        returns the necessary information about the pot state for any player to make a decision. 
        '''
        return self.pot_state.copy()
    

    def update_check_allowed(self, boolean:bool)->None:
        self.pot_state['check_allowed'] = boolean

    def initialize_pot_state(self, board_stage:BoardStage):
        if board_stage == BoardStage.PREFLOP:
            self.pot_state['check_allowed'] = False
        else:
            self.pot_state['check_allowed'] = True
            self.pot_state['call_amount'] = 0
            self.pot_state['minimum_raise'] = 2*self.bb_amount

    
    def update_pot_state(self, last_active_player: Player, last_action : PlayerBetResponse) -> None:
        # print("LAST PLAYER ACTION: ")
        # print(last_action)
        action : str = last_action['action']
        amount : int = last_action['amount_bet']
        self.pot_state['pot_size'] += amount

        if action=='check':
            self.pot_state['check_allowed'] = True
        elif action == 'raise':
            self.pot_state['check_allowed'] = False
            self.pot_state['call_amount'] = last_active_player.f_amount_bet_this_hand() # their total becomes the calling amount
            self.pot_state['minimum_raise'] = 2*amount
        else:
            self.pot_state['check_allowed'] = False

    def overwrite_pot_state(self, new_pot_state : PotState):
        self.pot_state = new_pot_state

    def get_hand_history(self):
        return self.hand_history