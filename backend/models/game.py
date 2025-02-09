
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
    def __init__(self, sio = None, max_players : int = MAX_PLAYERS, sb_amount : int = SB_AMOUNT, initial_player_funds : int = INITIAL_PLAYER_FUNDS):
        self.sio = sio # socketio server
        self.max_players = max_players
        self.sb_amount = sb_amount
        self.initial_player_funds = initial_player_funds
        # variables
        self.rounds  : List[BoardStage] = [BoardStage.PREFLOP, BoardStage.FLOP, BoardStage.TURN, BoardStage.RIVER]
        self.players : List[Player] = []
        self.pot : Pot = Pot(sb_amount=sb_amount)
        self.raise_occurred : bool = False
        # self.sb_index : int = 0
        self.deck : Deck =  Deck()
        self.board : Board = Board()
        # For persistence
        self.hand_history : Dict[str, List[BettingRoundRecord]] = {"PREFLOP": [], "FLOP":[], "TURN":[], "RIVER":[]} 


    # def next_sb_turn(method):
    #     '''decorator, increases modular count for small_blin index, corresponding to next turn.'''
    #     def wrapper(self, *args, **kw):
    #         self.sb_index += 1
    #         self.sb_index %= len(self.players)
    #         return method(self, *args, **kw)
    #     return wrapper
    
    def add_player(self, sid: str, player_name: str):
        self.players.append(
            Player(name = player_name,
                   pid = len(self.players)+1, 
                   sid = sid, 
                   funds = self.initial_player_funds))

    def clear_board(self):
        self.deck : Deck = Deck()
        self.board : Board = Board()


    # @next_sb_turn
    def update_player_turns(self) -> None:
        '''
        shifts the players list to the left, 
        effectively updating the sb_index.
        sb_index remains 0 throughout.
        '''
        self.players.append(self.players.pop(0)) # one at a time.
 

    def persist_player_action(self, response: PlayerBetResponse, game_state: GameState, player_state: PlayerState) -> None:        
        betting_record = BettingRoundRecord(sid= response['sid'], 
                                            response=response, 
                                            game_state=game_state,
                                            player_state=player_state) 
        stage : str = game_state['board']['stage']
        self.hand_history[stage].append(betting_record)


    def remove_player(self, sid: str) -> None:
        self.players = [player for player in self.players if player.get_sid() != sid]

   

    def get_hand_history(self):
        return self.hand_history

    def persist_betting_round(self):
        '''Save to db... coming soon'''
        pass


    def initialize_game_state(self, board_stage: BoardStage)-> None:
        '''
        updates pot_state at the beginning of betting round passed.
        '''
        self.pot.initialize(board_stage)
        self.board.set_round(board_stage)  # just needed for testing

    def collect_blinds(self):
        '''
        Take blinds from sb and bb, first turn is player #3
        '''
        self.players[0].collect_blind(self.sb_amount)
        self.players[1].collect_blind(self.sb_amount)
        self.pot.collect_blinds(self.sb_amount)

    def initialize_players_state(self):
        '''
        takes care of updating player roles, and resetting their amount bet this hand to 0.
        '''

        for i, player in enumerate(self.players):
            if i == 0: 
                self.players[i].set_role("sb")
            elif i==1: 
                self.players[i].set_role("bb")
            else: 
                self.players[i].set_role("other")
            player.reset_bet_total()

        ## all our work is done on active players
        self.collect_blinds()
        # To start at player #3
        self.players.append(self.players.pop(0))
        self.players.append(self.players.pop(0))


    def get_state(self) -> GameState:
        '''
        Returns a Game state for the player with his personalized call amount. 
        '''
        pot : PotState = self.pot.get_state()
        board : BoardState = self.board.get_state()
        return GameState(pot= pot, board=board)



    def get_players_to_call(self) -> int:
        '''
        Returns the number of players to call.
        Since this is used after a raise, isnt it just active players - 1?
        '''
        count : int = 0
        for player in self.players:
            if player.get_betting_status() == "active":
                # print(f"player_id: {player.get_id()}, bet_total: {player.get_bet_total()}, call_total: {self.pot.get_state()['call_total']}")
                if player.get_bet_total() != self.pot.get_state()['call_total']:
                    count += 1
        return count
    
    def update_lim(self, turn : int, lim : int, last_action : PlayerAction) -> int:
        additional_turns = 0
        if last_action == "raise" or last_action == "all-in":
            # print(f"last_action: {last_action}")
            additional_turns = self.get_players_to_call()
            return turn + additional_turns + 1
        return lim # the original number of turns


    async def betting_round(self, board_stage : BoardStage) -> None:  
        '''
        Single betting round ie preflop or flop or etc. 
        Awaits active player actions
        Updates player status from action response, ie all-in, folded, etc.
        '''
        self.initialize_game_state(board_stage)
        self.initialize_players_state()


        turn = 0
        lim = len(self.players)
        while turn < lim:
            i = turn%len(self.players)
            # # print("-----------STARTING LOOP-----------")
            # print(f"players_to_call: {players_to_call}")
            state : GameState = self.get_state()
            response : Optional[PlayerBetResponse] = await self.players[i].make_bet(state)
            self.persist_player_action(response, state, self.players[i].get_state())
            last_action = response['action']
            last_player_total = self.players[i].get_bet_total()
            next_player_total = self.players[(i+1)%len(self.players)].get_bet_total()
            self.pot.update_pot_state(last_action=response, last_player_total=last_player_total, next_player_total=next_player_total)
            lim = self.update_lim(turn, lim, last_action)
            turn += 1
            print(f"turn: {turn} < lim: {lim}")

        self.persist_betting_round()
        self.update_player_turns()  ## needs to go before initialize_players state
        await asyncio.sleep(0.1)  ## might be necessary until we have the calls

    def determine_winner(self):
        '''
        Determine the winner of the hand.
        '''
        pass

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
        self.determine_winner()

    
    async def start(self, server):
        # while True:
        pass
            ## 1) Wait for players to join server

    def get_player_state(self, sid):
        for player in self.players:
            if player.get_sid() == sid:
                return player.get_state()


    def handle_player_action(self, sid, data):
        '''
        Interacts with the socketio server to handle player actions.
        '''
        # print(f"handling action from {sid}: {data}")
        type = data['type']
        if type == 'hero_join_request':
            if len(self.players)+1 < MAX_PLAYERS:
                self.add_player(sid, data['name'])
                # print(f"New number of players: {len(self.players)}")
                # Sent to hero, with his information.
                self.sio.emit('message', {"type": "hero_join_success", 'data' : self.get_player_state(sid)}, to=sid)
                # Sent to all other players, with the updated list of players.
                players_public_info = [player.get_state()['public_info'] for player in self.players]
                self.sio.emit('message', {"type": "new_player_join", "players" : players_public_info})

            else:
                self.sio.emit('message', {"type": "player_join_failure", "message": "Game is full"}, to=sid)
                self.sio.disconnect(sid)
        
       
