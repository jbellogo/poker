from models.entity import Entity
from typing import Literal
from uuid import UUID
from pydantic import BaseModel
from models.definitions import PotState, PlayerBetResponse


class Player(Entity):
    pid : int
    funds : int
    role : Literal["sb", "bb", "other"] = "other"
    number_cards_dealt : int = 2
    current_hand_betting_status : Literal["active", "fold", "all-in", "inactive"] = "inactive"
    current_hand_amount_bet : int = 0

    def cards_dealt(self) -> int:
        return self.number_cards_dealt
    
    def hand_status(self):
        return self.current_hand_betting_status

    def set_status(self, new_status : Literal["active", "fold", "all-in", "inactive"]):
        self.current_hand_betting_status = new_status
    
    def amount_bet_this_hand(self):
        return self.current_hand_amount_bet
    
    # def add_amount_bet_this_hand(self, amount:int):
    #     ''' this is only used for testing'''
    #     self.current_hand_amount_bet+=amount

    async def make_bet(self, pot_state : PotState):
        ### prepare the JSON information package to send to player to make a betting decision: 
        
        # @TODO Implement API to connect to frontend. 
        # pre_bet_state = {
        #     "call_amount" : pot.get_calling_amount(),
        #     "check_allowed" : True,
        #     "minimum_raise" : 2*pot.get_calling_amount(),            
        #     "pot_size" : pot.get_pot_size() 
        # }
        ## 1**) send request to player's ip address, await resposne.
        ## this should already be validated as the pre_bet_state is betting constraints served to player
        
        response = PlayerBetResponse({
            "pid": self.pid,
            "player_funds" : self.funds,
            "role": self.role,
            "action" : "Fold", 
            "amount" : 0,
        })

        # update local player records with response. 
        self.funds -= response.amount_bet
        self.current_hand_amount_bet += response.amount
        return response


###########
