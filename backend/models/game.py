
from models.player import Player
from models.board import Board
from models.deck import Deck
from typing import List, Dict, Optional
from uuid import UUID
from models.definitions import *
import pprint
from models.config import * # Global variables, better practice to use json.
from models.pot import Pot
import asyncio
import copy



class Game():
    def __init__(self, sio, max_players : int = MAX_PLAYERS, sb_amount : int = SB_AMOUNT, initial_player_funds : int = INITIAL_PLAYER_FUNDS):
        self.sio = sio # socketio server
        self.max_players = max_players
        self.sb_amount = sb_amount
        self.initial_player_funds = initial_player_funds
        # variables
        self.rounds  : List[BoardStage] = [BoardStage.PREFLOP, BoardStage.FLOP, BoardStage.TURN, BoardStage.RIVER]
        self.players : List[Player] = []
        self.pot : Pot = Pot(sb_amount=sb_amount)
        self.sb_index : int = 0
        self.deck : Deck =  Deck()
        self.board : Board = Board()
        # For persistence
        self.hand_history : Dict[str, List[BettingRoundRecord]] = {"PREFLOP": [], "FLOP":[], "TURN":[], "RIVER":[]} 


    def next_sb_turn(method):
        '''decorator, increases modular count for small_blin index, corresponding to next turn.'''
        def wrapper(self, *args, **kw):
            self.sb_index += 1
            self.sb_index %= len(self.players)
            return method(self, *args, **kw)
        return wrapper
    
    def add_player(self, sid: str, player_name: str):
        self.players.append(
            Player(name = player_name,
                   pid = len(self.players)+1, 
                   sid = sid, 
                   funds = self.initial_player_funds))

    def clear_board(self):
        self.deck : Deck = Deck()
        self.board : Board = Board()


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

    def remove_player(self, sid: str) -> None:
        self.players = [player for player in self.players if player.sid != sid]

    def get_players(self) -> List[int]:
        '''
        Returns a list of PIDs to simplify tests
        '''
        return [player.get_id() for player in self.players]
    
    def get_sb_index(self) -> int:
        return self.sb_index


    def get_hand_history(self):
        return self.hand_history

    def persist_betting_round(self):
        '''Save to db... coming soon'''
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


    async def betting_round(self, board_stage : BoardStage) -> None:  
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
                    elif player_action == "all-in":
                        players_to_call = active_players-1
                        active_players-=1
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

    async def start(self, server):
        # while True:
        pass
            ## 1) Wait for players to join server

    def get_player_state(self, sid):
        for player in self.players:
            if player.get_sid() == sid:
                return player.get_state()


    def handle_player_action(self, sid, data):
        print(f"handling action from {sid}: {data}")
        type = data['type']
        if type == 'hero_join_request':
            if len(self.players)+1 < MAX_PLAYERS:
                self.add_player(sid, data['name'])
                print(f"New number of players: {len(self.players)}")
                # Sent to hero, with his information.
                self.sio.emit('message', {"type": "hero_join_success", 'data' : self.get_player_state(sid)}, to=sid)
                # Sent to all other players, with the updated list of players.
                players_public_info = [player.get_state()['public_info'] for player in self.players]
                self.sio.emit('message', {"type": "new_player_join", "players" : players_public_info})

            else:
                self.sio.emit('message', {"type": "player_join_failure", "message": "Game is full"}, to=sid)
                self.sio.disconnect(sid)
        

