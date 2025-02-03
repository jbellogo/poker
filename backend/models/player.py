from models.definitions import *
from models.entity import Entity
from typing import Optional
import asyncio



class Player(Entity):
    # public info
    ## inputed values
    name : str
    pid : int # Only keeping for consistent color coding. 
    sid : str
    funds : int

    ## internaly set
    role : PlayerRole = "other"  # @TODO update them every round
    betting_status : PlayerStatus = "active" ## carefull with this. 
    last_action : PlayerAction = "no-action"

    # internal
    current_bet : int = 0


    # private info
    cards : List[Card] = [] # no need for tuple since this is all internal

    # supporting info
    _number_cards_dealt : int = 2

    def __str__(self):
        return self.model_dump_json()

    def _cards_dealt(self) -> int:
        return self._number_cards_dealt
    
    def set_role(self, role: PlayerRole)->None:
        self.role = role
    
    def set_status(self, new_status : PlayerStatus)->None:
        self.betting_status = new_status

    def get_betting_status(self):
        return self.betting_status

    def get_id(self) -> int:
        return self.pid
    
    def get_sid(self) -> str:
        return self.sid
    
    def get_role(self) -> PlayerRole:
        return self.role
        
    def get_current_bet(self)->int:
        return self.current_bet
    
    def reset_amount_bet_this_hand(self):
        self.current_bet = 0

    def collect_blind(self, sb_amount : int):
        print(f"collecting blind for {self.role}")
        if self.role == "sb":
            print(f"sb collecting amount: {sb_amount}")
            self.funds -= sb_amount
            self.current_bet += sb_amount
        elif self.role == "bb":
            print(f"bb collecting amount: {sb_amount*2}")
            self.funds -= sb_amount*2
            self.current_bet += sb_amount*2

    def get_state(self)->PlayerState:
        # you can make this into a TypedDict if you want. 
        return {
            "public_info": {
                "name": self.name,
                "pid": self.pid,
                "sid": self.sid,
                "funds": self.funds,
                "role": self.role,
                "last_action": self.last_action,
                "current_bet": self.current_bet,
                "betting_status": self.betting_status
            },
            "private_info": {
                "cards": self.cards
            }
        }
        

    async def request_betting_response(self) -> dict:
        '''
             # Receive this: 
            {
                'sid' : 'sid1',
                'amount_bet' : 40,
                'action' : "call",
            }
        '''
        await asyncio.sleep(1)
        return None
    
    def validate_response(self, response : dict, game_state : GameState) -> PlayerBetResponse:
        # Already validated in frontend. Just for testing. 
        assert(response['amount_bet'] <= self.funds)
        if(response['action'] == 'fold'):
            assert(response['amount_bet']==0) 
        if(response['action'] == 'all-in'):
            assert(response['amount_bet']==self.funds)
        if(response['action'] == 'call'):
            assert(response['amount_bet']==game_state['pot']['call_amount'])  
        if(response['action'] == 'check'):
            assert(response['amount_bet']==0) 
            assert(game_state['pot']['check_allowed'])  
        return PlayerBetResponse(**response)





    async def make_bet(self, game_state: GameState) -> Optional[PlayerBetResponse]: 
        '''
        Wrapper that Uses API response from request_betting_response() and:
        - validates the response
        - converts relevant fields to internal structures (PlayerRole, PlayerAction, hand, etc)
        - updates local player fields.
        @TODO needs work with the new schema. 
        '''
        
        response : PlayerBetResponse  = await self.request_betting_response() # pass to it a GameState and PlayerState
        response = self.validate_response(response, game_state)
        # update local player records with response. 
        self.funds -= response['amount_bet']
        self.betting_status = PlayerAction(response['action']).to_status()  ## this one is iffy
        self.current_bet += response['amount_bet']
        self.last_action = response['action']
        return response

