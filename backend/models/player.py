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

    ## internal
    role : PlayerRole = "other"  # @TODO update them every round
    last_action : PlayerAction = "no-action"
    current_bet : int = 0
    bet_total : int = 0
    betting_status : PlayerStatus = "active"

    # private info
    cards : List[Card] = []

    # supporting info
    _number_cards_dealt : int = 2

    def __str__(self):
        return self.model_dump_json()

    def _cards_dealt(self) -> int:
        return self._number_cards_dealt
    
    def set_role(self, role: PlayerRole)->None:
        self.role = role
    
    def get_id(self) -> int:
        return self.pid
    
    def get_sid(self) -> str:
        return self.sid
    
    def get_role(self) -> PlayerRole:
        return self.role
        
    def get_bet_total(self)->int:
        return self.bet_total
    
    def get_betting_status(self) -> PlayerStatus:
        return self.betting_status
    
    # def reset_bet_total(self):
    #     self.bet_total = 0

    def collect_blind(self, sb_amount : int):
        if self.role == "sb":
            self.funds -= sb_amount
            self.bet_total += sb_amount

        elif self.role == "bb":
            self.funds -= sb_amount*2
            self.bet_total += sb_amount*2

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
                "betting_status": self.betting_status,
                "bet_total": self.bet_total,
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
            assert(response['amount_bet'] + self.bet_total == game_state['pot']['call_total'])  
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
        self.bet_total += response['amount_bet']
        self.current_bet = response['amount_bet']
        self.last_action = response['action']
        self.betting_status = PlayerAction(response['action']).to_status()  ## this one is iffy
        return response

