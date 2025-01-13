from models.entities import Deck, Board, BoardStage, Player, PlayerBetResponse
from typing import List, Dict, Optional
from uuid import UUID
from models.definitions import *
import pprint
from models.config import * # Global variables, better practice to use json.
from models.pot import Pot
from aiohttp import ClientSession
import asyncio
import copy



class Game():
    # Input

    def __init__(self, num_players : int, sb_amount:int):
        self.num_players = num_players

        # variables
        self.rounds  : List[BoardStage] = [BoardStage.PREFLOP, BoardStage.FLOP, BoardStage.TURN, BoardStage.RIVER]
        self.players : List[Player] = [Player(pid = i, funds = INITIAL_PLAYER_FUNDS, betting_status = "active") for i in range(1, num_players+1)]

        self.pot : Pot = Pot(sb_amount=sb_amount)
        self.sb_index : int = 0
        self.deck : Deck =  Deck()  ## Hmmm don't know how I feel about this
        self.board : Board = Board()
        self.hand_history : Dict[str, List[BettingRoundRecord]] = {"PREFLOP": [], "FLOP":[], "TURN":[], "RIVER":[]} 


    # model_config = ConfigDict(arbitrary_types_allowed=True) # very important to circumvent thorough validation of created types.
    def next_sb_turn(method):
        '''decorator, increases modular count for small_blin index, corresponding to next turn.'''
        def wrapper(self, *args, **kw):
            self.sb_index += 1
            self.sb_index %= self.num_players
            return method(self, *args, **kw)
        return wrapper

    def clear_board(self):
        self.deck : Deck = Deck()
        self.board : Board = Board()


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
        Copies the list starting at sb_index and wrapping around
        Increases the sb_index turn through decorator
        '''
        self.players.append(self.players.pop(0)) # one at a time.
 

    def persist_player_action(self, response: PlayerBetResponse, game_state: GameState) -> None:        
        betting_record = BettingRoundRecord(pid= response['pid'], 
                                            response=response, 
                                            game_state=game_state) 
        stage : str = game_state['board']['stage']
        self.hand_history[stage].append(betting_record)

    # def handle_player_action(self, response: PlayerBetResponse, game_state: GameState, player:Player) -> None:
    #     if response['action'] # update player status

    #     self.persist_player_action(response, game_state)


    def get_hand_history(self):
        return self.hand_history

    def persist_betting_round(self):
        '''Save self.hand_history somewhere'''
        # @TODO persist to DB
        pass

    def get_state(self)-> GameState:
        pass

    def initialize_game_state(self, board_stage: BoardStage)-> None:
        '''
        updates pot_state at the beginning of betting round passed.
        '''
        self.pot.initialize_pot_state(board_stage)
        self.board.set_round(board_stage)  # just needed for testing

    def initialize_players_state(self):
        '''
        takes care of updating player roles, and resetting their amount bet this hand to 0.
        '''

        for i, player in enumerate(self.players):
            if i == 0: 
                self.players[i].set_role(PlayerRole.SMALL_BLIND)
            elif i==1: 
                self.players[i].set_role(PlayerRole.BIG_BLIND)
            else: 
                self.players[i].set_role(PlayerRole.OTHER)
            player.reset_amount_bet_this_hand()
        self.active_players = copy.deepcopy(self.players)



    def get_personalized_state(self, player:Player) -> GameState:
        pot : PotState = self.pot.get_state() # this returns a copy, perfect for us
        pot['call_amount'] -= player.f_amount_bet_this_hand()
        board : BoardState = self.board.get_state()
        return GameState(pot= pot, board=board)

    def update_active_players(self, player: Player, response_action : PlayerAction):
        '''
        updates player statuses based on response
        but now we are mutating the thing we are iterating...
        '''
        if response_action in [PlayerAction.ALLIN, PlayerAction.FOLD]:
            # How do we hide them from the list?
            self.active_players.remove(player)



    async def betting_round(self, board_stage : BoardStage, session: ClientSession = None) -> None:  
        '''
        Single betting round ie preflop or flop or etc. 
        Awaits active player actions
        Updates player status from action response, ie all-in, folded, etc.
        '''
        self.initialize_game_state(board_stage)
        self.initialize_players_state()

        active_players :int = len(self.active_players)
        players_to_call:int = active_players

        while players_to_call != 0:
            if players_to_call == 0:
                break
            # print("-----------STARTING LOOP-----------")
            for player in self.active_players:
                print(player)               
                if player.get_betting_status() == "active":
                    # NOW) the tailored pot state is sent to player with their respective call price. 
                    state : GameState = self.get_personalized_state(player)
                    # print(f"calling await player.make_bet(), num raises={number_of_raises}")
                    response : Optional[PlayerBetResponse] = await player.make_bet(state)

                    # NOW) persist betting record for player. 
                    self.persist_player_action(response, state)
                    # NOW) THEN WE UPDATE pot state with player response. this way we store the pot_state at the time before the player makes his move
                    self.pot.update_pot_state(player, response)
                    # NOW) we need a function which updates the list of players if they have gone all-in or folded
                    self.update_active_players(player, response['action']) 

                    player_action =  response['action']
                    if  player_action == "raise":
                        players_to_call = active_players-1 # all active players
                    elif player_action == "fold":
                        players_to_call-=1
                        active_players-=1
                    elif player_action == "call":
                        players_to_call -=1
                    elif player_action == "check":
                        pass
                        

        self.persist_betting_round()
        self.update_player_turns()  ## needs to go before initialize_players state

        await asyncio.sleep(0.1)  ## might be necessary until we have the calls


    async def play_hand(self):
        # Initialize clean Deck and Board
        self.clear_board()
        for player in self.players:
            self.deck.deal_cards(player)

        for round in self.rounds:
            self.board.set_round(round)
            self.deck.deal_cards(self.board)

            # 1) Show Board
            self.board.show()  ## Once we have a frontend, this game logic will go there. 
            # 2) Betting Round 

            await self.betting_round(round) 
            # Awaits player responses and uploads pot and player status. 
            # This should update the pot and this should be made visible in real time. 

            






            
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


