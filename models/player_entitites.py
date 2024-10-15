from models.entity import Entity
from typing import Literal


############
class BettingRoles(intEnum):
    OTHER  = 0
    SMALL_BLIND = 1
    BIG_BLIND = 2


class PlayerBetResponse(BaseModel):
    ## How about a player has one of these objects? and then e pass them the pot state to decide what to do?
    action : Literal["call", "raise", "fold"]
    # blind_tax : int = - BettingRoles.value * SMALL_BLIND
    amount_bet : int = 0



class Player(Entity):
    player_uui : UUID
    role : BettingRoles
    number_cards_dealt : int = 2
    ## Has money
    funds : int

    def cards_dealt(self) -> int:
        return self.number_cards_dealt
    
    async def make_bet(self, pot : Pot):
        ### prepare the JSON information package to send to player to make a betting decision: 
        
        pre_bet_state = pot.get_pre_bet_info()

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
            "action" : "Fold", 
            "amount" : 0,
        })
        # update local player records with response. 
        self.funds -= response.amount_bet
        return response


###########
