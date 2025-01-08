from models.entities import Deck, Board, BoardStage, Player, PlayerBetResponse
from typing import List, Dict
from uuid import UUID
from models.definitions import PotState, PlayerBetResponse, BettingRoundRecord
import pprint
from pydantic import BaseModel, ConfigDict
from models.config import * # Global variables, better practice to use json.
from models.pot import Pot



class Game(BaseModel):
    # variables
    rounds  : List[BoardStage] = [BoardStage.PREFLOP, BoardStage.FLOP, BoardStage.TURN, BoardStage.RIVER]
    players : List[Player] = [Player(pid = i, funds = INITIAL_PLAYER_FUNDS, betting_status = "active") for i in range(1, NUM_PLAYERS+1)]
    pot : Pot = Pot(bb_amount=40)
    sb_index : int = 0

    # I do want this class to deal with hand data persistence. 
    hand_history = {"PREFLOP": [], "FLOP":[], "TURN":[], "RIVER":[]} 


    model_config = ConfigDict(arbitrary_types_allowed=True) # very important to circumvent thorough validation of created types.


    def next_sb_turn(method):
        '''decorator, increases modular count for small_blin index, corresponding to next turn.'''
        def wrapper(self, *args, **kw):
            self.sb_index += 1
            self.sb_index %= NUM_PLAYERS
            return method(self, *args, **kw)
        return wrapper

    async def play_hand(self):
        # Initialize clean Deck and Board
        deck = Deck()
        board = Board()

        for round in self.rounds:
            board.set_round(round)
            # 1) Show Board
            board.show()  ## Once we have a frontend, this game logic will go there. 
            # 2) Betting Round 
            self.update_player_turns()

            await self.betting_round(round) 
            # Awaits player responses and uploads pot and player status. 
            # This should update the pot and this should be made visible in real time. 


    def get_players(self) -> List[int]:
        '''
        Returns a list of PIDs to simplify tests
        '''
        return [player.get_id() for player in self.players]
    
    def get_sb_index(self) -> int:
        return self.sb_index


    @next_sb_turn
    def update_player_turns(self) -> None:
        '''
        copies the list starting at sb_index and wrapping around
        Increases the sb_index turn
        '''
        indx =  self.sb_index
        print(f"MY index : {indx}")
        # self.players = self.players[indx:] + self.players[:indx]
        self.players.append(self.players.pop(0)) # one at a time.
 

    def persist_player_action(self, response: PlayerBetResponse, betting_round : BoardStage):
        
        player_id = "player" + str(response['pid'])
        betting_record = BettingRoundRecord(response=response, pot_state=self.pot.get_state()) 
        self.hand_history[betting_round.name].append({player_id : betting_record} )
        pass


    async def betting_round(self, board_stage : BoardStage):
        '''
        Single betting round ie preflop or flop or etc. 
        Awaits active player actions
        Updates player status from action response, ie all-in, folded, etc.
        '''
        active_players = len(self.players)
        players_to_call = active_players
        while players_to_call != 0:
            for player in self.players:
                if players_to_call == 0:
                    break
                if player.get_betting_status() == "active":

                    # NOW) the tailored pot state is sent to player with their respective call price. 
                    # pot_copy = self.get_tailored_pot_state(player)  ## NOT NEEDED ?
                    response : PlayerBetResponse = await player.make_bet(self.pot.get_state())
                    
                    # NOW) persist betting record for player. 
                    self._persist_player_action(response)
                    
                    # NOW) THEN WE UPDATE pot state with player response. this way we store the pot_state at the time before the player makes his move
                    self.update_pot_state(response, board_stage)
                    player_action =  response['action']
                    if  player_action == "raise":
                        players_to_call = active_players-1 # all active players
                    elif player_action == "fold":
                        players_to_call-=1
                        active_players-=1
                        player.set_status("fold")
                    elif player_action == "call" or player_action == "check":
                        players_to_call -=1
                    
                    
        print("betting round over!")
        self.persist_betting_round()


            






            
# class Hand(BaseModel):

#     '''     
#     Acts as dealer: Creates a deck, deals cards to board and players
#     will need to take list[pleyrs] as a reference to update their cards. 
#     Also takes "TURN" for the index of the small blind starting 

#     '''
#     def __init__(self, sb_amount:int, players: List[Player], sb_player_id: UUID):
#         self.sb_amount = sb_amount   # Passed and updated every hand. 
#         self.players = players
#         self.sb_player_id = sb_player_id
#         # Initialized per Hand.
#         self.board : Board = Board()
#         self.deck : Deck = Deck()    
#         self.pot : Pot = Pot(sb_amount=sb_amount, players=players, sb_player_id =sb_player_id)


#     def start(self):
#         for player in self.players:
#             self.deck.deal_cards(player)

        
#         ## RUNS FOR STAGES PREFLOP, FLOP, TURN, RIVER.
#         while(self.board.next_stage()):
#             ## 1) render the board
#             print(self.board)
#             ## 2) await betting round. 
#             self.pot.betting_round() 
#             ## 3) update the board. 
#             self.deck.deal_cards(self.board)
        
#         ## 4) Determine winner. 
            
#     def persist_hand():
#         ''' saves hand data/state to database'''
#         pass




# class Hand(str, Enum):
#     '''
#     it should also have tie-breaking information
#     Each hand has a number associated with it. We use this number for breaking ties.
#     --Ex) Straight has the biggest number. In the event of two players having straights, 
#           the player whose straight hand has the maximum number wins.
#           Royal_flush has none. 
#           Straight Flush has largest number. 
#           Four_of_a_kind has the number. 
#           full_house has the triple number THEN the secondary number. 
#           flush has the suit ranks  
#           three of a kind the number 

#     '''


