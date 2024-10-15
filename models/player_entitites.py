from models.entity import Entity
from typing import Literal
from uuid import UUID
from pydantic import BaseModel
from typing_extensions import TypedDict


############
# class BettingRoles(intEnum):
#     OTHER  = 0
#     SMALL_BLIND = 1
#     BIG_BLIND = 2


class PlayerBetResponse(BaseModel):
    pid : int
    player_funds : int
    role : Literal["sb", "bb", "other"] = "other"
    action : Literal["call", "raise", "fold"]
    amount_bet : int 
    # blind_tax : int = - BettingRoles.value * SMALL_BLIND

    

    

class PotState(TypedDict):
    call_amount : int
    check_allowed : bool
    minimum_raise : int
    pot_size : int



class Player(Entity):
    pid : int
    funds : int
    role : Literal["sb", "bb", "other"] = "other"
    number_cards_dealt : int = 2
    current_hand_betting_status : Literal["active", "fold", "all-in", "inactive"] = "inactive"


    def cards_dealt(self) -> int:
        return self.number_cards_dealt
    
    def hand_status(self):
        return self.current_hand_betting_status

    def set_status(self, new_status : Literal["active", "fold", "all-in", "inactive"]):
        self.current_hand_betting_status = new_status
    
    async def make_bet(self, pot : PotState):
        ### prepare the JSON information package to send to player to make a betting decision: 
        
        pre_bet_state = pot.get_pre_bet_info()
        # @TODO Implement API to connect to frontend. 
        # pre_bet_state = {
        #     "call_amount" : pot.get_calling_amount(),
        #     "check_allowed" : True,
        #     "minimum_raise" : 2*pot.get_calling_amount(),            
        #     "pot_size" : pot.get_pot_size() 
        # }
        pre_bet_state["player_funds"] = self.funds
        ## 1**) send request to player's ip address, await resposne.
        print(pre_bet_state)
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
        return response


###########
