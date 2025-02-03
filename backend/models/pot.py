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
    

    # def update_check_allowed(self, boolean:bool)->None:
    #     self.pot_state['check_allowed'] = boolean

    def initialize_pot_state(self, board_stage:BoardStage):
        if board_stage == BoardStage.PREFLOP:
            self.pot_state['check_allowed'] = False
        else:
            self.pot_state['check_allowed'] = True
            self.pot_state['call_amount'] = 0
            self.pot_state['minimum_raise'] = 2*self.bb_amount

    def collect_blinds(self, sb_amount : int):
        self.pot_state['pot_size'] += 3*sb_amount
    
    def update_pot_state(self, last_player: Player, last_action : PlayerBetResponse, next_player : Player) -> None:
        self.pot_state['pot_size'] += last_action['amount_bet']

        # if action=='check':
        #     self.pot_state['check_allowed'] = True
        if last_action['action'] == 'raise':
            # self.pot_state['check_allowed'] = False
            self.pot_state['call_amount'] = last_player.get_current_bet() # their total becomes the calling amount
            self.pot_state['minimum_raise'] = 2*last_action['amount_bet']
        ## THIS SHOLD BE DEPENDANT ON THE PLAYER ABOUT TO ACT!!
        # if their current bet is equal to the call amount, check is allowed.
        # print(f"next_player.get_current_bet(): {next_player.get_current_bet()}")
        # print(f"self.pot_state['call_amount']: {self.pot_state['call_amount']}")
        if next_player.get_current_bet() == self.pot_state['call_amount']:
            self.pot_state['check_allowed'] = True
        else:
            self.pot_state['check_allowed'] = False
        # elif action == 'call'and players_to_call == 0:
        #     self.pot_state['check_allowed'] = True
        # else:
        #     self.pot_state['check_allowed'] = False

    def overwrite_pot_state(self, new_pot_state : PotState):
        self.pot_state = new_pot_state

    def get_hand_history(self):
        return self.hand_history