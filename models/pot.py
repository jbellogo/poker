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

    
    def update_pot_state(self, last_active_player: Player, last_action : PlayerBetResponse, turn_index :int) -> None:
        print("LAST PLAYER ACTION: ")
        print(last_action)
        action : str = last_action['action']
        amount : int = last_action['amount_bet']
        self.pot_state['pot_size'] += amount

        # @TODO there is an issue with call amount. test_round4 is failing
        
        # Basically everytime there is a raise, we should update check_allowed and call_amount

        if action=='check':
            self.pot_state['check_allowed'] = True
        else:
            self.pot_state['check_allowed'] = False

        
        # Fine tunning:
        if action == 'raise':
            self.pot_state['check_allowed'] = False
            self.pot_state['call_amount'] = last_active_player.f_amount_bet_this_hand() # their total becomes the calling amount
            self.pot_state['minimum_raise'] = 2*amount


    def overwrite_pot_state(self, new_pot_state : PotState):
        self.pot_state = new_pot_state

    # def get_tailored_pot_state(self, player : Player):
    #     pot_copy = self.pot_state.copy() 
    #     # Makes a copy so so that it can return the amount player i needs to call while keeping the calling amount equal to the last raise. 
    #     pot_copy['call_amount'] -= player.amount_bet_this_hand() # updates
    #     return pot_copy

    # def betting_round(self, board_stage : BoardStage):
    #     '''
    #     Single betting round ie preflop or flop or etc. 
    #     Awaits active player actions
    #     Updates player status from action response, ie all-in, folded, etc.
    #     '''
    #     active_players = len(self.players)
    #     players_to_call = active_players
    #     while players_to_call != 0:
    #         for player in self.players:
    #             if players_to_call == 0:
    #                 break
    #             if player.hand_status() == "active":
    #                 # print(f"\nplayers_to_call = {players_to_call}")
    #                 # print(f"active_players = {active_players}")
    #                 pot_copy = self.get_tailored_pot_state(player)
    #                 # the tailored pot state is sent to player with their respective call price. 
    #                 response : PlayerBetResponse = player.make_bet(pot_copy) # needs to be awaited. 
    #                 player_id = "player" + str(response['pid'])
    #                 betting_record = BettingRoundRecord(response=response, pot_state=pot_copy)
    #                 self.hand_history[board_stage.name].append({player_id : betting_record} )
    #                 ### THEN WE UPDATE. this way we store the pot_state at the time before the player makes his move
    #                 self.update_pot_state(response, board_stage)
    #                 player_action =  response['action']
    #                 if  player_action == "raise":
    #                     players_to_call = active_players-1 # all active players
    #                 elif player_action == "fold":
    #                     players_to_call-=1
    #                     active_players-=1
    #                     player.set_status("fold")
    #                 elif player_action == "call" or player_action == "check":
    #                     players_to_call -=1
                    
                    
    #     print("betting round over!")
    #     self.persist_betting_round()

    def persist_betting_round(self):
        pass

    def get_hand_history(self):
        return self.hand_history